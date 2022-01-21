#!/usr/bin/env python3
from db import save_line
import requests
import json
import csv
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
db = TinyDB('db.json', storage=serialization)

save_line("", "", "")

aftalenr = "1343950"
fra = "2021-01-01T23:00:00.000Z"
til = "2022-12-31T23:00:00.000Z"
email = "mads.eckardt@gmail.com"
password = "ZxmBYN3CX<Y[iW!N?Gpv"

cookieJar = None


if(len(sys.argv) > 1 and sys.argv[1] == 'refresh'):
    print("Fetching cookies ...")
    req = requests.get("https://www.ok.dk/")
    cookieJar = req.cookies

    data = json.dumps({ "values": { "email": "mads.eckardt@gmail.com", "password": "ZxmBYN3CX<Y[iW!N?Gpv", "persists": "true" } })
    headers = { "Content-Type": "application/json", "Content-Length": str(len(data)) }

    print("Authenticating ...")
    req = requests.post("https://www.ok.dk/min-ok-forside/login/authenticate", cookies=cookieJar, data=data, headers=headers)
    cookieJar = req.cookies

    print("Fetching data ...")
    req = requests.post("https://www.ok.dk/min-ok-forside/el-overblik/forbrug/downloadrawdata?aftalenr=1343950&fra=2021-01-01T00:00:00.000Z&til=2022-12-31T23:00:00.000Z", cookies=cookieJar)

    print("Preparing data ...")
    csv_data = req.text.replace("\"\"", '').replace('=', '')
    csv_data = csv_data.split("\n")
    csv_data = "\n".join(csv_data[1:]).splitlines()

    print("Parsing CSV data ...")
    reader = csv.reader(csv_data, delimiter=';', quotechar='"')
    lines_num = len(csv_data)

    for idx, row in enumerate(reader):
        print(str(idx) + " / " + str(lines_num), end="\r", flush=True)

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

print("")

#     names.append(r.from_datetime.strftime('%H'))
#     values.append(r.kwh)
#
#
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# ax.bar(names, values)
# #plt.plot(names, values)
# plt.show()
