import json

from bson.json_util import dumps
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client.jobboard

app = FastAPI()
jobs_collection = db.jobs_collection

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs")
def jobs():
    data = [ json.loads(dumps(job)) for job in jobs_collection.find({}, {"_id":0, "description":0})]
    return data
