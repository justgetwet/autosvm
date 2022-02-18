import pandas as pd
import pickle
import re


input_f = "./20220203_hamamatsu_data.pickle"
with open(input_f, mode="rb") as f:
    race_data = pickle.load(f)

with open('ranking.pickle', mode='rb') as f:
    ranking_df = pickle.load(f)
    ranking_d = dict(zip(ranking_df["現行ランク"], ranking_df["順位"]))

oneday_data = []
for race in range(len(race_data)):

# race = 2
    entry_df = race_data[race][0]
    result_df = race_data[race][3][0]

    rank_d = {"S": [1,0], "A": [0,1], "B": [0,0]}
    time_d = dict(zip(result_df["車"], result_df["競走タイム"]))
    st_d = dict(zip(result_df["車"], result_df["ST"]))

    f = lambda x: float(re.sub("：|%", "", x))/100 # 連対率、3着内率の変換

    onerace_data = []
    for bike in range(len(entry_df)):
        racer = entry_df.iloc[bike,:].values
        if not racer[3].split()[1] == "-" and len(racer[4].split()) == 3:
            data = []
            data += [race+1, racer[0]]
            # print(data)
            racer3 = racer[3].split() # handicap, trial-time,  dev-trial
            data += [float(racer3[0].strip("m")), float(racer3[1]), (float(racer3[1])+float(racer3[2]))]
            rank, pre_rank, point = racer[4].split()
            data += rank_d[rank[0]] # rank
            data += [ranking_d[rank], float(point)] # order in all rank, point
            data += [float(x) for x in racer[5].split()] # mean of trail, mean of race, max of race
            st, _, quin, _, trio = racer[6].split()[1:6]
            data += [float(st), f(quin), f(trio)] # mean of st, rate of quin, rage of trio
            pr = [float(re.sub("m|着", "", x)) for x in racer[8].split()[3:6]] # pre race
            data += [pr[0], pr[1], pr[2]]
            data += [time_d[racer[0]], st_d[racer[0]]]
            onerace_data.append(data)
    oneday_data += onerace_data

# print(oneday_data)

col = ["race", "bike", "handi", "trial", "div-try", "rankS", "rankA", "order", "point"]
col += ["mean_trial", "mean_race", "max_race", "mean_st", "quin", "trio"]
col += ["p-handi", "p-order", "p-time", "time", "ST"]

df = pd.DataFrame(oneday_data, columns=col)
print(df.head())

filename = "_".join(input_f.split("_")[:2]) + "_entry.pickle"
with open(filename, "wb") as f:
    pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)