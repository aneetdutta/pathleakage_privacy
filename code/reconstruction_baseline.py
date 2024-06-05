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
documents = list(md.collection.find())
inter_df = pd.DataFrame(documents)
inter_data = {document['_id']: document['mapping'] for document in documents}

md.set_collection('intra_mappings')
documents = list(md.collection.find({"mapping": {"$size": 1}}))
intra_data = {document['_id']: document['mapping'][0] for document in documents}
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
print(bl_df.to_string())
# non_numeric_rows = bl_df[bl_df['last_timestep'].isna()]

# print("Rows with non-numeric values in 'last_timestep':")
# print(non_numeric_rows)
bl_df['last_timestep'] = bl_df['last_timestep'].astype(float)
bl_df['start_timestep'] = bl_df['start_timestep'].astype(float)
bl_df["duration"] = bl_df["last_timestep"] - bl_df["start_timestep"]
bl_df['privacy_score'] = bl_df.apply(calculate_privacy_score, axis=1)
ml.logger.info("Privacy score calculated")

bluetooth_df = bl_df[bl_df['protocol'] == 'bluetooth'].reset_index(drop=True)
wifi_df = bl_df[bl_df['protocol'] == 'wifi'].reset_index(drop=True)
lte_df = bl_df[bl_df['protocol'] == 'lte'].reset_index(drop=True)

# print(wifi_df.to_string())
idx = wifi_df.groupby('user_id')['privacy_score'].idxmax()
# print(idx.to_string())
wifi_df = wifi_df.loc[idx].reset_index(drop=True)

idx = lte_df.groupby('user_id')['privacy_score'].idxmax()
lte_df = lte_df.loc[idx].reset_index(drop=True)

idx = bluetooth_df.groupby('user_id')['privacy_score'].idxmax()
bluetooth_df = bluetooth_df.loc[idx].reset_index(drop=True)

ml.logger.info("Saving WIFI and LTE csv")
wifi_df.to_csv('csv/baseline_wifi.csv', index=False)
wifi_data = wifi_df.to_dict(orient='records')
md.db['reconstruction_baseline'].insert_many(wifi_data)
lte_df.to_csv('csv/baseline_lte.csv', index=False)
lte_data = lte_df.to_dict(orient='records')
bluetooth_df.to_csv('csv/baseline_bluetooth.csv', index=False)
bluetooth_data = bluetooth_df.to_dict(orient='records')

md.db['reconstruction_baseline'].insert_many(lte_data)
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

    md.db['modified_inter_mappings'].drop()
    md.db['modified_inter_mappings'].insert_many(inter_df.to_dict(orient='records'))
    md.db['modified_intra_mappings'].drop()
    md.db['modified_intra_mappings'].insert_many(intra_df.to_dict(orient='records'))

bl_data = bl_df.to_dict(orient='records')
md.db['reconstruction_baseline'].drop()
md.db['reconstruction_baseline'].insert_many(bl_data)
ml.logger.info("Reconstruction baseline completed")