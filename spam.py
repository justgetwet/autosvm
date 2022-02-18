import pandas as pd
import pickle


input_f = "./20220131_isesaki_entry.pickle"
with open(input_f, mode="rb") as f:
    df1 = pickle.load(f)

input_f = "./20220201_isesaki_entry.pickle"
with open(input_f, mode="rb") as f:
    df2 = pickle.load(f)

df = pd.concat([df1, df2])

print(df)