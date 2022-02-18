ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
import requests

siteurl = "https://autorace.jp"
url = siteurl + "/netstadium/Ranking/Rank/All/"

for rank in ["B"]:#, "A", "B"]:
    res = requests.get(url + rank, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    for tag in soup.select("a[href^='/netstadium/Profile/']"):
        racerurl = siteurl + tag.get("href")
        res = requests.get(racerurl, headers=ua)
        soup = BeautifulSoup(res.content, "html.parser")
        name = "".join(soup.h3.text.split()[:2])
        tag = soup.select_one("img[src^='/netstadium/image/photo']")
        src = tag.get("src")
        no = src.split("/")[-1].split(".")[0]
        imgurl = siteurl + src
        r = requests.get(imgurl, headers=ua)
        filename = "./images/" + no + "_" + name + ".jpg"
        print(filename)
        with open(filename, "wb") as f:
            f.write(r.content)