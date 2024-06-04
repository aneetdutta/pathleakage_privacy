from services.general import *
from modules.mongofn import MongoDB
from collections import defaultdict

""" Load the sumo_simulation result from mongodb """
from services.general import UnionFind
import pandas as pd
from env import TIMESTEPS
import sys
from modules.logger import MyLogger

ml = MyLogger("reconstruction_baseline_random")
# import sys
md = MongoDB()

md.set_collection("baseline_intra_mappings")
documents = list(md.collection.find({"mapping": {"$size": 1}}))
intra_data = {}
for document in documents:
    intra_data[document["_id"]] = document["mapping"][0]

md.set_collection("inter_mappings")
documents = md.collection.find()
inter_df = pd.DataFrame(documents)

md.set_collection("reconstruction_baseline")
documents = md.collection.find()
baseline_data = pd.DataFrame(documents)

ml.logger.info("MongoDB data loaded")

merge_columns_inter = ["id","start_timestep","last_timestep","duration","user_id","ideal_duration","protocol",]
merge_columns_intra = ["id","start_timestep", "last_timestep", "duration"]

inter_df = (
    pd.merge(
        inter_df,
        baseline_data[merge_columns_inter],
        left_on="_id",
        right_on="id",
        how="left",
    )
    .drop(columns=["id"])
    .sort_values(by="start_timestep")
)


baseline_random = []

visited_set = set()
for index, inter_row in inter_df.iterrows():
    inter_id = inter_row["_id"]

    ml.logger.info(f'{index}, {inter_id}, {inter_row["user_id"]}, {inter_row["protocol"]}')

    if inter_id in visited_set:
        continue
    visited_set.add(inter_id)
    
    if inter_id in intra_data:
        chain = find_chain_for_key(intra_data, inter_id)
        """ chain is ordered - assuming"""
        # print(chain)
        chain = chain[0]
        id_df = inter_df[inter_df["_id"].isin(chain)]
        id_df = id_df.drop(columns=["mapping"])
        count_timesteps = sum(
            id_df[id_df["_id"].isin(chain)]["last_timestep"] == TIMESTEPS
        )
        for id in reversed(chain):
            if (
                count_timesteps > 1
                and id_df[id_df["_id"] == id]["last_timestep"].values[0] == TIMESTEPS
            ):
                chain.remove(id)
                id_df = id_df[id_df["_id"] != id]
                count_timesteps -= 1
        min_start_timestep = id_df["start_timestep"].min()
        max_last_timestep = id_df["last_timestep"].max()
        visited_set.update(set(chain))
    else:
        min_start_timestep = inter_row["start_timestep"]
        max_last_timestep = inter_row["last_timestep"]

    duration = max_last_timestep - min_start_timestep
    baseline_random.append(
        {
            "id": inter_id,
            "start_timestep": min_start_timestep,
            "last_timestep": max_last_timestep,
            "duration": duration,
            "ideal_duration": inter_row["ideal_duration"],
            "user_id": inter_row["user_id"],
            "protocol": inter_row["protocol"],
        }
    )

ml.logger.info(f"Iteration completed - calculating privacy score")

baseline_random_df = pd.DataFrame(baseline_random)

baseline_random_df["privacy_score"] = (
    baseline_random_df["duration"] / baseline_random_df["ideal_duration"]
)

ml.logger.info(f"Splitting into Wifi and LTE data")

wifi_df = baseline_random_df[baseline_random_df["protocol"] == "wifi"].reset_index(
    drop=True
)

lte_df = baseline_random_df[baseline_random_df["protocol"] == "lte"].reset_index(
    drop=True
)

idx = wifi_df.groupby("user_id")["privacy_score"].idxmax()
wifi_df = wifi_df.loc[idx].reset_index(drop=True)

idx = lte_df.groupby("user_id")["privacy_score"].idxmax()
lte_df = lte_df.loc[idx].reset_index(drop=True)

unique_users_df1 = set(wifi_df["user_id"])
unique_users_df2 = set(lte_df["user_id"])

missing_user_in_df2 = unique_users_df2 - unique_users_df1

ml.logger.info("Missing user in df2:", missing_user_in_df2)

ml.logger.info(f"Saving WIFI and LTE CSV data")

wifi_df.to_csv("csv/baseline_random_wifi.csv", index=False)
lte_df.to_csv("csv/baseline_random_lte.csv", index=False)

# bl_data = baseline_random_df.to_dict(orient='records')
# md.db['reconstruction_baseline'].drop()
# md.db['reconstruction_baseline'].insert_many(bl_data)


# multi_protocol_df["privacy_score"] = multi_protocol_df["duration"]/multi_protocol_df["ideal_duration"]
