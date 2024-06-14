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

md.set_collection('baseline_intra_mappings')
documents = list(md.collection.find({"mapping": {"$size": 1}}))
intra_data = {}
for document in documents:
    intra_data[document['_id']]= document['mapping'][0]
intra_df = pd.DataFrame(documents)

md.set_collection('inter_mappings')
documents = md.collection.find()
inter_df = pd.DataFrame(documents)

md.set_collection('reconstruction_baseline')
documents = md.collection.find()
baseline_data = pd.DataFrame(documents)


inter_df = pd.merge(inter_df, baseline_data[['id', 'start_timestep', 'last_timestep', 'duration', 'user_id', 'ideal_duration', 'protocol']], left_on='_id', right_on='id', how='left')
intra_df = pd.merge(intra_df, baseline_data[['id', 'start_timestep', 'last_timestep', 'duration', 'user_id', 'ideal_duration', 'protocol']], left_on='_id', right_on='id', how='left')
inter_df = inter_df.drop(columns=['id'])
intra_df = intra_df.drop(columns=['id'])
inter_df = inter_df.sort_values(by='start_timestep')

intra_data = {}
# print(list(intra_df.keys()))
for index, intra_row in intra_df.iterrows():
    # print(intra_row)
    intra_data[intra_row["_id"]] = (intra_row["mapping"][0], intra_row["user_id"])


baseline_random = []

visited_set = set()
for index, inter_row in inter_df.iterrows():
    inter_id = inter_row["_id"]
    user_id = inter_row["user_id"]
    # print(inter_id, inter_row["user_id"], inter_row["protocol"]), 
    if inter_id in visited_set:
        continue
    visited_set.add(inter_id)
    id1=inter_id
    # print("Interid", inter_id)
    if inter_id in intra_data:
        inter_in_intra = True
    else:
        inter_in_intra = False
        
    
    min_start_timestep = inter_row["start_timestep"]
    max_last_timestep = inter_row["last_timestep"]
    
    if inter_in_intra:
        chain = find_chain_for_key(intra_data, inter_id, user_id)
        ''' chain is ordered assuming'''
        # print(chain)
        # print("hello")
        chain = chain[0]
        # print(chain)
        id_df = inter_df[inter_df['_id'].isin(chain)]
        id_df = id_df.drop(columns=['mapping'])
        count_timesteps = sum(id_df[id_df['_id'].isin(chain)]['last_timestep'] == TIMESTEPS)
        # print(count_timesteps)
        for id in reversed(chain):
            if count_timesteps > 1 and id_df[id_df['_id'] == id]['last_timestep'].values[0] == TIMESTEPS:
                chain.remove(id)
                id_df = id_df[id_df['_id'] != id]
                count_timesteps -= 1
        # print(id_df)
        min_start_timestep = min(min_start_timestep, id_df['start_timestep'].min())
        max_last_timestep = max(max_last_timestep, id_df['last_timestep'].max())     
        visited_set.update(set(chain))

    
    duration = max_last_timestep - min_start_timestep
    baseline_random.append({"id": id1, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration, "ideal_duration": inter_row["ideal_duration"], "user_id": inter_row["user_id"], "protocol": inter_row["protocol"]})

baseline_random_df = pd.DataFrame(baseline_random)

# print(baseline_random_df)

baseline_random_df["privacy_score"] = baseline_random_df["duration"]/baseline_random_df["ideal_duration"]


wifi_df = baseline_random_df[baseline_random_df['protocol'] == 'wifi'].reset_index(drop=True)
# print(list(wifi_df["user_id"]))
lte_df = baseline_random_df[baseline_random_df['protocol'] == 'lte'].reset_index(drop=True)

idx = wifi_df.groupby('user_id')['privacy_score'].idxmax()
wifi_df = wifi_df.loc[idx].reset_index(drop=True)

idx = lte_df.groupby('user_id')['privacy_score'].idxmax()
lte_df = lte_df.loc[idx].reset_index(drop=True)

unique_users_df1 = set(wifi_df['user_id'])
unique_users_df2 = set(lte_df['user_id'])

# print(unique_users_df1)
# print(unique_users_df1)
# print(unique_users_df2)
# Find the missing user ID in df2
missing_user_in_df2 = unique_users_df2 - unique_users_df1

print("Missing user in df2:", missing_user_in_df2)

wifi_df.to_csv('csv/baseline_random_wifi.csv', index=False)
lte_df.to_csv('csv/baseline_random_lte.csv', index=False)

# bl_data = baseline_random_df.to_dict(orient='records')
# md.db['reconstruction_baseline'].drop()
# md.db['reconstruction_baseline'].insert_many(bl_data)

    
# multi_protocol_df["privacy_score"] = multi_protocol_df["duration"]/multi_protocol_df["ideal_duration"]