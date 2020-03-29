from model import Model
import pandas as pd

train_file = "data/train.csv"

df = pd.read_csv(train_file, dtype=str)
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
