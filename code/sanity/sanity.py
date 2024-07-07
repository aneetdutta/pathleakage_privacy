import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from modules.mongofn import MongoDB
from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
import sys

from modules.logger import MyLogger

DB_NAME = os.getenv("DB_NAME")
ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH", "false"))

md = MongoDB()
ml = MyLogger(f"sanity_{DB_NAME}")

md.set_collection("aggregate_users")
documents = md.collection.find()
user_data = pd.DataFrame(documents)

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
# ml.logger.info(intra_length, inter_length)

# sys.exit(0)
intra_counter = 0
inter_counter = 0

null_intra_counter = 0
null_inter_counter = 0

tracked_intra_users = set()
tracked_intra_users_lte = defaultdict(set)
tracked_intra_users_wifi = defaultdict(set)
tracked_intra_users_ble = defaultdict(set)

tracked_inter_users = set()
tracked_inter_users_wifi_dict = defaultdict(set)
tracked_inter_users_ble_dict = defaultdict(set)
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

ble_intra_total_mapping = set()
ble_intra__single_mapping = set()
ble_intra__multiple_mapping = set()

lte_intra__single_users = set()
lte_intra__multiple_users = set()
wifi_intra__single_users = set()
wifi_intra__multiple_users = set()
ble_intra__single_users = set()
ble_intra__multiple_users = set()

lte_inter__single_users = set()
lte_inter__multiple_users = set()
wifi_inter__single_users = set()
wifi_inter__multiple_users = set()
ble_inter__single_users = set()
ble_inter__multiple_users = set()

null_intra_users = set()
null_inter_users = set()

null_intra_lte_users = set()
null_intra_wifi_users = set()
null_intra_ble_users = set()
null_inter_lte_users = set()
null_inter_wifi_users = set()
null_inter_ble_users = set()

untracked_intra_lte_users = set()
tracked_intra_lte_users = set()
untracked_intra_wifi_users = set()
tracked_intra_wifi_users = set()
untracked_intra_ble_users = set()
tracked_intra_ble_users = set()

untracked_inter_lte_users = set()
tracked_inter_lte_users = set()
untracked_inter_wifi_users = set()
tracked_inter_wifi_users = set()
untracked_inter_ble_users = set()
tracked_inter_ble_users = set()


for index, row in user_data.iterrows():
    # ml.logger.info(f"Index: {index}")
    lte_ids = set(row['lte_ids'])
    wifi_ids = set(row['wifi_ids'])
    if ENABLE_BLUETOOTH:
        ble_ids = set(row['bluetooth_ids'])
    else:
        ble_ids = set()
    user_id = row['user_id']
    ids = set(row['ids'])
    
    # ml.logger.info(user_id, lte_ids, wifi_ids,ids)
    
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
                # ml.logger.info(user_id, intra_ids, intra_id)
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
                #ml.logger.info(user_id, intra_ids, len(intra_ids))
            # tracked_intra_users_wifi[user_id].add(intra_id)
        else:
            untracked_intra_wifi_users.add(user_id)
            untracked_intra_wifi_users = untracked_intra_wifi_users - tracked_intra_wifi_users
        
        ''' BLE implementation here'''
        if ENABLE_BLUETOOTH:
            p1_ble, p2_ble = {intra_id}.intersection(ble_ids), intra_ids.intersection(ble_ids)
            if p1_ble and p2_ble:
                if intra_id not in ble_intra_total_mapping:
                    ble_intra_total_mapping.add(intra_id)
                tracked_intra_ble_users.add(user_id)
                if len(intra_ids) == 1:
                    if intra_id not in ble_intra__single_mapping:
                        ble_intra__single_mapping.add(intra_id)
                    ble_intra__single_users.add(user_id)
                else:
                    if intra_id not in ble_intra__multiple_mapping:
                        ble_intra__multiple_mapping.add(intra_id)
                    ble_intra__multiple_users.add(user_id)
                    #ml.logger.info(user_id, intra_ids, len(intra_ids))
                # tracked_intra_users_ble[user_id].add(intra_id)
            else:
                untracked_intra_ble_users.add(user_id)
                untracked_intra_ble_users = untracked_intra_ble_users - tracked_intra_ble_users

    
lte_intra__single_users = lte_intra__single_users - lte_intra__single_users.intersection(lte_intra__multiple_users)
wifi_intra__single_users = wifi_intra__single_users - wifi_intra__single_users.intersection(wifi_intra__multiple_users)
ble_intra__single_users = ble_intra__single_users - ble_intra__single_users.intersection(ble_intra__multiple_users)

untracked_intra_lte_users = untracked_intra_lte_users - tracked_intra_lte_users
untracked_intra_wifi_users = untracked_intra_wifi_users - tracked_intra_wifi_users
untracked_intra_ble_users = untracked_intra_ble_users - tracked_intra_ble_users


for index, row in user_data.iterrows():
    # ml.logger.info(f"Index: {index}")
    lte_ids = set(row['lte_ids'])
    wifi_ids = set(row['wifi_ids'])
    if ENABLE_BLUETOOTH:
        ble_ids = set(row['bluetooth_ids'])
    else:
        ble_ids = set()
    user_id = row['user_id']
    ids = set(row['ids'])
    
    
    for inter_id, inter_ids in inter_data.items():
        inter_ids = set(inter_ids)
        if not inter_ids and inter_id not in visited_inter_ids:
            ml.logger.info(inter_id)
            null_inter_counter +=1
            # ml.logger.info(user_id, inter_id)
            null_inter_users.add(user_id)
            visited_inter_ids.add(inter_id)
            continue
        
        """ if key = LTE, value = WIFI
        if key = Wifi, value = LTE """
        p1_lte, p1_wifi = {inter_id}.intersection(lte_ids), inter_ids.intersection(wifi_ids)
        p2_wifi, p2_lte = {inter_id}.intersection(wifi_ids), inter_ids.intersection(lte_ids)
        if ENABLE_BLUETOOTH:
            p1_ble, p2_ble = inter_ids.intersection(ble_ids), inter_ids.intersection(ble_ids)
            p3_ble, p3_lte, p3_wifi = {inter_id}.intersection(ble_ids), inter_ids.intersection(lte_ids), inter_ids.intersection(wifi_ids)
        # ml.logger.info(p2_wifi, p2_lte)
        
        if not ENABLE_BLUETOOTH:
            if p1_lte and p1_wifi:
                tracked_inter_users_lte_dict[user_id].update(inter_ids)
                ''' Atleast one mapping from LTE to Wifi present 
                Tracking inter from lte to wifi '''
                tracked_inter_lte_users.add(user_id)
                # ml.logger.info(user_id, inter_id, inter_ids)
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
        else:
            if p1_lte and p1_wifi and p1_ble:
                tracked_inter_users_lte_dict[user_id].update(inter_ids)
                ''' Atleast one mapping from LTE to Wifi present 
                Tracking inter from lte to wifi '''
                tracked_inter_lte_users.add(user_id)
                # ml.logger.info(user_id, inter_id, inter_ids)
            else:
                untracked_inter_lte_users.add(user_id)
                untracked_inter_lte_users = untracked_inter_lte_users - tracked_inter_lte_users
                    
            if p2_wifi and p2_lte and p2_ble:
                tracked_inter_users_wifi_dict[user_id].update(inter_ids)
                ''' Atleast one mapping from Wifi to LTE present 
                Tracking inter from wifi to lte '''
                tracked_inter_wifi_users.add(user_id)
                
            else:
                untracked_inter_wifi_users.add(user_id)
                untracked_inter_wifi_users = untracked_inter_wifi_users - tracked_inter_wifi_users
            
            if p3_ble and p3_lte and p3_ble:
                tracked_inter_users_ble_dict[user_id].update(inter_ids)
                ''' Atleast one mapping from Wifi to LTE present 
                Tracking inter from wifi to lte '''
                tracked_inter_ble_users.add(user_id)
                
            else:
                untracked_inter_ble_users.add(user_id)
                untracked_inter_ble_users = untracked_inter_ble_users - tracked_inter_ble_users
        
for index, row in user_data.iterrows():
    # ml.logger.info(f"Index: {index}")
    lte_ids = set(row['lte_ids'])
    wifi_ids = set(row['wifi_ids'])
    ble_ids = set(row['bluetooth_ids'])
    user_id = row['user_id']
    ids = set(row['ids'])     
    
    if not ENABLE_BLUETOOTH:
        if tracked_inter_users_wifi_dict[user_id] == lte_ids:
            # ml.logger.info(user_id, tracked_inter_users_wifi_dict[user_id])
            wifi_inter__single_users.add(user_id)
        else:
            wifi_inter__multiple_users.add(user_id)
        
        if tracked_inter_users_lte_dict[user_id] == wifi_ids:
            # ml.logger.info(user_id, tracked_inter_users_lte_dict[user_id])
            lte_inter__single_users.add(user_id)
        else:
            lte_inter__multiple_users.add(user_id)
    else:
        if tracked_inter_users_wifi_dict[user_id] == lte_ids.union(ble_ids):
            # ml.logger.info(user_id, tracked_inter_users_wifi_dict[user_id])
            wifi_inter__single_users.add(user_id)
        else:
            wifi_inter__multiple_users.add(user_id)
        
        if tracked_inter_users_lte_dict[user_id] == wifi_ids.union(ble_ids):
            # ml.logger.info(user_id, tracked_inter_users_lte_dict[user_id])
            lte_inter__single_users.add(user_id)
        else:
            lte_inter__multiple_users.add(user_id)
            
        if tracked_inter_users_ble_dict[user_id] == lte_ids.union(wifi_ids):
            # ml.logger.info(user_id, tracked_inter_users_lte_dict[user_id])
            ble_inter__single_users.add(user_id)
        else:
            ble_inter__multiple_users.add(user_id)
        
ml.logger.info(f"Total Users: {total_users}")

ml.logger.info(f"Total Untracked (Not randomized) LTE Intra users {len(untracked_intra_lte_users)}")
ml.logger.info(f"Total Untracked LTE Inter users {len(untracked_inter_lte_users)}")

ml.logger.info(f"Total LTE Intra tracked users  {len(tracked_intra_lte_users)}")
ml.logger.info(f"Total LTE Intra users with single mapping:  {len(lte_intra__single_users)}")
ml.logger.info(f"Total LTE Intra users with multiple mapping:  {len(lte_intra__multiple_users)}")

ml.logger.info(f"Total LTE Intra mappings for tracked users:  {len(lte_intra_total_mapping)}")
ml.logger.info(f"Total LTE Intra single mappings for tracked users:  {len(lte_intra__single_mapping)}")
ml.logger.info(f"Total LTE Intra multiple mappings for tracked users:  {len(lte_intra__multiple_mapping)}")

ml.logger.info(f"Total Untracked (Not Randomized) WIFI Intra users {len(untracked_intra_wifi_users)}")
ml.logger.info(f"Total Untracked WIFI Inter users {len(untracked_inter_wifi_users)}")

ml.logger.info(f"Total Wifi Intra tracked users  {len(tracked_intra_wifi_users)}")
ml.logger.info(f"Total Wifi Intra users with single mapping:  {len(wifi_intra__single_users)}")
ml.logger.info(f"Total Wifi Intra users with multiple mapping:  {len(wifi_intra__multiple_users)}")

ml.logger.info(f"Total Wifi Intra mappings for tracked users:  {len(wifi_intra_total_mapping)}")
ml.logger.info(f"Total Wifi Intra single mappings for tracked users:  {len(wifi_intra__single_mapping)}")
ml.logger.info(f"Total WIfi Intra multiple mappings for tracked users:  {len(wifi_intra__multiple_mapping)}")

if ENABLE_BLUETOOTH:
    ml.logger.info(f"Total Untracked (Not Randomized) BLE Intra users {len(untracked_intra_ble_users)}")
    ml.logger.info(f"Total Untracked BLE Inter users {len(untracked_inter_ble_users)}")

    ml.logger.info(f"Total BLE Intra tracked users  {len(tracked_intra_ble_users)}")
    ml.logger.info(f"Total BLE Intra users with single mapping:  {len(ble_intra__single_users)}")
    ml.logger.info(f"Total BLE Intra users with multiple mapping:  {len(ble_intra__multiple_users)}")

    ml.logger.info(f"Total BLE Intra mappings for tracked users:  {len(ble_intra_total_mapping)}")
    ml.logger.info(f"Total BLE Intra single mappings for tracked users:  {len(ble_intra__single_mapping)}")
    ml.logger.info(f"Total BLE Intra multiple mappings for tracked users:  {len(ble_intra__multiple_mapping)}")

if not ENABLE_BLUETOOTH:
    ml.logger.info(f"Total LTE-Wifi Inter users with single mapping (set having same intra mappings):  {len(lte_inter__single_users)}")
    ml.logger.info(f"Total LTE-Wifi Inter users with multiple mapping  (set having different intra mappings):  {len(lte_inter__multiple_users)}")
    ml.logger.info(f"Total LTE-Wifi Inter tracked users: {len(tracked_inter_lte_users)}")

    ml.logger.info(f"Total Wifi-LTE Inter users with single mapping: {len(wifi_inter__single_users)}")
    ml.logger.info(f"Total Wifi-LTE Inter users with multiple mapping: {len(wifi_inter__multiple_users)}")
    ml.logger.info(f"Total Wifi-LTE Inter tracked users: {len(tracked_inter_wifi_users)}")
else:
    ml.logger.info(f"Total LTE-Wifi-ble Inter users with single mapping (set having same intra mappings):  {len(lte_inter__single_users)}")
    ml.logger.info(f"Total LTE-Wifi-ble Inter users with multiple mapping  (set having different intra mappings):  {len(lte_inter__multiple_users)}")
    ml.logger.info(f"Total LTE-Wifi-ble Inter tracked users: {len(tracked_inter_lte_users)}")

    ml.logger.info(f"Total Wifi-LTE-ble Inter users with single mapping: {len(wifi_inter__single_users)}")
    ml.logger.info(f"Total Wifi-LTE-ble Inter users with multiple mapping: {len(wifi_inter__multiple_users)}")
    ml.logger.info(f"Total Wifi-LTE-ble Inter tracked users: {len(tracked_inter_wifi_users)}")
    
    ml.logger.info(f"Total BLE-LTE-WIFI Inter users with single mapping: {len(ble_inter__single_users)}")
    ml.logger.info(f"Total BLE-LTE-WIFI Inter users with multiple mapping: {len(ble_inter__multiple_users)}")
    ml.logger.info(f"Total BLE-LTE-WIFI Inter tracked users: {len(tracked_inter_ble_users)}")

ml.logger.info(f"Total Null Intra_ids: {null_intra_counter}")
ml.logger.info(f"Total Null Inter_ids:  {null_inter_counter}")

# ml.logger.info(f"Null inter users: {null_inter_users}")
# print(visited_inter_ids)