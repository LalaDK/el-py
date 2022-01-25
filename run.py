#!/usr/bin/env python3

# https://python.readthedocs.io/en/v2.7.2/howto/curses.html

from db import save_document, search_documents

import requests
import json
import csv
import sys
from datetime import datetime
from rich.progress import track
from rich import print
import plotext as plt
import os
import pytz
os.system('cls' if os.name == 'nt' else 'clear')

aftalenr = "1343950"
fra = datetime.now().replace(year=2021, hour=23, minute=00, second=00, microsecond=0).isoformat() + 'Z'
til = datetime.now().replace(hour=23, minute=00, second=00, microsecond=0).isoformat() + 'Z'
email = "mads.eckardt@gmail.com"
password = "ZxmBYN3CX<Y[iW!N?Gpv"

cookieJar = None
status_idx = 0

def print_status(value):
    global status_idx
    status_idx = status_idx + 1
    print("[bold][red][ [white]" + str(status_idx) + "[red] ][white] " + value)

if(len(sys.argv) > 1 and sys.argv[1] == 'refresh'):
    print_status("Fetching cookies")
    req = requests.get("https://www.ok.dk/")
    cookieJar = req.cookies

    data = json.dumps({ "values": { "email": "mads.eckardt@gmail.com", "password": "ZxmBYN3CX<Y[iW!N?Gpv", "persists": "true" } })
    headers = { "Content-Type": "application/json", "Content-Length": str(len(data)) }

    print_status("Authenticating")
    req = requests.post("https://www.ok.dk/min-ok-forside/login/authenticate", cookies=cookieJar, data=data, headers=headers)
    cookieJar = req.cookies

    print_status("Fetching data")
    print(f'https://www.ok.dk/min-ok-forside/el-overblik/forbrug/downloadrawdata?aftalenr={aftalenr}&fra={fra}&til={til}')
    req = requests.post(f'https://www.ok.dk/min-ok-forside/el-overblik/forbrug/downloadrawdata?aftalenr={aftalenr}&fra={fra}&til={til}', cookies=cookieJar)

    print_status("Preparing data")
    csv_data = req.text.replace("\"\"", '').replace('=', '')
    csv_data = csv_data.split("\n")
    csv_data = "\n".join(csv_data[1:]).splitlines()

    print_status("Parsing CSV data")
    reader = csv.reader(csv_data, delimiter=';', quotechar='"')
    lines_num = len(csv_data)

    for line in track(range(lines_num), description="Processing..."):
        row = next(reader);
        from_datetime = datetime.strptime(row[0], "%d-%m-%Y %H:%M")
        to_datetime = datetime.strptime(row[1], "%d-%m-%Y %H:%M")
        kwh = float(row[2].replace(',', '.'))
        save_document(from_datetime, to_datetime, kwh)


arr = search_documents(datetime(2022, 1, 1), datetime(2022, 1, 30))
print(arr)
#
# os.system('cls' if os.name == 'nt' else 'clear')
#
# def to_d(x):
#     plt.datetime.set_datetime_form(date_form='%H:%M')
#     t = datetime.fromtimestamp(int(x.get('from_datetime')))
#     return plt.datetime.datetime_to_string(t)
#
#
# names = list(map(lambda x : to_d(x), arr))
# values = list(map(lambda x : x.get('kwh'), arr))
# plt.bar(names, values, width = 0.3)
# plt.grid(0, 1)
# plt.ylim(0, 4)
# plt.title("Strømforbrug")
# plt.clc() # to remove colors
# plt.xlabel("Tidspunkt")
# plt.ylabel("kWh")
# plt.show()
