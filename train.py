from model import Model
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="LA Hacks 2020 Patient Matching training")
parser.add_argument(
    "--data",
    dest="data_file",
    type=str,
    help="Training csv file (with ground-truth GroupIDs)",
    required=True,
)
args = parser.parse_args()

df = pd.read_csv(args.data_file, dtype=str)
df = df.fillna("")
Z = []
for _, row in df.iterrows():
    z = dict(row)
    z["Current Street"] = z["Current Street 1"] + " " + z["Current Street 2"]
    z["Previous Street"] = z["Previous Street 1"] + " " + z["Previous Street 2"]
    Z.append(z)
m = Model()
m.fit(Z)
m.save("models/model.joblib")
