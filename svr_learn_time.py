import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV


input_f = "./20220131_isesaki_entry.pickle"
with open(input_f, mode="rb") as f:
    df1 = pickle.load(f)

input_f = "./20220201_isesaki_entry.pickle"
with open(input_f, mode="rb") as f:
    df2 = pickle.load(f)

df = pd.concat([df1, df2])

# print(df)

X = df.iloc[:, 1:-2]
# print(X.head())
y = df["time"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# def gen_cv():
#     m_train = np.floor(len(y_train)*0.75).astype(int)#このキャストをintにしないと後にハマる
#     train_indices = np.arange(m_train)
#     test_indices = np.arange(m_train, len(y_train))
#     yield (train_indices, test_indices)

# m_train = np.floor(len(y_train)*0.75).astype(int)#このキャストをintにしないと後にハマる
# print(len(y_train))
# print(m_train)
# print(np.arange(m_train))
# print(np.arange(m_train, len(y_train)))

# train_idxs = np.arange(m_train)
# test_idxs = np.arange(m_train, len(y_train))

# def gengen():
#     yield (train_idxs, test_idxs)

# print(gengen().__next__())
# print(gengen().__next__())

cnt = 40
params = {"C":np.logspace(-1,0,cnt), "epsilon":np.logspace(-3,0,cnt)}
model = GridSearchCV(SVR(), params, cv=5, scoring="r2", return_train_score=True)
model.fit(X_train, y_train)
print("最適なパラメーター =", model.best_params_)
print("精度 =", model.best_score_)

# cv fold数 = k個のブロックに分ける

# model = SVR(C=0.1128837891, epsilon=0.0, gamma='auto') # 0.78
# model.fit(X_train, y_train)
print(model.score(X_test, y_test))

filename = "model.pickle"
with open(filename, "wb") as f:
    pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)

# 検証曲線
# plt_x, plt_y = np.meshgrid(params["C"], params["epsilon"])
# fig = plt.figure(figsize=(8,8))
# fig.subplots_adjust(hspace = 0.3)
# for i in range(2):
#     if i==0:
#         plt_z = np.array(model.cv_results_["mean_train_score"]).reshape(cnt, cnt, order="F")
#         title = "Train"
#     else:
#         plt_z = np.array(model.cv_results_["mean_test_score"]).reshape(cnt, cnt, order="F")
#         title = "Cross Validation"
#     ax = fig.add_subplot(2, 1, i+1)
#     CS = ax.contour(plt_x, plt_y, plt_z) #, levels=[0.6, 0.65, 0.7, 0.75, 0.8, 0.85])
#     ax.clabel(CS, CS.levels, inline=True)
#     ax.set_xscale("log")
#     ax.set_yscale("log")
#     ax.set_xlabel("C")
#     ax.set_ylabel("epsilon")
#     ax.set_title(title)
# plt.suptitle("Validation curve / Gaussian SVR")
# plt.show()