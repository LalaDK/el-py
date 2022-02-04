from tinydb import TinyDB, Query
from rich.progress import track
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from datetime import datetime
import csv


serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
db = TinyDB('db.json', storage=serialization)


def save_document(from_datetime, to_datetime, kwh):
    query = Query()
    if(len(db.search(query.from_datetime == from_datetime.timestamp() and query.to_datetime == to_datetime.timestamp())) == 0):
        doc = {
            'from_datetime': from_datetime.timestamp(),
            'to_datetime': to_datetime.timestamp(),
            'kwh': kwh
        }
        db.insert(doc)


def search_documents(from_datetime, to_datetime):
    query = Query()
    return db.search(query.from_datetime >= from_datetime.timestamp() and query.from_datetime <= to_datetime.timestamp())


def save_csv(csv_data):
    csv_data = csv_data.replace("\"\"", '').replace('=', '')
    csv_data = csv_data.split("\n")
    csv_data = "\n".join(csv_data[1:]).splitlines()

    reader = csv.reader(csv_data, delimiter=';', quotechar='"')
    lines_num = len(csv_data)
    description = "Saving " + str(lines_num) + " entries to database..."

    for line in track(range(lines_num), description=description):
        row = next(reader)
        from_datetime = datetime.strptime(row[0], "%d-%m-%Y %H:%M")
        to_datetime = datetime.strptime(row[1], "%d-%m-%Y %H:%M")
        kwh = float(row[2].replace(',', '.'))
        save_document(from_datetime, to_datetime, kwh)


def last_datetime():
    data = db.all()
    if len(data):
        last = sorted(data, key=lambda x: x['to_datetime'], reverse=True)[0]
        if last:
            return datetime.fromtimestamp(last['to_datetime'])
