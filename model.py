from sklearn.linear_model import LogisticRegression
import itertools
import numpy as np


def placeholder(s1, s2):
    return 1 if len(s1) == len(s2) else 0


GROUND_TRUTH = "GroupID"

FIELDS = [
    ("Patient Acct #", False, placeholder),
    ("First Name", True, placeholder),
    ("MI", True, placeholder),
    ("Last Name", True, placeholder),
    ("Date of Birth", False, placeholder),
    ("Sex", False, placeholder),
    ("Street", True, placeholder),
    ("City", True, placeholder),
    ("State", True, placeholder),
    ("Zip Code", True, placeholder),
]


def get_versions(field):
    ans = {
        "Patient Acct #": ["Patient Acct #"],
        "Date of Birth": ["Date of Birth"],
        "Sex": ["Sex"],
        "First Name": ["First Name", "Previous First Name"],
        "MI": ["MI", "Previous MI"],
        "Last Name": ["Last Name", "Previous Last Name"],
        "Street": ["Current Street", "Previous Street"],
        "City": ["Current City", "Previous City"],
        "State": ["Current State", "Previous State"],
        "Zip Code": ["Current Zip Code", "Previous Zip Code"],
    }
    return ans[field]


def _is_match(z1, z2):
    """Given two dictionaries with ground truth group ID, return whether its
    a match.
    """
    return z1[GROUND_TRUTH] == z2[GROUND_TRUTH]


def _similarity(w1, w2):
    """Given two dictionaries representing patients, compute the similarity
    vector.
    """
    v = np.zeros(len(FIELDS))
    for i, (field, _, fn) in enumerate(FIELDS):
        f1 = [w1[x] for x in get_versions(field)]
        f2 = [w2[x] for x in get_versions(field)]
        for x1, x2 in itertools.product(f1, f2):
            v[i] = max(v[i], fn(x1, x2))
    return v


class Model:
    def __init__(self):
        self.clf = LogisticRegression(random_state=0)

    def fit(self, Z):
        X, y = [], []
        for z1, z2 in itertools.product(Z, repeat=2):
            X.append(_similarity(z1, z2))
            y.append(_is_match(z1, z2))
        self.clf.fit(X, y)

    def predict(self, w1, w2):
        return self.clf.predict(_similarity(w1, w2).reshape(1, -1))[0]


import random

Z = []
for _ in range(10):
    z = {}
    for f, _, _ in FIELDS:
        for x in get_versions(f):
            z[x] = random.choice(["bob", "alice", "smokey"])
    z["GroupID"] = random.choice([1, 2, 3])
    Z.append(z)

m = Model()
m.fit(Z)
