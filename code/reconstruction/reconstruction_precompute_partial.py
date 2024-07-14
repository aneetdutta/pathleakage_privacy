
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

md.set_collection("parsed_sniffed_data")
documents = list(md.collection.find())
# data = list(pd.DataFrame(documents))
id_data = defaultdict(set)
for i in documents:
    id_data[i["id"]].add(i["timestep"])

# print(id_data)
md.set_collection("aggregate_users")
documents = list(md.collection.find())
# data = list(pd.DataFrame(documents))
user_data = {document["user_id"]: set(document["ids"]) for document in documents}

user_timeset = {}
user_duration = {}
for user_id, ids in user_data.items():
    temp_set = set()
    for id in ids:
        print(type(temp_set), id_data[id])
        temp_set.update(id_data[id])
    user_timeset[user_id] = temp_set
    user_duration[user_id] = len(temp_set)

ml = MyLogger(f"reconstruction_multiprotocol_{DB_NAME}")

md.set_collection('modified_intra_mappings')
documents = list(md.collection.find())
intra_data = {document['_id']: document['mapping'] for document in documents}
intra_df = pd.DataFrame(documents)

md.set_collection('modified_inter_mappings')
documents = list(md.collection.find())
inter_time_data = {document['_id']: (document["start_timestep"], document["last_timestep"]) for document in documents}
inter_user_data = {document['_id']: document["user_id"] for document in documents}
inter_last_time_data = {document['_id']: document["last_timestep"] for document in documents}
inter_mapping_data = {document['_id']: document["mapping"] for document in documents}
# print(inter_last_time_data["7DLVEZAWLLHL"])
inter_df = pd.DataFrame(documents)

md.set_collection("aggregate_users")
documents = list(md.collection.find())
user_data = {document['user_id']: document["ids"] for document in documents}
user_time_data = {document['user_id']: document["last_timestep"] for document in documents}




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
corresponding_users = set()
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
reconstructed_inter = {}
k=0
for inter_id, mapping in inter_mapping_data.items():
    ml.logger.info(f"index - {k} of {total_rows}")
    k=k+1
    # print(index)
    u = inter_user_data[inter_id]
    min_start_timestep, max_last_timestep = inter_time_data[inter_id][0], inter_time_data[inter_id][1]
    
    if inter_id in chained_dict:
        chain1 = chained_dict[inter_id]
        # print(chain1)
    else:
        chain1 = []
    # user_id_match = inter_row["user_id_match"]
    chain_ = inter_intra_mapper(mapping)

    chain_.append(chain1)
    
    chain_sets = [set(c) for c in chain_]
    updated_chain = []

    for c_set in chain_sets:
        updated_set = {j for j in c_set if inter_last_time_data[j] <= user_time_data[u]}
        updated_chain.append(updated_set)

    # Convert the sets back to lists if necessary
    chain_ = [list(s) for s in updated_chain]
    user_id_ = None
    lchain = []
    # p = [False]*len(chain_)
    
    correctness_ = False
    '''Due to computation this becomes slower, so we directly use the user_id available with the inter to verify the corrcetness'''
    ids = user_data[inter_user_data[inter_id]]
    for i, c in enumerate(chain_):
        if not c:
            continue
        if set(c).issubset(ids):
            lchain.extend(c)
            correctness_ = True
            correctness[inter_id] = True
            flag = True
    
    if not correctness_:
        ''' Consider baseline'''
        correctness[inter_id] = False
        corresponding_users.add(u)
        reconstructed_inter[inter_id] = [inter_id]
        continue
    
    reconstructed_inter[inter_id] = lchain


print("Processing now")
for inter_id, rchain in reconstructed_inter.items():
    user_ = inter_user_data[inter_id]
    ud = user_duration[user_]
    if correctness[inter_id]:
        time_set = set()
        for id in rchain:
            time_set.update(id_data[id])
        privacy_score = len(time_set)/ud
    else:
        privacy_score = len(id_data[inter_id])/ud
    multi_protocol.append({"id": inter_id,  "user_id": user_, "privacy_score": privacy_score})
    

# ml.logger.info("Correctness: {correc}")

true_count = sum(correctness.values())

# Count False values
false_count = len(correctness) - true_count

ml.logger.info(f"Count of True values: {true_count}")
ml.logger.info(f"Count of False values: {false_count}")

print("completed")
multi_protocol_df = pd.DataFrame(multi_protocol)
ml.logger.info(multi_protocol_df)

idx = multi_protocol_df.groupby('user_id')['privacy_score'].idxmax()
multi_protocol_df = multi_protocol_df.loc[idx].reset_index(drop=True)

multi_data = multi_protocol_df.to_dict(orient='records')

multi_protocol_df.to_csv(f'csv/multi_protocol_{DB_NAME}_partial.csv', index=False)
md.db['reconstruction_multiproto'].drop()
md.db['reconstruction_multiproto'].insert_many(multi_data)

with open(f'data/correctness_{DB_NAME}.json', 'w') as f:
    json.dump(correctness, f)
    
ml.logger.info(corresponding_users)
ml.logger.info(len(corresponding_users))


