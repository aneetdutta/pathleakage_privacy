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

md.set_collection("aggregate_users")
documents = md.collection.find()
user_df = pd.DataFrame(documents)

md.set_collection("aggregate_timesteps")
documents = md.collection.find()
timestep_data = pd.DataFrame(documents)

md.set_collection('intra_mappings_modified')
documents = list(md.collection.find({"mapping": {"$size": 1}}))
intra_data = {}
for document in documents:
    intra_data[document['_id']]= document['mapping'][0]
intra_df = pd.DataFrame(documents)

md.set_collection('inter_mappings_modified')
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

# print(intra_data)
# inter_data["mapping"] = inter_data["mapping"].apply(set)
# intra_data["mapping"] = intra_data["mapping"].apply(set)

inter_df = pd.merge(inter_df, baseline_data[['id', 'start_timestep', 'last_timestep', 'duration']], left_on='_id', right_on='id', how='left')
intra_df = pd.merge(intra_df, baseline_data[['id', 'start_timestep', 'last_timestep', 'duration']], left_on='_id', right_on='id', how='left')
inter_df = inter_df.drop(columns=['id'])
intra_df = intra_df.drop(columns=['id'])
inter_df = inter_df.sort_values(by='start_timestep')

# print(inter_df)

# intra_chains = find_all_chains(intra_data)
# chain_intra_df = create_chain_dataframe(intra_df)
# print(chain_intra_df)

# sys.exit()

multi_protocol = []

visited_set = set()
for index, inter_row in inter_df.iterrows():
    inter_id = inter_row["_id"]
    inter_mapping = inter_row["mapping"]
    if inter_id in visited_set:
        continue
    visited_set.add(inter_id)
    id1=inter_id
    inter_start_timestep = inter_row["start_timestep"]
    
    ''' Fetch chain for id1 - (inter id) intra mapping and calculating min/max timestep'''
    print(inter_id)
    inter_in_intra = False
    if inter_id in intra_data:
        inter_in_intra = True
        
    if inter_in_intra:
        chain = find_chain_for_key(intra_data, inter_id)
        print(chain)
        chain = chain[0]
        id1_df = inter_df[inter_df['_id'].isin(chain)]
        count_timesteps = sum(id1_df[id1_df['_id'].isin(chain)]['last_timestep'] == TIMESTEPS)
        # print(count_timesteps)
        for id in reversed(chain):
            if count_timesteps > 1 and id1_df[id1_df['_id'] == id]['last_timestep'].values[0] == TIMESTEPS:
                chain.remove(id)
                id1_df = id1_df[id1_df['_id'] != id]
                count_timesteps -= 1
        min_start_timestep_id1 = id1_df['start_timestep'].min()
        max_last_timestep_id1 = id1_df['last_timestep'].max()        
        visited_set.update(set(chain))
    else:
        min_start_timestep_id1 = inter_row["start_timestep"]
        max_last_timestep_id1 = inter_row["last_timestep"]
    
    columns = ['_id', 'start_timestep', 'last_timestep']
    fetch_inter_mapping_timesteps = pd.DataFrame(columns=columns)
    fetch_inter_mapping_timesteps = intra_df[intra_df['_id'].isin(inter_mapping)]
    min_start_timestep = fetch_inter_mapping_timesteps['start_timestep'].min()

    # Filter the DataFrame to include only rows with the minimum start_timestep
    fetch_inter_mapping_timesteps = fetch_inter_mapping_timesteps[fetch_inter_mapping_timesteps['start_timestep'] == min_start_timestep]
    if len(fetch_inter_mapping_timesteps) == 1:
        ''' Fetch chain for its intra mapping and calculating min/max timestep'''
        # print(fetch_inter_mapping_timesteps["_id"])
        intra_id1 = str(fetch_inter_mapping_timesteps['_id'].values[0])
        visited_set.add(intra_id1)
        id2=intra_id1
        if intra_id1 in intra_data:
            chain = find_chain_for_key(intra_data, intra_id1)
            chain = chain[0]
            ''' considering inter for search as it contains all id mappings '''
            id2_df = inter_df[inter_df['_id'].isin(chain)]
            id2_df = id2_df.drop(columns=['mapping'])
            count_timesteps = sum(id2_df[id2_df['_id'].isin(chain)]['last_timestep'] == TIMESTEPS)
            # print(count_timesteps)
            for id in reversed(chain):
                if count_timesteps > 1 and id2_df[id2_df['_id'] == id]['last_timestep'].values[0] == TIMESTEPS:
                    chain.remove(id)
                    id2_df = id2_df[id2_df['_id'] != id]
                    count_timesteps -= 1
                    
            min_start_timestep_id2 = id2_df['start_timestep'].min()
            max_last_timestep_id2 = id2_df['last_timestep'].max()        
            visited_set.update(set(chain))  
        else:
            min_start_timestep_id2 = fetch_inter_mapping_timesteps['start_timestep'].values[0]
            max_last_timestep_id2 = fetch_inter_mapping_timesteps['last_timestep'].values[0]

        min_start_timestep = min(min_start_timestep_id2, min_start_timestep_id1)
        max_last_timestep = max(max_last_timestep_id2, max_last_timestep_id1)
        

    
    elif len(fetch_inter_mapping_timesteps) > 1 and inter_in_intra:
        ''' stop  there | just check intra mappings of inter_id '''
        min_start_timestep = min_start_timestep_id1
        max_last_timestep = max_last_timestep_id1
        linked_id = f"{inter_id}"
        id2= None
        
    duration = max_last_timestep - min_start_timestep
    multi_protocol.append({"id1": id1, "id2": id2, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration})
    # delete 

multi_protocol_df = pd.DataFrame(multi_protocol)
multi_protocol_df = multi_protocol_df.dropna(subset=['start_timestep'])

multi_protocol_df = pd.merge(multi_protocol_df, baseline_data[['id', 'ideal_duration', 'protocol', 'user_id']], left_on='id1', right_on='id', how='left')
multi_protocol_df = multi_protocol_df.drop(columns=['id'])
multi_protocol_df.rename(columns={'user_id': 'user_id1'}, inplace=True)
multi_protocol_df.rename(columns={'protocol': 'protocol_id1'}, inplace=True)


multi_protocol_df = pd.merge(multi_protocol_df, baseline_data[['id', 'protocol', 'user_id']], left_on='id2', right_on='id', how='left')
multi_protocol_df = multi_protocol_df.drop(columns=['id'])
multi_protocol_df.rename(columns={'user_id': 'user_id2'}, inplace=True)
multi_protocol_df.rename(columns={'protocol': 'protocol_id2'}, inplace=True)

multi_protocol_df = multi_protocol_df[multi_protocol_df['user_id1'] == multi_protocol_df['user_id2']]
multi_protocol_df.drop(columns=['user_id2'], inplace=True)
multi_protocol_df.rename(columns={'user_id1': 'user_id'}, inplace=True)
# print(multi_protocol_df)
unique_users_df2 = set(multi_protocol_df['user_id'])
print(unique_users_df2)
multi_protocol_df["privacy_score"] = multi_protocol_df["duration"]/multi_protocol_df["ideal_duration"]

# print(multi_protocol_df)
multi_data = multi_protocol_df.to_dict(orient='records')
multi_protocol_df.to_csv('multi_protocol_localization.csv', index=False)
md.db['reconstruction_multiproto_localization'].insert_many(multi_data)