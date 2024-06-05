from services.general import *
from modules.mongofn import MongoDB
from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
from services.general import UnionFind
import pandas as pd
from env import TIMESTEPS
import sys
# import sys
md = MongoDB()
from modules.logger import MyLogger
ml = MyLogger("reconstruction_multiprotocol")

md.set_collection('modified_intra_mappings')
documents = list(md.collection.find({"mapping": {"$size": 1}}))
intra_data = {document['_id']: (document['mapping'][0], document["user_id"]) for document in documents}
intra_df = pd.DataFrame(documents)

md.set_collection('modified_inter_mappings')
documents = md.collection.find()
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

multi_protocol = []
visited_set = set()
visited_user = set()
for index, inter_row in inter_df.iterrows():
    min_start_timestep, max_last_timestep = None, None
    inter_id, intra_id1 = None, None
    inter_id = inter_row["_id"]
    
    inter_mapping = inter_row["mapping"]
    user_id = inter_row["user_id"]
    ml.logger.info(f'{index}, {inter_id}, {user_id}')
    
    if inter_id in visited_set or user_id in visited_user:
        continue
    visited_set.add(inter_id)
    visited_user.add(user_id)
    # id1=inter_id
    
    ''' Fetch chain for id1 - (inter id) intra mapping and calculating min/max timestep'''
        
    if inter_id in intra_data:
        chain = find_chain_for_key(intra_data, inter_id, user_id)
        chain: list = chain[0]
        id1_df = inter_df[inter_df['_id'].isin(chain)]
        # count_timesteps = (id1_df["last_timestep"] == TIMESTEPS).sum()
        # ml.logger.info(f"{inter_df['_id']} - {count_timesteps}")
        
        # for id in reversed(chain):
        #     if count_timesteps > 1 and id1_df[id1_df['_id'] == id]['last_timestep'].values[0] == TIMESTEPS:
        #         chain.remove(id)
        #         id1_df = id1_df[id1_df['_id'] != id]
        #         count_timesteps -= 1
        min_start_timestep_id1 = id1_df['start_timestep'].min()
        max_last_timestep_id1 = id1_df['last_timestep'].max()        
        visited_set.update(set(chain))
    else:
        min_start_timestep_id1 = inter_row["start_timestep"]
        max_last_timestep_id1 = inter_row["last_timestep"]
    
    fetch_inter_mapping_timesteps = intra_df[intra_df['_id'].isin(inter_mapping)]
    # print(inter_id, fetch_inter_mapping_timesteps)
    temp_start = fetch_inter_mapping_timesteps['start_timestep'].min()
    
    # Filter the DataFrame to include only rows with the minimum start_timestep
    fetch_inter_mapping_timesteps = fetch_inter_mapping_timesteps[fetch_inter_mapping_timesteps['start_timestep'] == temp_start]
    if len(fetch_inter_mapping_timesteps) == 1 and user_id == str(fetch_inter_mapping_timesteps['user_id'].values[0]):
        ''' Fetch chain for its intra mapping and calculating min/max timestep'''
        intra_id1 = str(fetch_inter_mapping_timesteps['_id'].values[0])
        visited_set.add(intra_id1)
        # id2=intra_id1
        if intra_id1 in intra_data:
            chain = find_chain_for_key(intra_data, intra_id1, user_id)[0]
            print(chain)
            ''' considering inter for search as it contains all id mappings '''
            id2_df = inter_df[inter_df['_id'].isin(chain)].drop(columns=['mapping'])
            min_start_timestep_id2 = id2_df['start_timestep'].min()
            max_last_timestep_id2 = id2_df['last_timestep'].max()        
            visited_set.update(set(chain))
        else:
            min_start_timestep_id2 = fetch_inter_mapping_timesteps['start_timestep'].values[0]
            max_last_timestep_id2 = fetch_inter_mapping_timesteps['last_timestep'].values[0]

        min_start_timestep = min(min_start_timestep_id2, min_start_timestep_id1)
        max_last_timestep = max(max_last_timestep_id2, max_last_timestep_id1)
    elif fetch_inter_mapping_timesteps.empty:
        intra_id1 = inter_mapping[0]
        visited_set.add(intra_id1)
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
        ''' stop  there , just check intra mappings of inter_id '''
        min_start_timestep = min_start_timestep_id1
        max_last_timestep = max_last_timestep_id1
        
    duration = max_last_timestep - min_start_timestep
    multi_protocol.append({"id1": inter_id, "id2": intra_id1, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration, "user_id": user_id})
    # delete 

multi_protocol_df = pd.DataFrame(multi_protocol)
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

multi_data = multi_protocol_df.to_dict(orient='records')
# print(multi_protocol_df.to_string())
multi_protocol_df.to_csv('csv/multi_protocol.csv', index=False)
md.db['reconstruction_multiproto'].drop()
md.db['reconstruction_multiproto'].insert_many(multi_data)