from modules.device import Device
from modules.devicemanager import DeviceManager
from services.general import *
from services.tracking_algorithm import tracking_algorithm
from modules.mongofn import MongoDB
import json
from collections import defaultdict
from pprint import pprint
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()
md.set_collection("sniffed_data")
pipeline = [
    {
        "$group": {
            "_id": {"timestep": "$timestep", "user_id": "$user_id", "location": "$location"},
            "lte_ids": {"$addToSet": {"$cond": [{"$ne": ["$lte_id", "None"]}, "$lte_id", None]}},
            "wifi_ids": {"$addToSet": {"$cond": [{"$ne": ["$WiFi_id", "None"]}, "$WiFi_id", None]}},
            "bluetooth_ids": {"$addToSet": {"$cond": [{"$ne": ["$bluetooth_id", "None"]}, "$bluetooth_id", None]}},
        }
    },
    {
        "$project": {
            "_id": 0,
            "timestep": "$_id.timestep",
            "user_id": "$_id.user_id",
            "lte_id": {"$arrayElemAt": ["$lte_ids", 0]},
            "wifi_id": {"$arrayElemAt": ["$wifi_ids", 0]},
            "bluetooth_id": {"$arrayElemAt": ["$bluetooth_ids", 0]},
            "location": "$_id.location"
        }
    },
    {
        "$group": {
            "_id": "$timestep",
            "user_data": {
                "$push": {
                    "user_id": "$user_id",
                    "lte_id": "$lte_id",
                    "wifi_id": "$wifi_id",
                    "bluetooth_id": "$bluetooth_id",
                    "location": "$location"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "timestep": "$_id",
            "user_data": 1
        }
    }
]

results = md.collection.aggregate(pipeline)
user_location: dict[list] = {}
for result in results:
    timestep, user_data = result["timestep"], result['user_data']
    for user in user_data:
        if "WiFi_id" not in user and "bluetooth_id" not in user and "lte_id" in user:
            user_id = user["user_id"]
            if user_id in user_location:
                user_location[user_id].append([timestep,user["location"]])
            else:
                user_location[user_id] = [[timestep,user["location"]]]
with open("user_location.json", "w") as f:
    json.dump(user_location, f)


user_location = extract_orjson("user_location.json")
sniffer_locations = []
# for users, location_data in user_location.items():
locations = process_dict(user_location, 20)

with open("sniffer_location2.json", "w") as f:
    json.dump({"sniffer_location": locations}, f)
