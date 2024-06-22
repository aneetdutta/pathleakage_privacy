import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from tracking.tracking_algorithm_smart import tracking_algorithm_smart
from modules.mongofn import MongoDB
from collections import defaultdict
import math
from pprint import pprint
from modules.logger import MyLogger

DB_NAME = os.getenv("DB_NAME")
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()

BLUETOOTH_MAX_TRANSMIT = int(os.getenv("BLUETOOTH_MAX_TRANSMIT"))
WIFI_MAX_TRANSMIT = int(os.getenv("WIFI_MAX_TRANSMIT"))
LTE_MAX_TRANSMIT = int(os.getenv("LTE_MAX_TRANSMIT"))
SNIFFER_TIMESTEP = max(BLUETOOTH_MAX_TRANSMIT, WIFI_MAX_TRANSMIT, LTE_MAX_TRANSMIT)

TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP = str_to_bool(os.getenv("TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP"))
TRACK_UNTIL = int(os.getenv("TRACK_UNTIL"))
FIRST_TIMESTEP = int(os.getenv("FIRST_TIMESTEP"))

if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    ml = MyLogger(f"tracking_single_{DB_NAME}_{TRACK_UNTIL}")
    ml.logger.info(f"Env set: TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP - {TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP}, TRACK_UNTIL - {TRACK_UNTIL}")
else:
    ml = MyLogger(f"tracking_single_{DB_NAME}")
    

'''The below code will fetch groups for every two timesteps and compare them'''

md.set_collection("groups_smart")

total_timesteps = md.get_all_timesteps()

timestep_pairs = [(total_timesteps[i], total_timesteps[i + 1]) for i in range(len(total_timesteps) - 1)]

database_list:list = []

intra_potential_mapping: defaultdict[set] = defaultdict(set)
visited_intra_list: defaultdict[set] = defaultdict(set)

intra_potential_mapping_list = convert_sets_to_lists(intra_potential_mapping)
visited_intra_mapping_list = convert_sets_to_lists(visited_intra_list)

for timestep_pair in timestep_pairs:
    # Extract documents for each timestep pair
    documents = md.collection.find({"st_window": {"$in": timestep_pair}})
    # Process or print the documents as needed
    ''' Collected data of two timesteps - T0 and T1 which consists of multiple groups
    Storing the data in two_timestep_data'''
    
    two_timestep_data = []
    for document in documents:
        two_timestep_data.append((document['st_window'], document['grouped_data']))
    
    timestep = two_timestep_data[1][0]
    ml.logger.info(timestep)
        
    intra_potential_mapping, visited_intra_list  =  tracking_algorithm_smart(two_timestep_data, intra_potential_mapping=intra_potential_mapping, visited_intra_list=visited_intra_list)
    
    # Convert sets to lists in intra_potential_mapping
    intra_potential_mapping_list = convert_sets_to_lists(intra_potential_mapping)
    visited_intra_mapping_list = convert_sets_to_lists(visited_intra_list)

    if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
        TS = math.floor((TRACK_UNTIL - FIRST_TIMESTEP)/SNIFFER_TIMESTEP)
        if int(timestep) > TS:
            ml.logger.info(f"Tracking break; {int(timestep)} step reached")
            break


if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    md.db[f'baseline_intra_mappings_{TRACK_UNTIL}'].drop()
    md.db[f'visited_baseline_intra_list_{TRACK_UNTIL}'].drop()

    for i, j in intra_potential_mapping_list.items():
        result = md.db[f'baseline_intra_mappings_{TRACK_UNTIL}'].update_one(
                {"_id": str(i)},
                {"$set": {"_id": str(i), "mapping": list(j)}},
                upsert=True  # Create a new document if no document matches the filter
            )

    for i, j in visited_intra_mapping_list.items():
        result = md.db[f'visited_baseline_intra_list_{TRACK_UNTIL}'].update_one(
                {"_id": str(i)},
                {"$set": {"_id": str(i), "mapping": list(j)}},
                upsert=True  # Create a new document if no document matches the filter
            )
else:
    md.db['baseline_intra_mappings'].drop()
    md.db['visited_baseline_intra_list'].drop()

    for i, j in intra_potential_mapping_list.items():
        result = md.db['baseline_intra_mappings'].update_one(
                {"_id": str(i)},
                {"$set": {"_id": str(i), "mapping": list(j)}},
                upsert=True  # Create a new document if no document matches the filter
            )

    for i, j in visited_intra_mapping_list.items():
        result = md.db['visited_baseline_intra_list'].update_one(
                {"_id": str(i)},
                {"$set": {"_id": str(i), "mapping": list(j)}},
                upsert=True  # Create a new document if no document matches the filter
            )