ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import requests

url = "https://autorace.jp/netstadium/Ranking/Rank/All/"

df = pd.DataFrame()
for rank in ["S", "A", "B"]:
    res = requests.get(url + rank, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    dfs = pd.io.html.read_html(soup.prettify())
    if df.empty:
        df = dfs[5]
    else:
        df = pd.concat([df, dfs[5]])
        
df.iloc[0:3, 0] = [1.0, 2.0, 3.0]
with open("ranking.pickle", "wb") as f:
    pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
