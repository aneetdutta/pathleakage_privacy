import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from env import *
import numpy as np
import json
import pandas as pd
from collections import deque
from modules.mongofn import MongoDB
md = MongoDB()
# Path to the gzipped CSV file
DB_NAME = os.getenv("DB_NAME")
compressed_file_path = f"data/sniffed_data_{DB_NAME}.csv"
# Decompress and read the CSV file
df = pd.read_csv(compressed_file_path)
df["dist_S_U"] = (np.sqrt(((df["sl_x"] - df["ul_x"]) ** 2 + (df["sl_y"] - df["ul_y"]) ** 2))).astype(int)
# Drop the specified columns
df = df.drop(columns=['sl_x', 'sl_y', 'ul_x', 'ul_y'])
# sys.exit()
earliest_timestep = df['timestep'].min()
last_timestep = df['timestep'].max()
# print(earliest_timestep)
timestep_bins = np.arange(earliest_timestep, last_timestep, os.getenv("SNIFFER_TIMESTEP"))
timestep_bin_list = np.arange(len(timestep_bins))
print(timestep_bins)
timestep_bin_list_trimmed = timestep_bin_list[:-1]
df.loc[:, 'st_window'] = pd.cut(df['timestep'], bins=timestep_bins, labels=timestep_bin_list_trimmed, right=False)

df = df.dropna(subset=['st_window'])

# Aggregate the results into the desired format
# df['timestep'] = df['timestep']
df['protocol'] = df['protocol'].astype(str)
df['id'] = df['id'].astype(str)
df['sniffer_id'] = df['sniffer_id'].astype(str)
df['dist_S_U'] = df['dist_S_U'].astype(str)

data_dict = df.to_dict(orient='records')
md.db["temp_agg"].drop()
md.db["temp_agg"].insert_many(data_dict)

# print(df.dtypes)

md.set_collection("temp_agg")
md.db['aggregated_sniffer'].drop()
md.db['aggregated_sniffer'].insert_many(md.aggregate_st_window())