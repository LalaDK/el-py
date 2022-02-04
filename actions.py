from datetime import datetime
from db import search_documents, save_csv, last_datetime
from ok_api import initialize, authorize, fetchData
from credentials import email, password, aftalenr


def show_latest():
    #arr = search_documents(datetime(2022, 1, 1), datetime(2022, 1, 30))
    pass


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
    authorize(email(), password())
    csv_data = fetchData(aftalenr(), from_datetime, to_datetime)
    save_csv(csv_data)
