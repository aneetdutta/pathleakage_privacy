from modules.device import Device
from modules.devicemanager import DeviceManager
from services.general import *
from services.tracking_algorithm import tracking_algorithm
from modules.mongofn import MongoDB
from collections import defaultdict
from pprint import pprint
''' Load the sumo_simulation result from mongodb '''
import sys
import pandas as pd

md = MongoDB()

md.set_collection("userid")

# Define the aggregation pipeline
pipeline = [
    {
        "$project": {
            "_id": 0,
            "user_id": 1,
            "lte_ids": 1,
            "wifi_ids": 1,
            "ids": 1
        }
    }
]

documents = md.collection.aggregate(pipeline)


user_data = pd.DataFrame(documents)
# print(user_data)

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
# print(intra_length, inter_length)

# sys.exit(0)
intra_counter = 0
inter_counter = 0

null_intra_counter = 0
null_inter_counter = 0

tracked_intra_users = set()
tracked_intra_users_lte = defaultdict(set)
tracked_intra_users_wifi = defaultdict(set)

tracked_inter_users = set()
tracked_inter_users_wifi_dict = defaultdict(set)
tracked_inter_users_lte_dict = defaultdict(set)

total_users = len(user_data)
visited_intra_ids = set()
visited_inter_ids = set()

lte_intra_total_mapping = set()
lte_intra__single_mapping = set()
lte_intra__multiple_mapping = set()

wifi_intra_total_mapping = set()
wifi_intra__single_mapping = set()
wifi_intra__multiple_mapping = set()

lte_intra__single_users = set()
lte_intra__multiple_users = set()
wifi_intra__single_users = set()
wifi_intra__multiple_users = set()

lte_inter__single_users = set()
lte_inter__multiple_users = set()
wifi_inter__single_users = set()
wifi_inter__multiple_users = set()

null_intra_users = set()
null_inter_users = set()

null_intra_lte_users = set()
null_intra_wifi_users = set()
null_inter_lte_users = set()
null_inter_wifi_users = set()

untracked_intra_lte_users = set()
tracked_intra_lte_users = set()
untracked_intra_wifi_users = set()
tracked_intra_wifi_users = set()

untracked_inter_lte_users = set()
tracked_inter_lte_users = set()
untracked_inter_wifi_users = set()
tracked_inter_wifi_users = set()


for index, row in user_data.iterrows():
    # print(f"Index: {index}")
    lte_ids = set(row['lte_ids'])
    wifi_ids = set(row['wifi_ids'])
    user_id = row['user_id']
    ids = set(row['ids'])
    
    # print(user_id, lte_ids, wifi_ids,ids)
    
    for intra_id, intra_ids in intra_data.items():
        intra_ids = set(intra_ids)
        
        if not intra_ids and intra_id not in visited_intra_ids:
            null_intra_counter +=1
            null_intra_users.add(user_id)
            visited_intra_ids.add(intra_id)
            continue
        
        ''' Lte implementation here'''
        p1_lte, p2_lte = {intra_id}.intersection(lte_ids), intra_ids.intersection(lte_ids)
        

        if p1_lte and p2_lte:
            if intra_id not in lte_intra_total_mapping:
                lte_intra_total_mapping.add(intra_id)
            tracked_intra_lte_users.add(user_id)
            if len(intra_ids) == 1:
                if intra_id not in lte_intra__single_mapping:
                    lte_intra__single_mapping.add(intra_id)
                lte_intra__single_users.add(user_id)
            else:
                if intra_id not in lte_intra__multiple_mapping:
                    lte_intra__multiple_mapping.add(intra_id)
                # print(user_id, intra_ids, intra_id)
                lte_intra__multiple_users.add(user_id)
        else:
            untracked_intra_lte_users.add(user_id)
            untracked_intra_lte_users = untracked_intra_lte_users - tracked_intra_lte_users

        ''' Wifi implementation here'''
        p1_wifi, p2_wifi = {intra_id}.intersection(wifi_ids), intra_ids.intersection(wifi_ids)
        if p1_wifi and p2_wifi:
            if intra_id not in wifi_intra_total_mapping:
                wifi_intra_total_mapping.add(intra_id)
            tracked_intra_wifi_users.add(user_id)
            if len(intra_ids) == 1:
                if intra_id not in wifi_intra__single_mapping:
                    wifi_intra__single_mapping.add(intra_id)
                wifi_intra__single_users.add(user_id)
            else:
                if intra_id not in wifi_intra__multiple_mapping:
                    wifi_intra__multiple_mapping.add(intra_id)
                wifi_intra__multiple_users.add(user_id)
                #print(user_id, intra_ids, len(intra_ids))
            # tracked_intra_users_wifi[user_id].add(intra_id)
        else:
            untracked_intra_wifi_users.add(user_id)
            untracked_intra_wifi_users = untracked_intra_wifi_users - tracked_intra_wifi_users
        pass
    
lte_intra__single_users = lte_intra__single_users - lte_intra__single_users.intersection(lte_intra__multiple_users)
untracked_intra_lte_users = untracked_intra_lte_users - tracked_intra_lte_users

for index, row in user_data.iterrows():
    # print(f"Index: {index}")
    lte_ids = set(row['lte_ids'])
    wifi_ids = set(row['wifi_ids'])
    user_id = row['user_id']
    ids = set(row['ids'])
    
    
    for inter_id, inter_ids in inter_data.items():
        inter_ids = set(inter_ids)
        if not inter_ids and inter_id not in visited_inter_ids:
            null_inter_counter +=1
            print(user_id, inter_id)
            null_inter_users.add(user_id)
            visited_inter_ids.add(inter_id)
            continue
        
        """ if key = LTE, value = WIFI
        if key = Wifi, value = LTE """
        p1_lte, p1_wifi = {inter_id}.intersection(lte_ids), inter_ids.intersection(wifi_ids)
        p2_wifi, p2_lte = {inter_id}.intersection(wifi_ids), inter_ids.intersection(lte_ids)
        # print(p2_wifi, p2_lte)
        
        if p1_lte and p1_wifi:
            tracked_inter_users_lte_dict[user_id].update(inter_ids)
            ''' Atleast one mapping from LTE to Wifi present 
            Tracking inter from lte to wifi '''
            tracked_inter_lte_users.add(user_id)
            # print(user_id, inter_id, inter_ids)
        else:
            untracked_inter_lte_users.add(user_id)
            untracked_inter_lte_users = untracked_inter_lte_users - tracked_inter_lte_users
                
        if p2_wifi and p2_lte:
            tracked_inter_users_wifi_dict[user_id].update(inter_ids)
            ''' Atleast one mapping from Wifi to LTE present 
            Tracking inter from wifi to lte '''
            tracked_inter_wifi_users.add(user_id)
            
        else:
            untracked_inter_wifi_users.add(user_id)
            untracked_inter_wifi_users = untracked_inter_wifi_users - tracked_inter_wifi_users
        
for index, row in user_data.iterrows():
    # print(f"Index: {index}")
    lte_ids = set(row['lte_ids'])
    wifi_ids = set(row['wifi_ids'])
    user_id = row['user_id']
    ids = set(row['ids'])     
    
    if tracked_inter_users_wifi_dict[user_id] == lte_ids:
        # print(user_id, tracked_inter_users_wifi_dict[user_id])
        wifi_inter__single_users.add(user_id)
    else:
        wifi_inter__multiple_users.add(user_id)
    
    if tracked_inter_users_lte_dict[user_id] == wifi_ids:
        # print(user_id, tracked_inter_users_lte_dict[user_id])
        lte_inter__single_users.add(user_id)
    else:
        lte_inter__multiple_users.add(user_id)
        
print("Total Users", total_users)

print("\nTotal Untracked Intra users", len(untracked_intra_lte_users))
print("Total Untracked Inter users", len(untracked_inter_lte_users))

print("Total LTE Intra tracked users ", len(tracked_intra_lte_users))
print("Total LTE Intra users with single mapping: ", len(lte_intra__single_users))
print("Total LTE Intra users with multiple mapping: ", len(lte_intra__multiple_users))

print("\nTotal LTE Intra mappings: ", len(lte_intra_total_mapping))
print("Total LTE Intra single mappings: ", len(lte_intra__single_mapping))
print("Total LTE Intra multiple mappings: ", len(lte_intra__multiple_mapping))

print("\nTotal Wifi Intra tracked users ", len(tracked_intra_wifi_users))
print("Total Wifi Intra users with single mapping: ", len(wifi_intra__single_users))
print("Total Wifi Intra users with multiple mapping: ", len(wifi_intra__multiple_users))

print("\nTotal Wifi Intra mappings: ", len(wifi_intra_total_mapping))
print("Total Wifi Intra single mappings: ", len(wifi_intra__single_mapping))
print("Total WIfi Intra multiple mappings: ", len(wifi_intra__multiple_mapping))

print("\nTotal LTE-Wifi Inter users with single mapping (set having same intra mappings): ", len(lte_inter__single_users))
print("Total LTE-Wifi Inter users with multiple mapping  (set having different intra mappings): ", len(lte_inter__multiple_users))
print("Total LTE-Wifi Inter tracked users: ", len(tracked_inter_lte_users))

print("\nTotal Wifi-LTE Inter users with single mapping: ", len(wifi_inter__single_users))
print("Total Wifi-LTE Inter users with multiple mapping: ", len(wifi_inter__multiple_users))
print("Total Wifi-LTE Inter tracked users: ", len(tracked_inter_wifi_users))

print("\nTotal Null (Wifi+LTE) Intra_ids: ", null_intra_counter)
print("Total Null (Wifi+LTE) Inter_ids: ", null_inter_counter)

print(null_inter_users)
print(visited_inter_ids)