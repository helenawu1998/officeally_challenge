import sys
import pandas as pd
import sqlalchemy as db

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

    data2 = data
