from model import Model
import pandas as pd

from cleaner import clean_data

train_file = "data/train.csv"

df = pd.read_csv(train_file, dtype=str)
df = df.fillna("")
Z = []
for _, row in df.iterrows():
    z = dict(row)
    z = clean_data(z)
    Z.append(z)
    
m = Model()
m.fit(Z)
m.save("models/model.joblib")
