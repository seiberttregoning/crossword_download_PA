#!/usr/bin/python3.8
# coding: utf-8


from datetime import datetime, timedelta
from bs4 import BeautifulSoup as soup
import csv
import requests
import sqlite3

login_url = ''
leaders_url = 'https://www.nytimes.com/puzzles/leaderboards'
username = ''
password = ''


players = ['Seibert', 'dirk orozco', 'Joshtreg', 'E-thousand']

with open('/home/Seibert/CrosswordPage/cookie.txt') as f:
    cookie = f.readlines()[0]

# Cookie manually added

# def login(username, password):
#     login_resp = requests.post(login_url, data = {'login': username,
#                                             'password': password},
#                                     headers = {'User-Agent': 'Mozilla/5.0',
#                                                'client_id': 'ios.crosswords'})
#     login_resp.raise_for_status()
#     for cookie in login_resp.json()['data']['cookies']:
#         if cookie['name'] == 'NYT-S':
#             return cookie['cipheredValue']
#     raise ValueError('NYT-S cookie not found')

conn = sqlite3.connect('/home/Seibert/CrosswordPage/db.sqlite3')

cur = conn.cursor()


def get_mini_times(cookie, output):
    response = requests.get(leaders_url, cookies={'NYT-S': cookie})
    page = soup(response.content, features='html.parser')
    solvers = page.find_all('div', class_='lbd-score')
    current_datetime = datetime.now()
    month = str(current_datetime.strftime("%m"))
    day = str(current_datetime.strftime("%d"))
    year = str(current_datetime.strftime("%Y"))
    daytimes = []
    # print('--------------------------')
    # print("Mini Times for " + month + '-' + day + '-' + year)
    for solver in solvers:
        name = solver.find('p', class_='lbd-score__name').text.strip()
        try:
            time = solver.find('p', class_='lbd-score__time').text.strip()
        except:
            time = "--"
        if name.endswith("(you)"):
            name_split = name.split()
            name = name_split[0]
        if name in players:
            if time == '--':
                time = ''
                seconds = 'NULL'
                milliseconds = 'NULL'
            else:
                t = datetime.strptime(time, "%M:%S")
                delta = timedelta(
                    hours=t.hour, minutes=t.minute, seconds=t.second)
                seconds = round(delta.total_seconds())
                milliseconds = round(seconds * 1e6)
            daytimes.append(
                [month, day, year, f'{year}-{month}-{day}', name, time, seconds])
            new_solve_SQL = f"INSERT INTO graph_solve(solve_Month,solve_Day,solve_Year,solve_Date,solve_Player,solve_Time,solve_Seconds) VALUES ({month},{day},{year},'{year}-{month}-{day}','{name}',{milliseconds},{seconds})"
            cur.execute(new_solve_SQL)
            conn.commit()
            # print(new_solve_SQL)
    with open(output, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(daytimes)


if (datetime.now().weekday() in [0, 1, 2, 3, 4]):
    if datetime.now().hour == 20:
        get_mini_times(
            cookie, '/home/Seibert/CrosswordPage/mini_data.csv')
    else:
        pass
else:
    if datetime.now().hour == 16:
        get_mini_times(
            cookie, '/home/Seibert/CrosswordPage/mini_data.csv')
    else:
        pass
