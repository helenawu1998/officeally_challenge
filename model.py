from sklearn.linear_model import LogisticRegression
import itertools
import numpy as np
from comparer import PMD

pmd = PMD()
compare_funs = pmd.get_compare_fun()

import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def placeholder(s1, s2):
    return 1 if len(s1) == len(s2) else 0


FIELDS = [
    "Patient Acct #",
    "First Name",
    "MI",
    "Last Name",
    "Date of Birth",
    "Sex",
    "Street",
    "City",
    "State",
    "Zip Code",
]

FIELDS = [(f, compare_funs[f]) for f in FIELDS]
GROUND_TRUTH = "GroupID"


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


def cmax(x1, x2):
    assert x1.shape == (3,), "Assuming we have 3 cases (match, not match, missing)"
    assert x2.shape == (3,), "Assuming we have 3 cases (match, not match, missing)"
    for z in np.eye(3, dtype=int):
        if np.array_equal(x1, z) or np.array_equal(x2, z):
            return z
    assert False, "Should never get to this point"


def _similarity(w1, w2):
    """Given two dictionaries representing patients, compute the similarity
    matrix. Dimensions = #FIELDS x 3. Returns as a flattened array (1-hot trick)
    """
    v = np.zeros((len(FIELDS), 3), dtype=int)
    for i, (field, fn) in enumerate(FIELDS):
        f1 = [w1[x] for x in get_versions(field)]
        f2 = [w2[x] for x in get_versions(field)]
        for x1, x2 in itertools.product(f1, f2):
            v[i] = cmax(v[i], np.array(fn(x1, x2)))
    return v.flatten()


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
    for f, _ in FIELDS:
        for x in get_versions(f):
            z[x] = random.choice(["bob", "alice", "smokey"])
    z["GroupID"] = random.choice([1, 2, 3])
    Z.append(z)

m = Model()
m.fit(Z)
