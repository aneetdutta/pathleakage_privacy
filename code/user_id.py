from pymongo import MongoClient
from modules.mongofn import MongoDB
from pymongo.errors import BulkWriteError
# Connect to MongoDB

md: MongoDB = MongoDB()
md.set_collection("sniffed_data")
# Define the pipeline for aggregation
pipeline = [
    {
        '$group': {
            '_id': '$user_id',
            "lte_ids": {"$addToSet": "$lte_id"},
            "bluetooth_ids": {"$addToSet": "$bluetooth_id"},
            "wifi_ids": {"$addToSet": "$WiFi_id"}
        }
    },
    {
        '$project': {
            'user_id': '$_id',
            '_id': 0,
            'lte_ids': 1,
            'bluetooth_ids': 1,
            'wifi_ids': 1,
            "ids": {
                "$setUnion": ["$lte_ids", "$bluetooth_ids", "$wifi_ids"]
            }
        }
    }
]

# Aggregate data
result = md.collection.aggregate(pipeline)
 
# Create a new collection and insert the aggregated data
md.db["userid"].insert_many(result)