from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

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
