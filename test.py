import pandas as pd
import numpy as np

from model import Model, _is_match, _similarity, FIELDS, get_versions


def debug_print(z1, z2, similarity):
    for i, (field, _) in enumerate(FIELDS):
        f1 = [z1[x] for x in get_versions(field)]
        f2 = [z2[x] for x in get_versions(field)]
        case = "error"
        if np.array_equal(similarity[i], [1, 0, 0]):
            case = "match"
        elif np.array_equal(similarity[i], [0, 1, 0]):
            case = "nomatch"
        elif np.array_equal(similarity[i], [0, 0, 1]):
            case = "missing"
        print(f"\tField: {field}")
        print(f"\t\t{case}")
        for x1 in f1:
            if x1:
                print(f"\t\tversion for patient 1: {x1}")
        for x2 in f2:
            if x2:
                print(f"\t\tversion for patient 2: {x2}")


val_file = "data/val.csv"
model_file = "models/model.joblib"

df = pd.read_csv(val_file, dtype=str)
df = df.fillna("")
Z = []
for _, row in df.iterrows():
    z = dict(row)
    z["Current Street"] = z["Current Street 1"] + " " + z["Current Street 2"]
    z["Previous Street"] = z["Previous Street 1"] + " " + z["Previous Street 2"]
    Z.append(z)

m = Model()
m.load(model_file)

res = []
for i in range(len(Z)):
    for j in range(i + 1, len(Z)):
        pred = m.predict(Z[i], Z[j])
        truth = _is_match(Z[i], Z[j])
        if pred == True and truth == False:
            print("=====================False positive=====================")
            print(f"Predicted probability {m.predict_proba(Z[i], Z[j])}")
            debug_print(Z[i], Z[j], (_similarity(Z[i], Z[j]).reshape(-1, 3)))
        if pred == False and truth == True:
            print("=====================False negative=====================")
            print(f"Predicted probability {m.predict_proba(Z[i], Z[j])}")
            debug_print(Z[i], Z[j], (_similarity(Z[i], Z[j]).reshape(-1, 3)))
        res.append([pred, truth])
res = np.array(res)

true_pos = len(res[(res[:, 0] == True) & (res[:, 1] == True)])
true_neg = len(res[(res[:, 0] == False) & (res[:, 1] == False)])
false_pos = len(res[(res[:, 0] == True) & (res[:, 1] == False)])
false_neg = len(res[(res[:, 0] == False) & (res[:, 1] == True)])

precision = true_pos / (true_pos + false_pos)
recall = true_pos / (true_pos + false_neg)
f1 = 2 / (1 / precision + 1 / recall)

print(f"Precision {precision}, recall {recall}, F1 {f1}")

print(f"True pos {true_pos}")
print(f"True neg {true_neg}")
print(f"False pos {false_pos}")
print(f"False neg {false_neg}")
