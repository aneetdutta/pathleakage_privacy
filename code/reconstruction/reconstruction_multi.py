import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from modules.mongofn import MongoDB
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
# from env import USER_TIMESTEPS
import sys
# import sys
md = MongoDB()
from modules.logger import MyLogger

DB_NAME = os.getenv("DB_NAME")


TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP = str_to_bool(os.getenv("TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP"))
TRACK_UNTIL = int(os.getenv("TRACK_UNTIL"))

if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    ml = MyLogger(f"reconstruction_multiprotocol_{DB_NAME}_{TRACK_UNTIL}")
    ml.logger.info(f"Env set: TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP - {TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP}, TRACK_UNTIL - {TRACK_UNTIL}")
else:
    ml = MyLogger(f"reconstruction_multiprotocol_{DB_NAME}")
    
    
if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    md.set_collection(f'modified_intra_mappings_{TRACK_UNTIL}')
    documents = list(md.collection.find())
    intra_data = {document['_id']: document['mapping'] for document in documents}
    intra_df = pd.DataFrame(documents)

    md.set_collection(f'modified_inter_mappings_{TRACK_UNTIL}')
    documents = list(md.collection.find())
    inter_data = {document['_id']: document["user_id"] for document in documents}
    inter_df = pd.DataFrame(documents)

    md.set_collection(f'reconstruction_baseline_{TRACK_UNTIL}')
    documents = md.collection.find()
    baseline_data = pd.DataFrame(documents)
else:
    md.set_collection('modified_intra_mappings')
    documents = list(md.collection.find())
    intra_data = {document['_id']: document['mapping'] for document in documents}
    intra_df = pd.DataFrame(documents)

    md.set_collection('modified_inter_mappings')
    documents = list(md.collection.find())
    inter_data = {document['_id']: document["user_id"] for document in documents}
    inter_df = pd.DataFrame(documents)

    md.set_collection('reconstruction_baseline')
    documents = md.collection.find()
    baseline_data = pd.DataFrame(documents)

''' To create something like:
user_id, linked_id, duration_of_linked_id_through_tracking, duration_of_linked_id_in_sniffed_data, privacy score

Algorithm -
a) Take an id from inter identifier - calculate whether the mappings in it are chained, through its intra
b) Take user_id corresponding to the linked_id, - measure its duration in sniffed data
c) Privacy score = duration_of_linked_id_through_tracking / duration_of_linked_id_in_sniffed_data'''

intra_data_user = {}
for id, mapping in intra_data.items():
    user_id = inter_data[id]
    checker = True
    # if not mapping:
    #     continue
    for id_ in mapping:
        if inter_data[id_] != user_id:
            checker = False
    if checker:
        intra_data_user[id] = mapping
    else:
        intra_data_user[id] = []

# print(intra_data_user)
chained_intra = remove_subsets_and_merge(intra_data_user)
# print(chained_intra)
# sys.exit()
multi_protocol = []
# visited_set = set()
# visited_user = set()
# print(inter_df)
for index, inter_row in inter_df.iterrows():
    # print(index)
    min_start_timestep, max_last_timestep = None, None
    inter_id, intra_id1 = None, None
    inter_id = inter_row["_id"]
    
    inter_mapping = inter_row["mapping"]
    if not inter_mapping:
        ml.logger.info(f"No inter mapping found for {inter_id}")
        continue
    user_id = inter_row["user_id"]
    ml.logger.info(f'{index}, {inter_id}, {user_id}')
    
    # if inter_id in visited_set or user_id in visited_user:
    #     continue
    # visited_set.add(inter_id)
    # visited_user.add(user_id)
    # id1=inter_id
    
    ''' Fetch chain for id1 - (inter id) intra mapping and calculating min/max timestep'''
        
    if inter_id in intra_data_user:
        chain = get_list_containing_value(chained_intra, inter_id)
        ml.logger.info(f"{inter_id}, {chain}")
        id1_df = inter_df[inter_df['_id'].isin(chain)]
        min_start_timestep_id1 = id1_df['start_timestep'].min()
        max_last_timestep_id1 = id1_df['last_timestep'].max()        
        # visited_set.update(set(chain))
    else:
        min_start_timestep_id1 = inter_row["start_timestep"]
        max_last_timestep_id1 = inter_row["last_timestep"]
    
    fetch_inter_mapping_timesteps = intra_df[intra_df['_id'].isin(inter_mapping)]

    temp_start = fetch_inter_mapping_timesteps['start_timestep'].min()
    
    # Filter the DataFrame to include only rows with the minimum start_timestep
    fetch_inter_mapping_timesteps = fetch_inter_mapping_timesteps[fetch_inter_mapping_timesteps['start_timestep'] == temp_start]
    if len(fetch_inter_mapping_timesteps) == 1 and user_id == str(fetch_inter_mapping_timesteps['user_id'].values[0]):
        ''' Fetch chain for its intra mapping and calculating min/max timestep'''
        intra_id1 = str(fetch_inter_mapping_timesteps['_id'].values[0])
        # visited_set.add(intra_id1)
        # id2=intra_id1
        if intra_id1 in intra_data:
            chain = get_list_containing_value(chained_intra, intra_id1)
            # print(chain)
            ml.logger.info(f"{intra_id1}, {chain}")
            ''' considering inter for search as it contains all id mappings '''
            id2_df = inter_df[inter_df['_id'].isin(chain)].drop(columns=['mapping'])
            min_start_timestep_id2 = id2_df['start_timestep'].min()
            max_last_timestep_id2 = id2_df['last_timestep'].max()        
            # visited_set.update(set(chain))
        else:
            min_start_timestep_id2 = fetch_inter_mapping_timesteps['start_timestep'].values[0]
            max_last_timestep_id2 = fetch_inter_mapping_timesteps['last_timestep'].values[0]

        min_start_timestep = min(min_start_timestep_id2, min_start_timestep_id1)
        max_last_timestep = max(max_last_timestep_id2, max_last_timestep_id1)
    elif fetch_inter_mapping_timesteps.empty:
        # print(inter_mapping)
        intra_id1 = inter_mapping[0]
        # visited_set.add(intra_id1)
        result = inter_df.loc[inter_df['_id'] == intra_id1]
        if user_id == result["user_id"].values[0]:
            min_start_timestep_id2 = result['start_timestep'].values[0]
            max_last_timestep_id2 = result['last_timestep'].values[0]
            min_start_timestep = min(min_start_timestep_id2, min_start_timestep_id1)
            max_last_timestep = max(max_last_timestep_id2, max_last_timestep_id1)
        else:
            min_start_timestep = min_start_timestep_id1
            max_last_timestep = max_last_timestep_id1
    else:
        ''' stop  there as multiple inter mappings found, just check intra mappings of inter_id '''
        min_start_timestep = min_start_timestep_id1
        max_last_timestep = max_last_timestep_id1
    
    if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
        if max_last_timestep > TRACK_UNTIL:
            max_last_timestep = TRACK_UNTIL

    duration = max_last_timestep - min_start_timestep
    # print(inter_id, intra_id1)
    multi_protocol.append({"id1": inter_id, "id2": intra_id1, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration, "user_id": user_id})
    # delete 

multi_protocol_df = pd.DataFrame(multi_protocol)
ml.logger.info(multi_protocol_df)
multi_protocol_df = pd.merge(multi_protocol_df, baseline_data[['id', 'ideal_duration', 'protocol']], left_on='id1', right_on='id', how='left')
multi_protocol_df = multi_protocol_df.drop(columns=['id'])
multi_protocol_df.rename(columns={'protocol': 'protocol_id1'}, inplace=True)

multi_protocol_df = pd.merge(multi_protocol_df, baseline_data[['id', 'protocol']], left_on='id2', right_on='id', how='left')
multi_protocol_df = multi_protocol_df.drop(columns=['id'])
# multi_protocol_df.rename(columns={'user_id': 'user_id2'}, inplace=True)
multi_protocol_df.rename(columns={'protocol': 'protocol_id2'}, inplace=True)

# multi_protocol_df = multi_protocol_df[multi_protocol_df['user_id1'] == multi_protocol_df['user_id2']]
# multi_protocol_df.drop(columns=['user_id2'], inplace=True)
# multi_protocol_df.rename(columns={'user_id1': 'user_id'}, inplace=True)

multi_protocol_df['privacy_score'] = multi_protocol_df.apply(calculate_privacy_score, axis=1)
idx = multi_protocol_df.groupby('user_id')['privacy_score'].idxmax()
multi_protocol_df = multi_protocol_df.loc[idx].reset_index(drop=True)

multi_data = multi_protocol_df.to_dict(orient='records')
# print(multi_protocol_df.to_string())
if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    multi_protocol_df.to_csv(f'csv/multi_protocol_{DB_NAME}_{TRACK_UNTIL}.csv', index=False)
    md.db[f'reconstruction_multiproto_{TRACK_UNTIL}'].drop()
    md.db[f'reconstruction_multiproto_{TRACK_UNTIL}'].insert_many(multi_data) 
else:
    multi_protocol_df.to_csv(f'csv/multi_protocol_{DB_NAME}.csv', index=False)
    md.db['reconstruction_multiproto'].drop()
    md.db['reconstruction_multiproto'].insert_many(multi_data)