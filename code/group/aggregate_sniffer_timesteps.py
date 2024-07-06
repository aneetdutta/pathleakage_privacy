import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from env import *
import numpy as np
from services.general import str_to_bool
import pandas as pd
from collections import deque
from modules.mongofn import MongoDB
md = MongoDB()
# Path to the gzipped CSV file
DB_NAME = os.getenv("DB_NAME")
compressed_file_path = f"data/sniffed_data_{DB_NAME}.csv"

BLUETOOTH_MAX_TRANSMIT = int(os.getenv("BLUETOOTH_MAX_TRANSMIT"))
WIFI_MAX_TRANSMIT = int(os.getenv("WIFI_MAX_TRANSMIT"))
LTE_MAX_TRANSMIT = int(os.getenv("LTE_MAX_TRANSMIT"))
SNIFFER_TIMESTEP = max(BLUETOOTH_MAX_TRANSMIT, WIFI_MAX_TRANSMIT, LTE_MAX_TRANSMIT)
ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH"))
# print(SNIFFER_TIMESTEP)

# Decompress and read the CSV file
df = pd.read_csv(compressed_file_path)
# print(df)
df["dist_S_U"] = (np.sqrt(((df["sl_x"] - df["ul_x"]) ** 2 + (df["sl_y"] - df["ul_y"]) ** 2))).astype(int)
# Drop the specified columns
df = df.drop(columns=['sl_x', 'sl_y'])
# sys.exit()
earliest_timestep = df['timestep'].min()
last_timestep = df['timestep'].max()
# print(earliest_timestep)
timestep_bins = np.arange(earliest_timestep, last_timestep, SNIFFER_TIMESTEP)
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
# print(df)
# user_df_ = df.sort_values('st_window').groupby('user_id')

# for user_id, user_df in user_df_:
#     print(user_id)
#     print(user_df)
#     window_df = user_df.groupby('st_window')
#     for window in window_df:
#         print(window[0], window[1])
#         break
#     break
    
max_st_window_df = df.groupby('user_id')['st_window'].max().reset_index()

merged_df = pd.merge(df, max_st_window_df, on=['user_id', 'st_window'])
grouped_df = merged_df.groupby(['user_id']).agg({'protocol': set, 'st_window': 'first'}).reset_index()
if ENABLE_BLUETOOTH:
    filtered_df = grouped_df[grouped_df['protocol'].apply(lambda x: 'LTE' not in x or 'WiFi' not in x or 'Bluetooth' not in x)]
else:
    filtered_df = grouped_df[grouped_df['protocol'].apply(lambda x: 'LTE' not in x or 'WiFi' not in x)]

to_remove = pd.merge(df, filtered_df[['user_id', 'st_window']], on=['user_id', 'st_window'])
# to_remove = pd.merge(df, filtered_df[['user_id', 'st_window']], on=['user_id', 'st_window'], how='left', indicator=True)
# Remove those rows from the original DataFrame
# df = df[~df.index.isin(to_remove.index)]
df = df[~df.set_index(['user_id', 'st_window']).index.isin(to_remove.set_index(['user_id', 'st_window']).index)]

# print(last_timestep_df)

'''Problems statement:
To fetch the last st_window of every user and if multiprotocols do not exists for that user; delete that user'''

data_dict = df.to_dict(orient='records')
# print(data_dict)
md.db["parsed_sniffed_data"].drop()
md.db["parsed_sniffed_data"].insert_many(data_dict)

# print(df.dtypes)

md.set_collection("parsed_sniffed_data")