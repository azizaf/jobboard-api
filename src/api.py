import json

from bson.json_util import dumps
from fastapi import FastAPI
from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client.jobboard

app = FastAPI()
jobs_collection = db.jobs_collection

@app.get("/jobs")
def jobs():
    data = [ json.loads(dumps(job)) for job in jobs_collection.find({}, {"_id":0, "title":1, "pubDate":1, "link":1})]
    return data
