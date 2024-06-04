from services.general import *
from modules.mongofn import MongoDB
from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
# import sys
md = MongoDB()
from modules.logger import MyLogger

ml = MyLogger("reconstruction_baseline")

md.set_collection("aggregate_users")
documents = md.collection.find()
user_df = pd.DataFrame(documents)

md.set_collection("aggregate_timesteps")
documents = md.collection.find()
timestep_data = pd.DataFrame(documents)

md.set_collection('inter_mappings')

inter_docs = md.collection.find()
inter_data = {}
for document in inter_docs:
    inter_data[document['_id']] = document['mapping']

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
    print(i)
    i+=1
    baseline_ = {
        "id": id,
        "start_timestep": timestep_dict.get(id, {}).get("start_timestep", ""),
        "last_timestep": timestep_dict.get(id, {}).get("last_timestep", ""),
        "user_id": user_info_dict.get(id, {}).get("user_id", ""),
        "ideal_duration": user_info_dict.get(id, {}).get("ideal_duration", ""),
        "protocol": user_info_dict.get(id, {}).get("protocol", "")
    }
    baseline.append(baseline_)

ml.logger.info("Baseline iteration completed")

bl_df = pd.DataFrame(baseline)
bl_df['last_timestep'] = bl_df['last_timestep'].astype(float)
bl_df['start_timestep'] = bl_df['start_timestep'].astype(float)
bl_df["duration"] = bl_df["last_timestep"] - bl_df["start_timestep"]
bl_df["privacy_score"] = bl_df["duration"]/bl_df["ideal_duration"]
ml.logger.info("Privacy score calculated")
wifi_df = bl_df[bl_df['protocol'] == 'wifi'].reset_index(drop=True)
lte_df = bl_df[bl_df['protocol'] == 'lte'].reset_index(drop=True)

idx = wifi_df.groupby('user_id')['privacy_score'].idxmax()
wifi_df = wifi_df.loc[idx].reset_index(drop=True)

idx = lte_df.groupby('user_id')['privacy_score'].idxmax()
lte_df = lte_df.loc[idx].reset_index(drop=True)
ml.logger.info("Saving WIFI and LTE csv")
wifi_df.to_csv('baseline_wifi.csv', index=False)
lte_df.to_csv('baseline_lte.csv', index=False)
ml.logger.info("Saving data to mongodb - collection reconstruction_baseline")
bl_data = bl_df.to_dict(orient='records')
md.db['reconstruction_baseline'].drop()
md.db['reconstruction_baseline'].insert_many(bl_data)
ml.logger.info("Reconstruction baseline completed")