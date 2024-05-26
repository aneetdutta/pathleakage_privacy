import pickle
import ijson, json
import time, sys
import numpy as np
from modules.device import Device
from modules.devicemanager import DeviceManager
from funct.fn import *
from funct.mongofn import MongoDB
from pprint import pprint
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()

''' The below code converts the sumo_simulation results to aggregated results of the sniffer
It is modelled as below
{timestep: 0, sniffer_data: {0: [{groups}]}}'''

# md.set_collection("20240506150753_sniffed_data")
# results = md.aggregate_save()

# new_collection = md.db['aggregated_results']# Insert the aggregated results into the new collection
# now = time.time()
# for result in results: 
#     # print(result)
#     # break
#     new_collection.insert_one(result)
# print("Time taken to aggregate and save to mongodb: ", time.time() - now)


'''The below code converts the aggregated results into groups using the grouping distance algorithm
The groups of every sniffer are first calculated and then they are appended to single timestep.
So, we have the dict as 
{timestep: 0, grouped_data: [{LTE: "", WIFI: "", BLUETOOTH: ""}]}'''


# md.set_collection("aggregated_results")
# '''grouped according to timestep and sniffer'''
# sniffer_data = md.collection.find().sort('timestep', 1)


# group_collection = md.db['groups']
# # md.set_collection('groups')

# # list_cur = list(sniffer_data)
# # 
# ''' Processing every timestep - contains dict : {sniffer_id : [data]}
# Stores the processed group to mongodb collection '''

# for document in sniffer_data:
#     id = document["_id"]
#     timestep = document["timestep"]
#     sniffer_data = document["sniffer_data"]
#     print(id, timestep)
#     group = grouper(sniffer_data, md, id)
#     group_collection.insert_one({"timestep": timestep, "grouped_data": group})
    
'''The below code will fetch groups for every two timesteps and compare them'''

md.set_collection("groups")

total_timesteps = md.get_all_timesteps()

timestep_pairs = [(total_timesteps[i], total_timesteps[i + 1]) for i in range(len(total_timesteps) - 1)]

for timestep_pair in timestep_pairs:
    # Extract documents for each timestep pair
    documents = md.collection.find({"timestep": {"$in": timestep_pair}})
    # Process or print the documents as needed
    ''' Collected data of two timesteps - T0 and T1 which consists of multiple groups
    Storing the data in two_timestep_data'''
    two_timestep_data = []
    for document in documents:
        two_timestep_data.append(tuple(document['timestep'], document['grouped_data']))
        
    potential_mapping = tracking_algorithm(two_timestep_data)

    break
