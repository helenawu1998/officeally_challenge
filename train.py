from model import Model
import pandas as pd

df = pd.read_csv("data/data.csv", dtype=str)
df = df.fillna("")
Z = []
for _, row in df.iterrows():
    z = dict(row)
    z["Current Street"] = z["Current Street 1"] + " " + z["Current Street 2"]
    z["Previous Street"] = z["Previous Street 1"] + " " + z["Previous Street 2"]
    Z.append(z)
m = Model()
m.fit(Z)
