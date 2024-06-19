import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from modules.mongofn import MongoDB
from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
from services.general import UnionFind
import pandas as pd
from env import USER_TIMESTEPS
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
    intra_data[document['_id']]= document['mapping']
intra_df = pd.DataFrame(documents)

md.set_collection('modified_inter_mappings')
documents = list(md.collection.find())
inter_data = {document['_id']: document["user_id"] for document in documents}
inter_df = pd.DataFrame(documents)

md.set_collection('reconstruction_baseline')
documents = md.collection.find()
baseline_data = pd.DataFrame(documents)

# inter_df = pd.merge(inter_df, baseline_data[['id', 'start_timestep', 'last_timestep', 'duration', 'user_id', 'ideal_duration', 'protocol']], left_on='_id', right_on='id', how='left')
intra_df = pd.merge(intra_df, baseline_data[['id', 'start_timestep', 'last_timestep', 'duration', 'user_id', 'ideal_duration', 'protocol']], left_on='_id', right_on='id', how='left')
# inter_df = inter_df.drop(columns=['id'])
intra_df = intra_df.drop(columns=['id'])
# inter_df = inter_df.sort_values(by='start_timestep')

intra_data_user = {}
for id, mapping in intra_data.items():
    # print(mapping, id)
    # print(type(mapping))
    user_id = inter_data[id]
    checker = True
    # if not mapping:
    #     continue
    for id_ in list(mapping):
        # print(id_)
        if inter_data[id_] != user_id:
            checker = False
    if checker:
        intra_data_user[id] = mapping
    else:
        intra_data_user[id] = []

# print(intra_data_user)
chained_intra = remove_subsets_and_merge(intra_data_user)


baseline_smart = []

# visited_set = set()
for index, inter_row in inter_df.iterrows():
    min_start_timestep, max_last_timestep = None, None
    
    inter_id = inter_row["_id"]
    user_id = inter_row["user_id"]
        
    min_start_timestep = inter_row["start_timestep"]
    max_last_timestep = inter_row["last_timestep"]
    
    if inter_id in intra_data:
        chain = get_list_containing_value(chained_intra, inter_id)
        id_df = inter_df[inter_df['_id'].isin(chain)]
        min_start_timestep = min(min_start_timestep, id_df['start_timestep'].min())
        max_last_timestep = max(max_last_timestep, id_df['last_timestep'].max())     

    duration = max_last_timestep - min_start_timestep
    baseline_smart.append({"id": inter_id, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration, "ideal_duration": inter_row["ideal_duration"], "user_id": inter_row["user_id"], "protocol": inter_row["protocol"]})

baseline_smart_df = pd.DataFrame(baseline_smart)

baseline_smart_df['privacy_score'] = baseline_smart_df.apply(calculate_privacy_score, axis=1)

wifi_df = baseline_smart_df[baseline_smart_df['protocol'] == 'wifi'].reset_index(drop=True)
# print(list(wifi_df["user_id"]))
lte_df = baseline_smart_df[baseline_smart_df['protocol'] == 'lte'].reset_index(drop=True)

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

wifi_df.to_csv('csv/baseline_smart_wifi.csv', index=False)
lte_df.to_csv('csv/baseline_smart_lte.csv', index=False)

# bl_data = baseline_smart_df.to_dict(orient='records')
# md.db['reconstruction_baseline'].drop()
# md.db['reconstruction_baseline'].insert_many(bl_data)

    
# multi_protocol_df["privacy_score"] = multi_protocol_df["duration"]/multi_protocol_df["ideal_duration"]