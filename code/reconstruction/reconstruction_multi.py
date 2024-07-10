import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from modules.mongofn import MongoDB
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
# from env import USER_TIMESTEPS
import sys
from itertools import chain
# import sys
md = MongoDB()
import json
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
    inter_time_data = {document['_id']: (document["start_timestep"], document["last_timestep"]) for document in documents}
    inter_user_data = {document['_id']: document["user_id"] for document in documents}
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
    inter_time_data = {document['_id']: (document["start_timestep"], document["last_timestep"]) for document in documents}
    inter_user_data = {document['_id']: document["user_id"] for document in documents}
    inter_df = pd.DataFrame(documents)

    md.set_collection('reconstruction_baseline')
    documents = md.collection.find()
    baseline_data = pd.DataFrame(documents)


md.set_collection("aggregate_users")
documents = md.collection.find()
user_data = {document['user_id']: document["ids"] for document in documents}
''' To create something like:
user_id, linked_id, duration_of_linked_id_through_tracking, duration_of_linked_id_in_sniffed_data, privacy score

Algorithm -
a) Take an id from inter identifier - calculate whether the mappings in it are chained, through its intra
b) Take user_id corresponding to the linked_id, - measure its duration in sniffed data
c) Privacy score = duration_of_linked_id_through_tracking / duration_of_linked_id_in_sniffed_data'''


''' Create chain of intra mappings '''

intra_single = {}
for id, mapping in intra_data.items():
    # print(mapping)
    if len(mapping) > 1:
        intra_single[id] = ''
    elif mapping:
        intra_single[id] = mapping[0]
    else:
        intra_single[id] = ''

chained_intra = find_all_possible_chains(intra_single)
# Initialize an empty dictionary
chained_dict = {char: lst for lst in chained_intra for char in lst}

multi_protocol = []

def merge_matching_sublists(lst, target_sublist):
    # print(target_sublist)
    # print(lst)
    matching_set = set()
    for sublist in lst:
        if set(target_sublist).issubset(set(sublist)):
            matching_set.update(set(sublist))
    return matching_set

def inter_intra_mapper(data):
    if not data:
        return []
    # print("checking")
    o = []
    for p, p_item in data.items():
        sf = set(merge_matching_sublists(chained_intra, p_item))
        # print(sf)
        o.append(sf)
    # print(o)
    return o


correctness = {}
total_rows = inter_df.shape[0]

for index, inter_row in inter_df.iterrows():
    ml.logger.info(f"index - {index} of {total_rows}")
    # print(index)
    u = inter_row["user_id"]
    min_start_timestep, max_last_timestep = inter_row["start_timestep"], inter_row["last_timestep"]
    inter_id = inter_row["_id"]
    if inter_id in chained_dict:
        chain1 = chained_dict[inter_id]
        # print(chain1)
    else:
        chain1 = []
    # user_id_match = inter_row["user_id_match"]
    chain_ = inter_intra_mapper(inter_row["mapping"])
    # print(len(chain_))
    
    chain_.append(chain1)
    user_id_ = None

    p = [False]*len(chain_)
    
    for user_id, ids in user_data.items():
        flag = False
        for i, c in enumerate(chain_):
            # print(i, c)
            if not c:
                continue
            if set(c).issubset(ids):
                correctness[inter_id] = True
                p[i] = True
                flag = True
        if flag:
            break
    
    if inter_id not in correctness or not correctness[inter_id]:
        ''' Consider baseline'''
        # print(p)
        correctness[inter_id] = False
        # print(min_start_timestep)
        # print(max_last_timestep)
        duration = max_last_timestep - min_start_timestep
        multi_protocol.append({"id": inter_id, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration, "user_id": u})
        continue
    # print(p)
    lchain = []
    for i, j in enumerate(p):
        if p[i]:
            lchain.extend(chain_[i])
            
    fetch_inter_mapping_timesteps = inter_df[inter_df['_id'].isin(lchain)]
    # fetch_inter_mapping_timesteps = fetch_inter_mapping_timesteps.drop_duplicates(subset=['start_timestep', 'last_timestep'])
    min_start_timestep = min(fetch_inter_mapping_timesteps['start_timestep'].min(), min_start_timestep)
    max_last_timestep = max(fetch_inter_mapping_timesteps['last_timestep'].max(), max_last_timestep)

    
    if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
        if max_last_timestep > TRACK_UNTIL:
            max_last_timestep = TRACK_UNTIL

    duration = max_last_timestep - min_start_timestep
    # print(inter_id, intra_id1)
    multi_protocol.append({"id": inter_id, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration, "user_id": u})


# ml.logger.info("Correctness: {correc}")

true_count = sum(correctness.values())

# Count False values
false_count = len(correctness) - true_count

ml.logger.info(f"Count of True values: {true_count}")
ml.logger.info(f"Count of False values: {false_count}")

print("completed")
multi_protocol_df = pd.DataFrame(multi_protocol)
ml.logger.info(multi_protocol_df)
multi_protocol_df = pd.merge(multi_protocol_df, baseline_data[['id', 'ideal_duration']], left_on='id', right_on='id', how='left')
# multi_protocol_df = multi_protocol_df.drop(columns=['id'])
# multi_protocol_df.rename(columns={'protocol': 'protocol_id1'},1 inplace=True)

multi_protocol_df = pd.merge(multi_protocol_df, baseline_data[['id']], left_on='id', right_on='id', how='left')
# multi_protocol_df = multi_protocol_df.drop(columns=['id'])
# multi_protocol_df.rename(columns={'user_id': 'user_id2'}, inplace=True)
# multi_protocol_df.rename(columns={'protocol': 'protocol_id2'}, inplace=True)

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

with open(f'data/correctness_{DB_NAME}.json', 'w') as f:
    json.dump(correctness, f)