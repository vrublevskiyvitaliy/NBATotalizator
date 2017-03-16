# -*- coding: utf-8 -*-
import requests
import re
import json
from lxml import html

url = 'http://www.betexplorer.com/basketball/usa/nba-2014-2015/results/?stage=ShmZavVI&month=all'
url = 'http://www.betexplorer.com/basketball/usa/nba-2013-2014/results/?stage=4C5vWdeO&month=all'
url = 'http://www.betexplorer.com/basketball/usa/nba-2012-2013/results/?stage=MmxUanEr&month=all'
url = 'http://www.betexplorer.com/basketball/usa/nba-2015-2016/results/?stage=MDLVWKFc&month=all'


def get_data():
    page = requests.get(url)
    tree = html.fromstring(page.content)
    table = tree.xpath('//table')[0]
    list_tr = (html.fromstring(html.tostring(table))).xpath('//tr')

    all_matchs = []

    for tr in list_tr:
        try:
            team_t = (html.fromstring(html.tostring(tr))).xpath('//td')[0]
            f_team = (html.fromstring(html.tostring(team_t))).xpath('//span')[0].text
            s_team = (html.fromstring(html.tostring(team_t))).xpath('//span')[1].text

            score = (html.fromstring(html.tostring(tr))).xpath('//td')[1]
            score = (html.fromstring(html.tostring(score))).xpath('//a')[0].text

            f_score = score.split(':')[0]
            s_score = score.split(':')[1]

            f_odd = (html.fromstring(html.tostring(tr))).xpath('//td')[2]
            f_odd = re.findall("\d+\.\d+", html.tostring(f_odd))[0]
            f_odd = float(f_odd)

            s_odd = (html.fromstring(html.tostring(tr))).xpath('//td')[3]
            s_odd = re.findall("\d+\.\d+", html.tostring(s_odd))[0]
            s_odd = float(s_odd)

            date = (html.fromstring(html.tostring(tr))).xpath('//td')[4].text

            all_matchs.append({
                'first_team': f_team,
                'second_team': s_team,
                'first_score': int(f_score),
                'second_score': int(s_score),
                'f_odd': f_odd,
                's_odd': s_odd,
                'date': date
            })
        except Exception as e:
            print(e.message)

    with open('data_2015.json', 'w') as outfile:
        json.dump(all_matchs, outfile)


get_data()