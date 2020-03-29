import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm

from model import Model
from cleaner import clean_data


class DSU:
    """Disjoint-set data structure for maintaining sets of patient records.
    """

    def __init__(self, n):
        """
        Initialize DSU for an n element universe.
        """
        self.fa = [x for x in range(n)]

    def find(self, x):
        """
        Given an element x, return an identifier for the set that x belongs to.
        """
        if x == self.fa[x]:
            return x
        self.fa[x] = self.find(self.fa[x])
        return self.fa[x]

    def union(self, x, y):
        """
        Given two elements x and y, find the two sets containing x and y and
        union them together.
        """
        a = self.find(x)
        b = self.find(y)
        self.fa[b] = a


parser = argparse.ArgumentParser(description="LA Hacks 2020 Patient Matching")
parser.add_argument(
    "--input",
    dest="input_file",
    type=str,
    help="Input csv file (without GroupIDs)",
    required=True,
)
parser.add_argument(
    "--output",
    dest="output_file",
    type=str,
    help="Output csv file (with predicted GroupIDs)",
    required=True,
)
args = parser.parse_args()

model_file = "models/model.joblib"
m = Model()
m.load(model_file)
df = pd.read_csv(args.input_file, dtype=str)
df = df.fillna("")
Z = []
for _, row in df.iterrows():
    z = dict(row)
    z = clean_data(z)
    Z.append(z)

dsu = DSU(len(Z))
for i in tqdm(range(len(Z))):
    for j in range(i + 1, len(Z)):
        pred = m.predict(Z[i], Z[j])
        if pred:
            dsu.union(i, j)

counter = 1
renumber = {}
for i in range(len(Z)):
    z = Z[i]
    if dsu.find(i) not in renumber:
        renumber[dsu.find(i)] = counter
        counter += 1
    z["GroupID"] = renumber[dsu.find(i)]
df = pd.DataFrame(Z)
# Re-order so it looks the same
c = list(df.columns)
c = [c[-1]] + c[:-1]
df = df[c]
df.to_csv(args.output_file, index=False)
