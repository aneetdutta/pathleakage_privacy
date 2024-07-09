import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from modules.mongofn import MongoDB
# from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
# import sys
md = MongoDB()
from modules.logger import MyLogger


DB_NAME = os.getenv("DB_NAME")
# ml = MyLogger(f"reconstruction_baseline_{DB_NAME}")
ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH"))
ENABLE_WIFI = str_to_bool(os.getenv("ENABLE_WIFI"))
ENABLE_LTE = str_to_bool(os.getenv("ENABLE_LTE"))

TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP = str_to_bool(os.getenv("TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP"))
TRACK_UNTIL = int(os.getenv("TRACK_UNTIL"))

if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    ml = MyLogger(f"reconstruction_baseline_{DB_NAME}_{TRACK_UNTIL}")
    ml.logger.info(f"Env set: TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP - {TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP}, TRACK_UNTIL - {TRACK_UNTIL}")
else:
    ml = MyLogger(f"reconstruction_baseline_{DB_NAME}")

md.set_collection("aggregate_users")
documents = md.collection.find()
user_df = pd.DataFrame(documents)

md.set_collection("aggregate_timesteps")
documents = md.collection.find()
timestep_data = pd.DataFrame(documents)

if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    md.set_collection(f'inter_mappings_{TRACK_UNTIL}')
    documents = list(md.collection.find())
    inter_df = pd.DataFrame(documents)
    inter_data = {document['_id']: document['mapping'] for document in documents}

    md.set_collection(f'intra_mappings_{TRACK_UNTIL}')
    documents = list(md.collection.find())
    # intra_data = {document['_id']: document['mapping'][0] for document in documents}
    intra_df = pd.DataFrame(documents)
else:
    md.set_collection('inter_mappings')
    documents = list(md.collection.find())
    inter_df = pd.DataFrame(documents)
    inter_data = {document['_id']: document['mapping'] for document in documents}

    md.set_collection('intra_mappings')
    documents = list(md.collection.find())
    # intra_data = {document['_id']: document['mapping'][0] for document in documents}
    intra_df = pd.DataFrame(documents)

ml.logger.info("MongoDB data loaded")

''' To create something like:
user_id, linked_id, duration_of_linked_id_through_tracking, duration_of_linked_id_in_sniffed_data, privacy score

Algorithm -
a) Take a key (single identifier) - measure duration of tracking after tracking
b) Take user_id corresponding to the linked_id, - measure its duration in sniffed data
c) Privacy score = duration_of_linked_id_through_tracking / duration_of_linked_id_in_sniffed_data'''

''' Baseline single protocol'''

''' Preprocessing timestep data '''
timestep_dict = {}
for index, row in timestep_data.iterrows():
    for id in row["ids"]:
        if id not in timestep_dict:
            timestep_dict[id] = {"start_timestep": row["timestep"], "last_timestep": row["timestep"]}
        else:
            timestep_dict[id]["last_timestep"] = row["timestep"]
            
ml.logger.info("Preprocessed timestep data")

''' Preprocessing user data '''
# if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
#     user_info_dict = {}
#     for index, row in user_df.iterrows():
#         for protocol in ['lte', 'wifi', 'bluetooth']:
#             ids_column = f"{protocol}_ids"
#             for id in row[ids_column]:
#                 user_info_dict[id] = {
#                     "user_id": row["user_id"],
#                     "ideal_duration": TRACK_UNTIL - row["start_timestep"] if row["duration"] > TRACK_UNTIL - row["start_timestep"] else row["duration"],
#                     "protocol": protocol
#                 }
# else:
user_info_dict = {}
for index, row in user_df.iterrows():
    for protocol in ['lte', 'wifi', 'bluetooth']:
        ids_column = f"{protocol}_ids"
        for id in row[ids_column]:
            user_info_dict[id] = {
                "user_id": row["user_id"],
                "ideal_duration": row["duration"],
                "protocol": protocol
            }

ml.logger.info("Preprocessed user data")

baseline = []
i=0
for id in inter_data.keys():
    # print(i)
    ml.logger.info(f"{id} - i")
    i+=1
    # try:
    baseline_ = {
        "id": id,
        "start_timestep": timestep_dict.get(id, {}).get("start_timestep", ""),
        "last_timestep": timestep_dict.get(id, {}).get("last_timestep", ""),
        "user_id": user_info_dict.get(id, {}).get("user_id", ""),
        "ideal_duration": user_info_dict.get(id, {}).get("ideal_duration", ""),
        "protocol": user_info_dict.get(id, {}).get("protocol", "")
    }
    # except:
    #     # print(id, "hello")
    #     raise Exception

    baseline.append(baseline_)

ml.logger.info("Baseline iteration completed")

bl_df = pd.DataFrame(baseline)
# print(bl_df.to_string())
# non_numeric_rows = bl_df[bl_df['last_timestep'].isna()]

# print("Rows with non-numeric values in 'last_timestep':")
# print(non_numeric_rows)
bl_df['start_timestep'] = bl_df['start_timestep'].astype(float)

if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    bl_df['last_timestep'] = bl_df.apply(lambda row: TRACK_UNTIL if row['last_timestep'] > TRACK_UNTIL  else row['last_timestep'], axis=1)
else:
    bl_df['last_timestep'] = bl_df['last_timestep'].astype(float)
    
bl_df["duration"] = bl_df["last_timestep"] - bl_df["start_timestep"]
bl_df['privacy_score'] = bl_df.apply(calculate_privacy_score, axis=1)
ml.logger.info("Privacy score calculated")

if ENABLE_WIFI:
    wifi_df = bl_df[bl_df['protocol'] == 'wifi'].reset_index(drop=True)
    idx = wifi_df.groupby('user_id')['privacy_score'].idxmax()
    wifi_df = wifi_df.loc[idx].reset_index(drop=True)
else:
    wifi_df = None

if ENABLE_LTE:
    lte_df = bl_df[bl_df['protocol'] == 'lte'].reset_index(drop=True)
    idx = lte_df.groupby('user_id')['privacy_score'].idxmax()
    lte_df = lte_df.loc[idx].reset_index(drop=True)
else:
    lte_df = None

if ENABLE_BLUETOOTH:
    bluetooth_df = bl_df[bl_df['protocol'] == 'bluetooth'].reset_index(drop=True)
    idx = bluetooth_df.groupby('user_id')['privacy_score'].idxmax()
    bluetooth_df = bluetooth_df.loc[idx].reset_index(drop=True)
else:
    bluetooth_df = None

ml.logger.info(f"Saving csv of WIFI:{ENABLE_WIFI}, LTE: {ENABLE_LTE}, BLE: {ENABLE_BLUETOOTH}")

if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    if ENABLE_WIFI:
        wifi_df.to_csv(f'csv/baseline_wifi_{DB_NAME}_{TRACK_UNTIL}.csv', index=False)
    if ENABLE_LTE:
        lte_df.to_csv(f'csv/baseline_lte_{DB_NAME}_{TRACK_UNTIL}.csv', index=False)
    if ENABLE_BLUETOOTH:
        bluetooth_df.to_csv(f'csv/baseline_ble_{DB_NAME}_{TRACK_UNTIL}.csv', index=False)
else:
    if ENABLE_WIFI:
        wifi_df.to_csv(f'csv/baseline_wifi_{DB_NAME}.csv', index=False)
    if ENABLE_LTE:
        lte_df.to_csv(f'csv/baseline_lte_{DB_NAME}.csv', index=False)
    if ENABLE_BLUETOOTH:
        bluetooth_df.to_csv(f'csv/baseline_ble_{DB_NAME}.csv', index=False)

ml.logger.info("Saving data to mongodb - collection reconstruction_baseline")

merge_columns= ["id","start_timestep", "last_timestep", "duration", "user_id", "protocol", "ideal_duration"]

if not set(merge_columns).issubset(set(intra_df.keys())):
    inter_df = (
        pd.merge(
            inter_df,
            bl_df[merge_columns],
            left_on="_id",
            right_on="id",
            how="left",
        )
        .drop(columns=["id"])
        .sort_values(by="start_timestep")
    )

    intra_df = pd.merge(
        intra_df,
        bl_df[merge_columns],
        left_on="_id",
        right_on="id",
        how="left",
    ).drop(columns=["id"])

    if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
        md.db[f'modified_inter_mappings_{TRACK_UNTIL}'].drop()
        md.db[f'modified_inter_mappings_{TRACK_UNTIL}'].insert_many(inter_df.to_dict(orient='records'))
        md.db[f'modified_intra_mappings_{TRACK_UNTIL}'].drop()
        md.db[f'modified_intra_mappings_{TRACK_UNTIL}'].insert_many(intra_df.to_dict(orient='records'))
    else:
        md.db['modified_inter_mappings'].drop()
        md.db['modified_inter_mappings'].insert_many(inter_df.to_dict(orient='records'))
        md.db['modified_intra_mappings'].drop()
        md.db['modified_intra_mappings'].insert_many(intra_df.to_dict(orient='records'))

bl_data = bl_df.to_dict(orient='records')
if TRACK_AND_RECONSTRUCT_UNTIL_TIMESTEP:
    md.db[f'reconstruction_baseline_{TRACK_UNTIL}'].drop()
    md.db[f'reconstruction_baseline_{TRACK_UNTIL}'].insert_many(bl_data)
else:
    md.db['reconstruction_baseline'].drop()
    md.db['reconstruction_baseline'].insert_many(bl_data)
ml.logger.info("Reconstruction baseline completed")