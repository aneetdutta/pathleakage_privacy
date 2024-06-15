import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import *
import numpy as np
import json
import pandas as pd
from collections import deque
from modules.mongofn import MongoDB
md = MongoDB()
# Path to the gzipped CSV file
compressed_file_path = "data/sniffed_data.csv"
# Decompress and read the CSV file
df = pd.read_csv(compressed_file_path)
df["dist_S_U"] = (np.sqrt(((df["sl_x"] - df["ul_x"]) ** 2 + (df["sl_y"] - df["ul_y"]) ** 2))).astype(int)
# Drop the specified columns
df = df.drop(columns=['sl_x', 'sl_y', 'ul_x', 'ul_y', 'user_id'])
# sys.exit()
earliest_timestep = df['timestep'].min()
last_timestep = df['timestep'].max()
# print(earliest_timestep)
timestep_bins = np.arange(earliest_timestep, last_timestep+SNIFFER_TIMESTEP, SNIFFER_TIMESTEP)
timestep_bin_list = np.arange(len(timestep_bins))
timestep_bin_list_trimmed = timestep_bin_list[:-1]
df.loc[:, 'st_window'] = pd.cut(df['timestep'], bins=timestep_bins, labels=timestep_bin_list_trimmed, right=False)

# Aggregate the results into the desired format
# df['timestep'] = df['timestep']
df['protocol'] = df['protocol'].astype(str)
df['id'] = df['id'].astype(str)
df['sniffer_id'] = df['sniffer_id'].astype(str)
df['dist_S_U'] = df['dist_S_U'].astype(str)

data_dict = df.to_dict(orient='records')
md.db["temp_agg"].insert_many(data_dict)

# print(df.dtypes)

md.set_collection("temp_agg")
md.db['aggregated_sniffer'].drop()
md.db['aggregated_sniffer'].insert_many(md.aggregate_st_window())


# df_sorted = df.sort_values(by='timestep').reset_index(drop=True)
# # Step 2: Determine the earliest timestep for each sniffer_id
# earliest_timesteps = df_sorted.groupby('sniffer_id')['timestep'].min().reset_index()
# # Step 3: Sort the sniffer_ids by their earliest timestep
# sorted_sniffer_ids = earliest_timesteps.sort_values(by='timestep')['sniffer_id']
# # Step 4: Create a grouped DataFrame based on the sorted sniffer_ids
# grouped_sorted = {sniffer_id: df_sorted[df_sorted['sniffer_id'] == sniffer_id] for sniffer_id in sorted_sniffer_ids}
# # Example: Printing grouped DataFrames
# aggregated_sniffer = deque()

# sniffer_group: pd.DataFrame
# for sniffer_id, sniffer_group in grouped_sorted.items():
#     sniffer_group.loc[:, 'st_window'] = pd.cut(sniffer_group['timestep'], bins=timestep_bins, labels=timestep_bin_list_trimmed, right=False)
#     grouped_dicts = (
#         sniffer_group.groupby('st_window')
#         .apply(lambda x: {"st_window": x['st_window'].iloc[0], "data": x.drop(columns=['st_window','sniffer_id']).to_dict(orient='records')} if not x.empty else None)
#         .dropna()
#         .to_list()
#     )
#     grouped_dicts = json.loads(json.dumps(list(grouped_dicts), default=str))
#     aggregated_sniffer.append({"sniffer_id": str(sniffer_id), "data": grouped_dicts})


# md.db['aggregated_sniffer'].drop()
# md.db['aggregated_sniffer'].insert_many(aggregated_sniffer)


