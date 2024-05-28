from modules.device import Device
from modules.devicemanager import DeviceManager
from services.general import *
from services.tracking_algorithm import tracking_algorithm
from modules.mongofn import MongoDB
from collections import defaultdict
from pprint import pprint
''' Load the sumo_simulation result from mongodb '''
import sys

md = MongoDB()

md.set_collection("userid")

# Define the aggregation pipeline
pipeline = [
    {
        "$project": {
            "_id": 0,
            "user_id": 1,
            "ids": 1
        }
    }
]

documents = md.collection.aggregate(pipeline)

user_data = {}
for document in documents:
    user_data[document['user_id']] = document['ids']



md.set_collection('intra_mappings')

intra_docs = md.collection.find()
intra_data = {}
for document in intra_docs:
    intra_data[document['_id']] = document['mapping']
    
    
md.set_collection('inter_mappings')

inter_docs = md.collection.find()
inter_data = {}
for document in inter_docs:
    inter_data[document['_id']] = document['mapping']


intra_length = len(list(intra_data))
inter_length = len(list(inter_data))
print(intra_length, inter_length)

# sys.exit(0)
intra_counter = 0
inter_counter = 0

null_intra_counter = 0
null_inter_counter = 0

tracked_intra_users = set()
tracked_inter_users = set()

total_users = set()
visited_intra_ids = set()
visited_inter_ids = set()

for user_id, ids in user_data.items():
    total_users.add(user_id)
    ids = set(ids)
    
    for intra_id, intra_ids in intra_data.items():
        if not intra_ids and intra_id not in visited_intra_ids:
            null_intra_counter +=1
            visited_intra_ids.add(intra_id)
            continue
        p1 = {intra_id}.intersection(ids)
        p2 = set(intra_ids).intersection(ids)
        
        if p1 and p2 and intra_id not in tracked_intra_users:
            intra_counter+=1
            tracked_intra_users.add(user_id)

    for inter_id, inter_ids in inter_data.items():
        if not inter_ids and inter_id not in visited_inter_ids:
            null_inter_counter +=1
            visited_inter_ids.add(inter_id)
            continue
        p1 = {inter_id}.intersection(ids)
        p2 = set(inter_ids).intersection(ids)
        
        if p1 and p2 and inter_id not in tracked_inter_users:
            inter_counter+=1
            tracked_inter_users.add(user_id)


print("Actual Inter Length: ", inter_length)
print("Null Inter Counter: ", null_inter_counter)
inter_length = inter_length - null_inter_counter

print("Actual Intra Length: ", intra_length)
print("Null Intra Counter: ", null_intra_counter)
intra_length = intra_length - null_intra_counter


print(f"Total Correct Inter Potential Mappings found: {inter_counter} of {inter_length}")
print(f"Total Correct Intra Potential Mappings found: {intra_counter} of {intra_length}")


print("Total Users: ", len(total_users))
print("Total Tracked Users: ", len(tracked_intra_users))