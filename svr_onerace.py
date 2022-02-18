ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import pickle
import requests
import time

url_oddspark = "https://www.oddspark.com/autorace"

placeCd_d = {'川口': '02', '伊勢崎': '03', '浜松': '04', '飯塚': '05', '山陽': '06'}
placeEn_d = {'川口': 'kawaguchi', '伊勢崎': 'isesaki', '浜松': 'hamamatsu',\
            '飯塚': 'iiduka', '山陽': 'sanyo'}

def get_dfs(url):
    res = requests.get(url, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    dfs = []
    if soup.find("table"):
        dfs = pd.io.html.read_html(soup.prettify())
    else:
        print(f"it's no table! {url}")
    return dfs

def onerace(dt, place, raceNo):

    place_cd = placeCd_d[place]
    race_url = f"raceDy={dt}&placeCd={place_cd}&raceNo={raceNo}"

    entry_url = url_oddspark + "/RaceList.do?" + race_url

    win_place_url = url_oddspark + "/Odds.do?" + race_url + f"&betType={'1'}&viewType={'0'}"
    quinella_url = url_oddspark + "/Odds.do?" + race_url + f"&betType={'6'}&viewType={'0'}"
    exacta_url = url_oddspark + "/Odds.do?" + race_url + f"&betType={'5'}&viewType={'0'}"
    wide_url = url_oddspark + "/Odds.do?" + race_url + f"&betType={'7'}&viewType={'0'}"
    trio_url = url_oddspark + "/Odds.do?" + race_url + f"&betType={'9'}&viewType={'0'}" 
    odds_urls = [win_place_url, quinella_url, exacta_url, wide_url, trio_url]
    
    trifecta_url = url_oddspark + "/Odds.do?" + race_url + f"viewType={'0'}&betType={'8'}"

    result_url = url_oddspark + "/RaceResult.do?" + race_url

    dfs = get_dfs(entry_url)
    if dfs:
        entry_df = dfs[-1]
        bikes = list(map(lambda x: str(x), range(1, len(entry_df)+1)))
    else:
        print("no entry!")
        return []
    
    odds = []
    for url in odds_urls:
        dfs = get_dfs(url)
        odds.append(dfs)

    trifectas = []
    for bike in bikes:
        trifecta_bike_url = trifecta_url + f"bikeNo={bike}jikuNo={'1'}"
        dfs = get_dfs(trifecta_bike_url)
        trifectas.append(dfs)
    
    result_dfs = get_dfs(result_url)

    return [entry_df, odds, trifectas, result_dfs]

if __name__ == '__main__':

    dt = "20220202"
    place = "伊勢崎"
    raceNo = 1

    res = onerace(dt, place, raceNo)
    print(res[0])