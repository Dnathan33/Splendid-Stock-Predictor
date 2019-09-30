# from pymongo import MongoClient
from pymongo import MongoClient
import json
from bson import json_util, objectid
from .algorithm import get_data
import requests

def connect_monogo():
    client = MongoClient("mongodb+srv://<url>")
    database = client.get_database('HackUMBC19')
    return database

# Retrives Stock data
def get_predections(url, stock):
    db = connect_monogo()
    Predection_collection = db["Stock-data"]
    data = Predection_collection.find_one({"name":stock})
    Predection_collection.ex
    return json.loads(json_util.dumps(data))

# Adds Stock data to Monogodb
def add_document(url):
    # https://www.quandl.com/api/v3/datasets/EOD/MSFT.csv
    csvext = url.split('/')
    filename = csvext[len(csvext)-1].strip()
    filename = filename.split('.')
    filename = filename[0]

    API_KEY = '?api_key=<key>'
    db = connect_monogo()
    print("HERE 1", filename)
    Predection_collection = db["Prediction"]
    url = url + API_KEY
    data = get_data(url)
    Predection_collection.insert_one({filename: list(data)})



