import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from services.tracking_algorithm import tracking_algorithm
from modules.mongofn import MongoDB
from collections import defaultdict
from pprint import pprint
from modules.logger import MyLogger
''' Load the sumo_simulation result from mongodb '''

md = MongoDB()
ml = MyLogger("tracking")

'''The below code will fetch groups for every two timesteps and compare them'''

md.set_collection("groups")

total_timesteps = md.get_all_timesteps()

timestep_pairs = [(total_timesteps[i], total_timesteps[i + 1]) for i in range(len(total_timesteps) - 1)]

database_list:list = []

intra_potential_mapping: defaultdict[set] = defaultdict(set)
inter_potential_mapping: defaultdict[set] = defaultdict(set)
visited_inter_list: defaultdict[set] = defaultdict(set)
visited_intra_list: defaultdict[set] = defaultdict(set)

intra_potential_mapping_list = convert_sets_to_lists(intra_potential_mapping)
inter_potential_mapping_list = convert_sets_to_lists(inter_potential_mapping)
visited_inter_mapping_list = convert_sets_to_lists(visited_inter_list)
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
        
    intra_potential_mapping, inter_potential_mapping, visited_inter_list, visited_intra_list  =  tracking_algorithm(two_timestep_data, intra_potential_mapping=intra_potential_mapping, inter_potential_mapping=inter_potential_mapping, visited_inter_list=visited_inter_list, visited_intra_list=visited_intra_list)
    
    # Convert sets to lists in intra_potential_mapping
    intra_potential_mapping_list = convert_sets_to_lists(intra_potential_mapping)
    inter_potential_mapping_list = convert_sets_to_lists(inter_potential_mapping)
    visited_inter_mapping_list = convert_sets_to_lists(visited_inter_list)
    visited_intra_mapping_list = convert_sets_to_lists(visited_intra_list)
    
    check_full_document_database = False
    
    if check_full_document_database:
        database_dict = {"intra_data": intra_potential_mapping_list, "inter_data": inter_potential_mapping_list, "visited_inter_data": visited_inter_mapping_list, "visited_intra_data": visited_intra_mapping_list}
        # intra_dict[str(two_timestep_data[1][0])] = dict(intra_potential_mapping)
        result = md.db['database_mappings'].update_one(
                {"_id": str(timestep)},
                {"$set": database_dict},
                upsert=True  # Create a new document if no document matches the filter
            )
            
    # if int(timestep) > 2:
    #     break
    
    
md.db['intra_mappings'].drop()
md.db['inter_mappings'].drop()
md.db['visited_inter_list'].drop()
md.db['visited_intra_list'].drop()

for i, j in intra_potential_mapping_list.items():
    result = md.db['intra_mappings'].update_one(
            {"_id": str(i)},
            {"$set": {"_id": str(i), "mapping": list(j)}},
            upsert=True  # Create a new document if no document matches the filter
        )

for i, j in inter_potential_mapping_list.items():
    result = md.db['inter_mappings'].update_one(
            {"_id": str(i)},
            {"$set": {"_id": str(i), "mapping": list(j)}},
            upsert=True  # Create a new document if no document matches the filter
        )
    
for i, j in visited_inter_mapping_list.items():
    result = md.db['visited_inter_list'].update_one(
            {"_id": str(i)},
            {"$set": {"_id": str(i), "mapping": list(j)}},
            upsert=True  # Create a new document if no document matches the filter
        )
for i, j in visited_intra_mapping_list.items():
    result = md.db['visited_intra_list'].update_one(
            {"_id": str(i)},
            {"$set": {"_id": str(i), "mapping": list(j)}},
            upsert=True  # Create a new document if no document matches the filter
        )