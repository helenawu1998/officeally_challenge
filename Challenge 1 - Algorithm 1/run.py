"""
LA Hacks Submission for Office Ally Challenge #1. 

Team Patiently: Helena Wu, Victor Chen, Ziyan Mo

Code also in Jupyter notebook. This program loads the input CSV to a local 
SQLite database, 
"""

import sys
import pandas as pd
import sqlalchemy as db
import hashlib
from pyphonetics import Soundex, RefinedSoundex
from dsu import DSU

THRESHOLD = 1.0
LEV_THRESHOLD = 3

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def standardize(data):
    """
    Cleans input Pandas dataframe and standardizes all relevant fields by using 
    upper case letters and alphanumeric strings only.
    Returns tidied dataframe.
    """
    data = data.loc[:, :"Current Zip Code"]

    # Missing values are replaced with empty string or 0s
    data['First Name'] = data['First Name'].fillna("").str.upper().str.replace('\W', '')
    data['MI'] = data['MI'].fillna("").str.upper().str.replace('\W', '')
    data['Last Name'] = data['Last Name'].fillna("").str.upper().str.replace('\W', '')
    data['Current Street 1'] = data['Current Street 1'].fillna("").str.upper().str.replace('\W', '')
    data['Current Street 2'] = data['Current Street 2'].fillna("").str.upper().str.replace('\W', '')

    # For sex, only keep first character and represent missing Na as "U"
    data['Sex'] = data['Sex'].str.upper().str[0]
    data['Sex'] = data['Sex'].fillna("U")

    # Convert zip code to alphanumeric string or 0
    data['Current Zip Code'] = data['Current Zip Code'].fillna(0).astype(int).astype(str).str[:5]
    data['Current City'] = data['Current City'].fillna("").str.upper().str.replace('\W', '')

    data['Current State'] = data['Current State'].replace(to_replace=states, value=None)
    data['Current State'] = data['Current State'].str.upper().str.replace('\W', '')

    # Standardize date of births, and fill missing values with 0s
    data['Date of Birth'] = pd.to_datetime(data['Date of Birth'], errors='coerce').dt.date
    data['Date of Birth'] = data['Date of Birth'].fillna(0).astype(str)

    return data

def compute_hash(fields):
    """
    Computes partial SHA-1 hashes using salt, birthdate, partial names, sex
    """
    salt = "LAHACKS"
    res = []
    for first, last, date_of_birth, sex in fields:
        h = hashlib.sha1()
        # Partial hashing only uses first 3 chars of names
        partial_first = (first + ("_" * 3))[:3]
        partial_last = (last + ("_" * 3))[:3]
        date_of_birth = (date_of_birth + ("_" * 10))[:10]
        h.update((salt + date_of_birth + "~" + sex + "~" + partial_first + "~" + partial_last + "XXX").encode('utf-8'))
        res.append(h.hexdigest())
    return res

def is_similar(row1, row2):

    rs = RefinedSoundex()
    s = Soundex()

    similarity = 0
    # Heuristics for determining similarity
    if row1["First Name"] and row2["First Name"]:
        if s.sounds_like(row1["First Name"], row2["First Name"]) or \
        rs.distance(row1["First Name"], row2["First Name"], metric='levenshtein') < LEV_THRESHOLD:
            similarity += 0.4
    if row1["Last Name"] and row2["Last Name"]:
        if s.sounds_like(row1["Last Name"], row2["Last Name"]) or \
        rs.distance(row1["Last Name"], row2["Last Name"], metric='levenshtein') < LEV_THRESHOLD:
            similarity += 0.4
        
    if row1["Date of Birth"] and row2["Date of Birth"] and row1["Date of Birth"] != row2["Date of Birth"]:
        similarity -= 0.4
    else:
        similarity += 0.4
        
    if (row1["Sex"] == "M" and row2["Sex"] == "M") or (row1["Sex"] == "F" and row2["Sex"] == "F"):
        similarity += 0.2
    elif (row1["Sex"] == "M" and row2["Sex"] == "F") or (row1["Sex"] == "F" and row2["Sex"] == "M"):
        similarity -= 0.4
        
    if row1["Current Street 1"] and row2["Current Street 1"] and \
    row1["Current Street 1"] == row2["Current Street 1"]:
        similarity += 0.4
    
    if row1["Current Zip Code"] and row2["Current Zip Code"] and \
    row1["Current Zip Code"] == row2["Current Zip Code"]:
        similarity += 0.2
        
    if row1["Current City"] and row2["Current City"] and \
    row1["Current City"] == row2["Current City"]:
        similarity += 0.2
    return similarity > THRESHOLD

if __name__== "__main__":
    """
    usage: python3 run.py input_csv_file
    Load patient matching data as CSV, import into database.
    """

    # assume input file format/schema matches patient_matching_data.csv
    filename = sys.argv[1]

    with open(filename, "r") as f:
        data = pd.read_csv(f)

    engine = db.create_engine('sqlite:///patient_matching.db', echo=False)
    conn = engine.connect()

    # Store original CSV contents in patient_matching database
    print("Loaded initial patient matching data into patients table...")
    data.to_sql("patients", conn, if_exists='replace')

    # Clean up the data
    print("Cleaning up data...")
    data = standardize(data)

    # Compute hash using partial names, DOB, and sex for initial patient grouping
    print("Computing hashes...")
    data['parHash'] = compute_hash(list(zip(data["First Name"], data["Last Name"], data["Date of Birth"], data["Sex"])))


    # Deduplicate by the partial hash, so all accurate records are grouped
    print("Computing hash-based initial grouping...")
    dedupped = data.groupby(["parHash"])
    dedup_by_hash = data.groupby(["parHash"])["PatientID"].apply(list).reset_index(name='patient_ids')
    # Build reference table for dedupped groups and important information
    reference = dedupped.first().reset_index()\
    [["parHash", "First Name", "Last Name", "Date of Birth", "Sex", "Current Street 1", "Current City", "Current State", "Current Zip Code"]] 
    reference = reference.merge(dedup_by_hash)

    # Pairwise deduplication with Similarity Heuristics
    print("Estimating similarity between initial patient grouping...")
    dsu = DSU(len(reference))

    for index1, row1 in reference.iterrows():
        for index2, row2 in reference.iterrows():
            if index1 <= index2:
                break
            else:
                if is_similar(row1, row2):
                    dsu.union(index1, index2)

    print("Making final groupings...")
    # Mapping initial grouping to final groupings
    group_dict = {}
    # Loop through the previous group ids and determine their final groupings
    for group_id in range(len(reference)):
        if dsu.find(group_id) in group_dict:
            group_dict[dsu.find(group_id)].append(group_id)
        else:
            group_dict[dsu.find(group_id)] = [group_id]

    # Loop through the final groupings to get the patients
    counter = 0
    patients_dict = {}
    for final_id, group_ids in group_dict.items():
        patients_dict[counter] = []
        for group_id in group_ids:
            patient_ids = reference.iloc[[group_id]]["patient_ids"].tolist()
            patients_dict[counter] += patient_ids[0]
        counter += 1

    # Map patient ID to final group ID
    patient_to_group = {}
    for i, patients in patients_dict.items():
        for p in patients:
            patient_to_group[p] = i

    original = pd.read_csv("Patient_Matching_Data.csv")

    original["Temp Group ID"] = original["PatientID"].replace(to_replace=patient_to_group)

    # Compare results to original data
    groupings_list = original["Temp Group ID"].tolist()
    renumbering = {}
    counter = 0
    final_groupings = []
    for i in groupings_list:
        if i not in renumbering:
            counter += 1
            renumbering[i] = counter
        final_groupings.append(renumbering[i])
    original.insert(0, 'Final Group ID', final_groupings)

    # Store final groupings in patient_matching database
    original.to_sql("matched_patients", conn, if_exists='replace')
    print("Results are saved to matched_patients table in the database")

    # Output "Post_Patient_Matching_Groups.csv"
    print("Outputting results to Post_Patient_Matching_groups.csv")
    original.to_csv("Post_Patient_Matching_Groups.csv", index=False)

    print("DONE! Thanks for being patient with Patiently!")
