import sys
import pandas as pd
import sqlalchemy as db

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
    Takes pandas dataframe and standardizes all relevant fields.
    """
    data = data.loc[:, :"Current Zip Code"]

    # Standardize data by using all upper case letters
    # Retain only alphanumerics in strings
    data['First Name'] = data['First Name'].str.upper().str.replace('\W', '')
    data['MI'] = data['MI'].str.upper().str.replace('\W', '')
    data['Last Name'] = data['Last Name'].str.upper().str.replace('\W', '')
    data['Current Street 1'] = data['Current Street 1'].str.upper().str.replace('\W', '')
    data['Current Street 2'] = data['Current Street 2'].str.upper().str.replace('\W', '')
    # For sex, only keep first character, replace NaN with U?
    data['Sex'] = data['Sex'].str.upper().str[0]
    # data['Sex'] = data['Sex'].fillna("U")
    # Replace NaN with 0, and convert to alphanumeric string
    data['Current Zip Code'] = data['Current Zip Code'].fillna(0).astype(int).astype(str).str[:5]
    data['Current City'] = data['Current City'].str.upper().str.replace('\W', '')

    # Standardize the states by turning abbreviations into strings
    data['Current State'] = data['Current State'].replace(to_replace=states, value=None)
    data['Current State'] = data['Current State'].str.upper().str.replace('\W', '')

    # Standardize date of births
    data['Date of Birth'] = pd.to_datetime(data['Date of Birth'], errors='coerce')
    return data

if __name__== "__main__":
    """
    usage: python3 set_up.py input_csv_file
    Load patient matching data as CSV, import into database.
    """

    # assume input file format/schema matches patient_matching_data.csv
    filename = sys.argv[1]

    with open(filename, "r") as f:
        data = pd.read_csv(f)

    engine = db.create_engine('sqlite:///patient_matching.db', echo=False)
    conn = engine.connect()

    # Store CSV contents in patient_matching database
    data.to_sql("patients", conn, if_exists='replace')

    tidy_data = standardize(data)
    # Store tidied data in patient_matching database
    tidy_data.to_sql("tidy_patients", conn, if_exists='replace')
