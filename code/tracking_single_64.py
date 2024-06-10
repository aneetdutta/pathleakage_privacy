from modules.device import Device
from modules.devicemanager import DeviceManager
from services.general import *
from services.tracking_algorithm_single import tracking_algorithm_single
from modules.mongofn import MongoDB
from collections import defaultdict
from pprint import pprint
from modules.logger import MyLogger
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()
ml = MyLogger("tracking_single_64")

'''The below code will fetch groups for every two timesteps and compare them'''

md.set_collection("groups")

total_timesteps = md.get_all_timesteps()

timestep_pairs = [(total_timesteps[i], total_timesteps[i + 1]) for i in range(len(total_timesteps) - 1)]

database_list:list = []

intra_potential_mapping: defaultdict[set] = defaultdict(set)
visited_intra_list: defaultdict[set] = defaultdict(set)

intra_potential_mapping_list = convert_sets_to_lists(intra_potential_mapping)
visited_intra_mapping_list = convert_sets_to_lists(visited_intra_list)

for timestep_pair in timestep_pairs:
    # Extract documents for each timestep pair
    documents = md.collection.find({"timestep": {"$in": timestep_pair}})
    # Process or print the documents as needed
    ''' Collected data of two timesteps - T0 and T1 which consists of multiple groups
    Storing the data in two_timestep_data'''
    
    two_timestep_data = []
    for document in documents:
        two_timestep_data.append((document['timestep'], document['grouped_data']))
    
    timestep = two_timestep_data[1][0]
    ml.logger.info(timestep)
        
    intra_potential_mapping, visited_intra_list  =  tracking_algorithm_single(two_timestep_data, intra_potential_mapping=intra_potential_mapping, visited_intra_list=visited_intra_list)
    
    # Convert sets to lists in intra_potential_mapping
    intra_potential_mapping_list = convert_sets_to_lists(intra_potential_mapping)
    visited_intra_mapping_list = convert_sets_to_lists(visited_intra_list)
    
    if timestep > 18100:
        break

md.db['baseline_intra_mappings_64'].drop()
md.db['visited_baseline_intra_list_64'].drop()

for i, j in intra_potential_mapping_list.items():
    result = md.db['baseline_intra_mappings_64'].update_one(
            {"_id": str(i)},
            {"$set": {"_id": str(i), "mapping": list(j)}},
            upsert=True  # Create a new document if no document matches the filter
        )

for i, j in visited_intra_mapping_list.items():
    result = md.db['visited_baseline_intra_list_64'].update_one(
            {"_id": str(i)},
            {"$set": {"_id": str(i), "mapping": list(j)}},
            upsert=True  # Create a new document if no document matches the filter
        )