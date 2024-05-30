from modules.device import Device
from modules.devicemanager import DeviceManager
from services.general import *
from services.tracking_algorithm import tracking_algorithm
from modules.mongofn import MongoDB
import json
from collections import defaultdict
from pprint import pprint
import sys
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()
md.set_collection("sniffed_data")

pipeline = [
    {
        "$group": {
            "_id": {
                "timestep": "$timestep",
                "user_id": "$user_id",
                "location": "$location",
            },
            "sniffer_ids": {"$addToSet": "$sniffer_id"},
            "lte_ids": {"$addToSet": "$lte_id"},
            "wifi_ids": {"$addToSet": "$WiFi_id"},
            "bluetooth_ids": {"$addToSet": "$bluetooth_id"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "timestep": "$_id.timestep",
            "user_id": "$_id.user_id",
            "location": "$_id.location",
            "sniffer_ids": 1,
            "lte_ids": {
                "$filter": {
                    "input": "$lte_ids",
                    "as": "lte_id",
                    "cond": {"$ne": ["$$lte_id", None]}
                }
            },
            "wifi_ids": {
                "$filter": {
                    "input": "$wifi_ids",
                    "as": "wifi_id",
                    "cond": {"$ne": ["$$wifi_id", None]}
                }
            },
            "bluetooth_ids": {
                "$filter": {
                    "input": "$bluetooth_ids",
                    "as": "bluetooth_id",
                    "cond": {"$ne": ["$$bluetooth_id", None]}
                }
            }
        }
    },
    {
        "$sort": {
            "timestep": 1
        }
    }
]

results = list(md.collection.aggregate(pipeline, allowDiskUse=True))

user_location: defaultdict[set] = defaultdict(list)
for result in results:
    timestep = result["timestep"]
    user_id, lte, wifi, bluetooth, location = result["user_id"],result["lte_ids"], result["wifi_ids"], result["bluetooth_ids"], result["location"]
    # print(user_id, lte, wifi, bluetooth)
    if lte and not wifi and not bluetooth:
        print(timestep, user_id, lte, wifi, bluetooth, location)
        user_location[str(user_id)].append([timestep, location])
        
with open("user_location.json", "w") as f:
    json.dump(user_location, f)

user_location = extract_orjson("user_location.json")
sniffer_locations = []
# for users, location_data in user_location.items():
locations = process_dict(user_location, 20)

sniffer_locations: dict[list] = extract_orjson("sniffer_location2.json")
sniffer_l = sniffer_locations["sniffer_location"]

print("Previous", len(sniffer_l))
print("New", len(locations), location)
sniffer_l.extend(locations)
print("total length", len(sniffer_l))
sniffer_locations["sniffer_location"]=(sniffer_l)
with open("sniffer_location2.json", "w") as f:
    json.dump(sniffer_locations, f)