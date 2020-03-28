import csv
import pymysql
from pyphonetics import Soundex
from standardAbbr import address_abbr, state_abbr, gender_abbr
import Levenshtein
import string

def make_db():
    return pymysql.connect(
        host='localhost',
        database="lahacks",
        user="lahacks",
        password="1234567",
        db='db',
        autocommit=True,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


class PMD:
    def __init__(self):
        self.soundex = Soundex()
        self.nicknames = {}
        self.read_nicknames()

    def read_nicknames(self):
        with open('nicknames.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                self.nicknames[row[0]] = row[1:]
                self.nicknames[row[0]].append(row[0])

    def similarity(self, name1, name2, lev_only = False):
        # They both have only characters, then soundex is a good fit.
        if name1.isalpha() and name2.isalpha() and not lev_only:
            print(self.similarity_soundex(name1, name2), self.similarity_levenshtein(name1, name2))
            return max(self.similarity_soundex(name1, name2), self.similarity_levenshtein(name1, name2))
        return self.similarity_levenshtein(name1, name2)

    def similarity_soundex(self, name1, name2):
        return 1 - self.soundex.distance(name1, name2)/4

    def similarity_levenshtein(self, name1, name2):
        return 1 - Levenshtein.distance(name1, name2)/max(len(name1), len(name2))

    def similarity_street_helper(self, street1, street2):
        # We make every word into a unqiue character, and get the Levenshtein
        # distance of that.
        # Expects no more than 62 unique words...
        charset = list(string.ascii_letters+string.digits)
        charset_counter = 0
        unique_mapping = {}
        street1_arr = street1.split(" ")
        street2_arr = street2.split(" ")
        for street_arr in [street1_arr, street2_arr]:
            for i in street_arr:
                if i not in unique_mapping:
                    unique_mapping[i] = charset[charset_counter]
                    charset_counter += 1
        hashed_street=["", ""]
        for enum, street_arr in enumerate([street1_arr, street2_arr]):
            for i in street_arr:
                hashed_street[enum] += unique_mapping[i]
        print(self.similarity(hashed_street[0], hashed_street[1],lev_only=True), self.similarity(street1, street2, lev_only=True), 1 if street1=="" or street2 =="" else 0)
        return (max(self.similarity(hashed_street[0], hashed_street[1], lev_only=True), self.similarity(street1, street2, lev_only=True)), 1 if street1=="" or street2 =="" else 0)

    def similarity_names(self, name1, name2, threshold):
        empty  = 1 if name1 == "" or name2 == "" else 0
        name1 = self.prelim_cleaning(name1, alpha_only=True)
        name2 = self.prelim_cleaning(name2, alpha_only=True)
        score = 0
        if len(name1) > len(name2):
            temp = name1
            name1 = name2
            name2 = temp
        for i in self.nicknames.get(name1, [name1]):
            score = max(self.similarity(i, name2), score)
        return [1 if score > threshold else 0, 1 if score <= threshold and not empty else 0, empty]

    def similarity_alnum(self, str1, str2, threshold):
        print(str1, str2)
        score = self.similarity(self.prelim_cleaning(str1), self.prelim_cleaning(str2), lev_only=True)
        empty  = 1 if str1 == "" or str2 == "" else 0
        return [1 if score > threshold else 0, 1 if score <= threshold and not empty else 0, empty]

    def similarity_street(self, str1, str2, threshold):
        (score, empty) = self.similarity_street_helper(self.prelim_cleaning(str1), self.prelim_cleaning(str2))
        print(score)
        return [1 if score > threshold else 0, 1 if score <= threshold and not empty else 0, empty]

    def similarity_state(self, str1, str2, threshold):
        str1 = self.clean_state(self.prelim_cleaning(str1))
        str2 = self.clean_state(self.prelim_cleaning(str2))
        return [1 if str1 == str2 else 0, 1 if str1 != str2 else 0, 0 if str1=="" or str2 == "" else 0]

    def similarity_sex(self, str1, str2, threshold):
        str1 = self.clean_gender(self.prelim_cleaning(str1))
        str2 = self.clean_gender(self.prelim_cleaning(str2))
        return [1 if str1 == str2 else 0, 1 if str1 != str2 else 0, 0 if str1=="" or str2 == "" else 0]

    # Clean up street names by changing the abbrevations
    def clean_streets(self, street_name):
        street_name = street_name.split(" ")
        for enum, i in enumerate(street_name):
            street_name[enum] = address_abbr.get(i, i)
        return " ".join(street_name)

    def clean_state(self, states):
        return state_abbr.get(states, states)

    def clean_gender(self, gender):
        return gender_abbr.get(gender, gender)

    def prelim_cleaning(self, strr, alpha_only=False):
        strr = strr.lower()
        if alpha_only:
            return "".join([char for char in strr if char.isalpha() or char == " "])
        return strr

    def get_compare_fun(self):

        result = {}
        all_fields = ["PatientID","Patient Acct","First Name","MI","Last Name",
            "Date of Birth","Sex","Current Street 1","	Current Street 2",
            "Current City","Current State","Current Zip Code","Previous First Name",
            "Previous MI","Previous Last Name","Previous Street 1","Previous Street 2",
            "Previous City","Previous State", "Previous Zip Code"]

        simple_match_fields = ["Patient Acct","First Name","MI","Last Name",
            "Date of Birth","Zip Code"]

        streets = ["Current Street 1","	Current Street 2",
            "Previous Street 1","Previous Street 2"]

        alpha_only = ["First Name", "MI","Last Name"]

        alnum = ["Patient Acct #", "Date of Birth", "City", "Zip Code"]

        returned_field = ["Patient Acct #","First Name","MI","Last Name",
        "Date of Birth","Sex", "Street", "City", "State","Zip Code"]

        for i in simple_match_fields:
            result[i] = self.similarity_names

        for i in alnum:
            result[i] = self.similarity_alnum

        result['Sex'] = self.similarity_sex
        result['State'] = self.similarity_state
        result['Street'] = self.similarity_street

        return result
