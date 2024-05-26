import pickle
import ijson, json
import time, sys
# import pyximport; pyximport.install()
import numpy as np
from modules.device import Device
from modules.devicemanager import DeviceManager
from funct.fn import *
from funct.mongofn import MongoDB
from funct.rules import *
from pprint import pprint
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()

# md.set_collection("20240506150753_sniffed_data")
# results = md.aggregate_save()

# new_collection = md.db['aggregated_results']# Insert the aggregated results into the new collection
# now = time.time()
# for result in results: 
#     # print(result)
#     # break
#     new_collection.insert_one(result)
# print("Time taken to aggregate and save to mongodb: ", time.time() - now)


md.set_collection("aggregated_results")
'''grouped according to timestep and sniffer'''
sniffer_data = md.collection.find().sort('timestep', 1)


group_collection = md.db['groups']
md.set_collection('groups')

# list_cur = list(sniffer_data)
# 
''' Processing every timestep - contains dict : {sniffer_id : [data]}
Stores the processed group to mongodb collection '''

for document in sniffer_data:
    id = document["_id"]
    timestep = document["timestep"]
    sniffer_data = document["sniffer_data"]
    print(id, timestep)
    group = grouper(sniffer_data, md, id)
    group_collection.insert_one({"timestep": timestep, "grouped_data": group})
    