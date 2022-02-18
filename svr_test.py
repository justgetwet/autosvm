import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

input_f = "./20220202_isesaki_entry.pickle"
with open(input_f, mode="rb") as f:
    df = pickle.load(f)

# for r in range(1, 13):
#     df = e_df[e_df["race"]==r]
df = df[df["race"]>0]

X = df.iloc[:, 1:-2]
y = df["time"]
y_divtry = X["div-try"]

y_mean = X["mean_race"]


scaler = StandardScaler()
X = scaler.fit_transform(X)

with open("model.pickle", mode="rb") as f:
    model = pickle.load(f)

# print(y.values)
y_pred = model.predict(X)
# print(y_pred)
print(r2_score(y, y_pred))
print(r2_score(y, y_divtry))
print(r2_score(y, y_mean))

ax = plt.figure().gca()
ax.scatter(y_pred, y_pred - y)
ax.scatter(y_divtry, y_divtry - y)
ax.scatter(y_mean, y_mean - y)
ax.hlines(y=0, xmin=3.3, xmax=3.6, color="black")
plt.show()
