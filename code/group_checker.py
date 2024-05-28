from modules.device import Device
from modules.devicemanager import DeviceManager
from services.general import *
from services.tracking_algorithm import tracking_algorithm
from modules.mongofn import MongoDB
from collections import defaultdict
from pprint import pprint
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()

# md.set_collection("userid")

# # Define the aggregation pipeline
# pipeline = [
#     {
#         "$project": {
#             "_id": 0,
#             "user_id": 1,
#             "ids": 1
#         }
#     }
# ]

# documents = md.collection.aggregate(pipeline)

# user_data = {}
# for document in documents:
#     user_data[document['user_id']] = user_data['ids'] 
 
 
md.set_collection("sniffer_data")

# Query to find documents where only one of "LTE", "WiFi", or "Bluetooth" exists
pipeline = [
    {
        '$group': {
            '_id': {
                'timestep': '$timestep',
                'user_id': '$user_id'
            },
            'data': {
                '$push': {
                    "protocol": "$protocol",
                    "lte_id": "$lte_id",
                    "WiFi_id": "$WiFi_id",
                    "bluetooth_id": "$bluetooth_id",
                    "location": "$location",
                }
            }
        }
    },
    {
        '$group': {
            '_id': '$_id.timestep',
            'user_data': {
                '$push': {
                    'k': { '$toString': '$_id.user_id' },
                    'v': '$data'
                }
            }
        }
    },
    {
        '$project': {
            '_id': 0,
            'timestep': '$_id',
            'user_data': {
                '$arrayToObject': '$user_data'
            }
        }
    }
]

# Execute the aggregation pipeline
results = md.collection.aggregate(pipeline)

# Print the results
for result in results:
    print(result)
    break

