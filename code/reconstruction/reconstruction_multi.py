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
    inter_user_data = {document['_id']: document["user_id"] for document in documents}
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
    ''' Tries to first clean the intra mappings based on user id, those which dont match are set to null '''
    user_id = inter_user_data[id]
    checker = True
    # if not mapping:
    #     continue
    for id_ in mapping:
        if inter_user_data[id_] != user_id:
            checker = False
            break
    if checker:
        intra_data_user[id] = mapping
    else:
        intra_data_user[id] = []
# print(intra_data_user)
# sys.exit()
# print(intra_data_user)
# Initialize the columns
intra_df["chained_start_timestep"] = 0
intra_df["chained_last_timestep"] = 0

# Function to remove subsets and merge, assuming it's efficient and correct
chained_intra = remove_subsets_and_merge(intra_data_user)

# Flatten chained_intra and create a DataFrame with each intraid and its group
intraid_to_group = {intraid: idx for idx, group in enumerate(chained_intra) for intraid in group}

# Create a DataFrame from the dictionary
group_df = pd.DataFrame(list(intraid_to_group.items()), columns=['_id', 'group'])

# Merge the group DataFrame with intra_df to get the group for each row in intra_df
merged_df = intra_df.merge(group_df, on='_id', how='left')

# Group by 'group' and calculate the min and max timesteps
grouped = merged_df.groupby('group').agg({'start_timestep': 'min', 'last_timestep': 'max'}).reset_index()

# Merge the aggregated data back with the original merged DataFrame
merged_df = merged_df.merge(grouped, on='group', suffixes=('', '_chained'))

# Update the original DataFrame
intra_df['chained_start_timestep'] = merged_df['start_timestep_chained']
intra_df['chained_last_timestep'] = merged_df['last_timestep_chained']

inter_df = inter_df.merge(intra_df[['_id', 'chained_start_timestep', 'chained_last_timestep']], on='_id', how='left')
inter_df.fillna({'chained_start_timestep': inter_df['start_timestep']}, inplace=True)
inter_df.fillna({'chained_last_timestep': inter_df['last_timestep']}, inplace=True)

# inter_df['chained_start_timestep'] = inter_df['chained_start_timestep'].fillna(inter_df['start_timestep'], inplace=True)
# inter_df['chained_last_timestep'] = inter_df['chained_last_timestep'].fillna(inter_df['start_timestep'], inplace=True)
# print(inter_df)

# print(intra_df[['_id', 'start_timestep', 'last_timestep', 'chained_start_timestep', 'chained_last_timestep']])
# sys.exit()

# print(chained_intra)
# sys.exit()
multi_protocol = []
# visited_set = set()
# visited_user = set()
# print(inter_df)
def check_user_id(row, id_to_user_id):
    mapped_user_ids = [id_to_user_id[_id] for _id in row['mapping']]
    return all(user_id == row['user_id'] for user_id in mapped_user_ids)

inter_df['user_id_match'] = inter_df.apply(lambda row: check_user_id(row, inter_user_data), axis=1)

# user_id_match = check_user_id_match(inter_df, inter_user_data)

# print(user_id_match)
# sys.exit()


for index, inter_row in inter_df.iterrows():
    # print(index)
    min_start_timestep, max_last_timestep = None, None
    inter_id, intra_id1 = None, None
    inter_id = inter_row["_id"]
    user_id_match = inter_row["user_id_match"]
    # print(inter_id)
    # print(inter_row)
        
    inter_mapping = inter_row["mapping"]
    if not inter_mapping:
        ml.logger.info(f"No inter mapping found for {inter_id}")
        # continue
    user_id = inter_row["user_id"]
    ml.logger.info(f'{index}, {inter_id}, {user_id}')
    
    ''' Fetch chain for id1 - (inter id) intra mapping and calculating min/max timestep'''
        
    # if inter_id in intra_data_user:
    min_start_timestep = inter_row["chained_start_timestep"]
    max_last_timestep = inter_row["chained_last_timestep"]
    # else:
    #     min_start_timestep_id1 = inter_row["start_timestep"]
    #     max_last_timestep_id1 = inter_row["last_timestep"]
    
    fetch_inter_mapping_timesteps = inter_df[inter_df['_id'].isin(inter_mapping)]
    fetch_inter_mapping_timesteps = fetch_inter_mapping_timesteps[
        ~(
            ((fetch_inter_mapping_timesteps['start_timestep'] <= min_start_timestep) &
            (fetch_inter_mapping_timesteps['last_timestep'] <= min_start_timestep)) |
            ((fetch_inter_mapping_timesteps['start_timestep'] >= max_last_timestep) &
            (fetch_inter_mapping_timesteps['last_timestep'] <= max_last_timestep))
        )
    ]
    
    if not fetch_inter_mapping_timesteps.empty:
        fetch_inter_mapping_timesteps = fetch_inter_mapping_timesteps.drop_duplicates(subset=['chained_start_timestep', 'chained_last_timestep'])

    # print(fetch_inter_mapping_timesteps)
    # sys.exit()
    # Filter the DataFrame to include only rows with the minimum start_timestep
    if user_id_match:
        min_start_timestep = min(fetch_inter_mapping_timesteps['chained_start_timestep'].min(), min_start_timestep)
        max_last_timestep = max(fetch_inter_mapping_timesteps['chained_last_timestep'].max(), max_last_timestep)
    
    if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
        if max_last_timestep > TRACK_UNTIL:
            max_last_timestep = TRACK_UNTIL

    duration = max_last_timestep - min_start_timestep
    # print(inter_id, intra_id1)
    multi_protocol.append({"id": inter_id, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "duration": duration, "user_id": user_id})
    # delete 

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