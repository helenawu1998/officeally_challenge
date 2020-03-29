import sys
import pandas as pd
import sqlalchemy as db

if __name__== "__main__":
    """
    usage: python3 run.py
    Run patient matching on database
    """

    # Make sure to run set_up.py to load patient matching CSV
    engine = db.create_engine('sqlite:///patient_matching.db', echo=False)
    conn = engine.connect()

    metadata = db.MetaData()
    data = db.Table('patients', metadata, autoload=True, autoload_with=engine)

    print(data.columns.keys())

    query = db.select([data])
    print(query)
    ResultProxy = conn.execute(query)
    ResultSet = ResultProxy.fetchall()
    print(ResultSet)