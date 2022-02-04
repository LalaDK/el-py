#!/usr/bin/env python3

from db import search_documents, save_csv, last_datetime
from ok_api import initialize, authorize, fetchData
from utils import clear
from datetime import datetime
from q import Q
import cowsay
import time
aftalenr = "1343950"
email = "mads.eckardt@gmail.com"
password = "ZxmBYN3CX<Y[iW!N?Gpv"


def main_menu():
    clear()
    options = [
        "Vis data",
        "Hent data",
        "Afslut"
    ]

    answer = Q.ask("OK Data Downloader", options)
    if answer == 0:
        print(options[answer])
    elif answer == 1:
        fetch_menu()
    elif answer == 2:
        print(options[answer])


def fetch_menu():
    clear()
    options = [
        "Hent seneste data",
        "Hent alt data",
        "Tilbage..."
    ]

    answer = Q.ask("Hvilke data skal hentes?", options)
    if answer == 0:
        fetchLatest()
        main_menu()
    elif answer == 1:
        fetchAll()
        main_menu()
    elif answer == 2:
        main_menu()


def fetchLatest():
    last_request = last_datetime()
    if last_request is None:
        last_request = datetime.now().replace(year=1970)
    fetch_between(last_request, datetime.now())


def fetchAll():
    from_datetime = datetime.now().replace(year=1970)
    to_datetime = datetime.now()
    fetch_between(from_datetime, to_datetime)


def fetch_between(from_datetime, to_datetime):
    from_datetime = from_datetime.isoformat()
    to_datetime = to_datetime.isoformat()

    initialize()
    authorize(email, password)
    csv_data = fetchData(aftalenr, from_datetime, to_datetime)
    save_csv(csv_data)
    main_menu()


main_menu()
#arr = search_documents(datetime(2022, 1, 1), datetime(2022, 1, 30))
