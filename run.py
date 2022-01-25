#!/usr/bin/env python3
from db import save_line
import requests
import json
import csv
import sys

from datetime import datetime
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from rich.progress import track
from rich import print
import plotext as plt
import os
os.system('cls' if os.name == 'nt' else 'clear')

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
db = TinyDB('db.json', storage=serialization)

aftalenr = "1343950"
fra = "2021-01-01T23:00:00.000Z"
til = "2022-12-31T23:00:00.000Z"
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
    req = requests.post("https://www.ok.dk/min-ok-forside/el-overblik/forbrug/downloadrawdata?aftalenr=1343950&fra=2021-01-01T00:00:00.000Z&til=2022-12-31T23:00:00.000Z", cookies=cookieJar)

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
        query = Query()
        if(len(db.search(query.from_datetime == from_datetime.timestamp() and query.to_datetime == to_datetime.timestamp())) == 0):
            doc = {
                'from_datetime': from_datetime.timestamp(),
                'to_datetime': to_datetime.timestamp(),
                'kwh': kwh
            }
            db.insert(doc)

query = Query()
arr = db.search(query.from_datetime > datetime(2022, 1, 15).timestamp())

names = list(map(lambda x : plt.datetime.datetime_to_string(datetime(x.get('from_datetime')).iso()), arr))
values = list(map(lambda x : x.get('kwh'), arr))
print(names)
plt.bar(names, values, width = 0.3) # or shorter orientation = 'h'
plt.title("Most Favoured Pizzas in the World")
plt.clc() # to remove colors
#plt.plotsize(100, 2 * len(names) - 1 + 4) # 4 = 1 for x numerical ticks + 2 for x axes + 1 for title
plt.show()

#pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
#percentages = [14, 36, 11, 8, 7, 4]

# plt.bar(pizzas, percentages, orientation = "horizontal", width = 0.3) # or shorter orientation = 'h'
# plt.title("Most Favoured Pizzas in the World")
# plt.clc() # to remove colors
# plt.plotsize(100, 2 * len(pizzas) - 1 + 4) # 4 = 1 for x numerical ticks + 2 for x axes + 1 for title
# plt.show()
