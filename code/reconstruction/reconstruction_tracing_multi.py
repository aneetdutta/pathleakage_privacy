import os, sys
sys.path.append(os.getcwd())
from modules.general import *
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
import polars as pl
from tqdm import tqdm
from modules.logger import MyLogger


SCENARIO_NAME = os.getenv("SCENARIO_NAME")
ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH"))
ENABLE_WIFI = str_to_bool(os.getenv("ENABLE_WIFI"))
ENABLE_LTE = str_to_bool(os.getenv("ENABLE_LTE"))

ml = MyLogger(f"reconstruction_multi_{SCENARIO_NAME}")

df = pl.read_parquet(f"data/{SCENARIO_NAME}/aggregated_id_{SCENARIO_NAME}.parquet")
id_data = df.to_pandas()
id_protocol = {row['id']: row['protocol'] for _, row in id_data.iterrows()}
id_user_data = {row['id']: row['user_id'] for _, row in id_data.iterrows()}
id_timestep_data = {row['id']: (row['start_timestep'], row['last_timestep'])     for _, row in id_data.iterrows()
}

inter_data = np.load(f'data/{SCENARIO_NAME}/refined_intermap_{SCENARIO_NAME}.npy', allow_pickle=True).item()
intra_data = np.load(f'data/{SCENARIO_NAME}/refined_intramap_{SCENARIO_NAME}.npy', allow_pickle=True).item()


user_df = pl.read_parquet(f"data/{SCENARIO_NAME}/aggregated_users_{SCENARIO_NAME}.parquet")
user_df = user_df.to_pandas()
user_data = {row['user_id']: row['ids'] for _, row in user_df.iterrows()}
user_time_data = {row['user_id']: row['last_timestep'] for _, row in user_df.iterrows()}
# user_df = user_df.drop(['sniffer_list', '_id', 'trace'])

'''

        Baseline Below 

'''

if ENABLE_WIFI:
    wifi_df = id_data[id_data['protocol'] == 'WiFi'].reset_index(drop=True)
    wifi_df = pd.merge(wifi_df, user_df[['user_id', 'wifi_duration']], left_on='user_id', right_on='user_id', how='left')
    wifi_df['privacy_score'] = wifi_df.apply(
        lambda row: calculate_privacy_score_single(row, 'wifi_duration'), axis=1
    )
    idx = wifi_df.groupby('user_id')['privacy_score'].idxmax()
    wifi_df = wifi_df.loc[idx].reset_index(drop=True)
else:
    wifi_df = None

if ENABLE_LTE:
    lte_df = id_data[id_data['protocol'] == 'LTE'].reset_index(drop=True)
    lte_df = pd.merge(lte_df, user_df[['user_id', 'lte_duration']], left_on='user_id', right_on='user_id', how='left')
    lte_df['privacy_score'] = lte_df.apply(
        lambda row: calculate_privacy_score_single(row, 'lte_duration'), axis=1
    )
    idx = lte_df.groupby('user_id')['privacy_score'].idxmax()
    lte_df = lte_df.loc[idx].reset_index(drop=True)
else:
    lte_df = None

if ENABLE_BLUETOOTH:
    bluetooth_df = id_data[id_data['protocol'] == 'Bluetooth'].reset_index(drop=True)
    bluetooth_df = pd.merge(bluetooth_df, user_df[['user_id', 'ble_duration']], left_on='user_id', right_on='user_id', how='left')
    bluetooth_df['privacy_score'] = bluetooth_df.apply(
        lambda row: calculate_privacy_score_single(row, 'ble_duration'), axis=1
    )
    idx = bluetooth_df.groupby('user_id')['privacy_score'].idxmax()
    bluetooth_df = bluetooth_df.loc[idx].reset_index(drop=True)
else:
    bluetooth_df = None

folder_path = f'output/data/{SCENARIO_NAME}/'
os.makedirs(folder_path, exist_ok=True)


if ENABLE_WIFI:
    file_path = os.path.join(folder_path, f'baseline_wifi_{SCENARIO_NAME}.csv')
    wifi_df.to_csv(file_path, index=False)
if ENABLE_LTE:
    file_path = os.path.join(folder_path, f'baseline_lte_{SCENARIO_NAME}.csv')
    lte_df.to_csv(file_path, index=False)
if ENABLE_BLUETOOTH:
    file_path = os.path.join(folder_path, f'baseline_ble_{SCENARIO_NAME}.csv')
    bluetooth_df.to_csv(file_path, index=False)

ml.logger.info("Baseline Privacy score calculated")

''' 
        Multi Protocol Mapping Below 
'''

print("Loaded and Multiprotocol reconstruction started")
intra_single = {}
for id, mapping in intra_data.items():
    if len(mapping) > 1:
        intra_single[id] = ''
    elif mapping:
        intra_single[id] = mapping[0]
    else:
        intra_single[id] = ''

print("Computing all possible chains")
'''  Generate all possible chains in form of list of lists of intra mappings '''
chained_intra = find_all_possible_chains(intra_single)

chained_dict = {char: lst for lst in chained_intra for char in lst}
corresponding_users = set()
multi_protocol = []

ml.logger.info("Reconstruction started")
print("Reconstruction started")
incorrectness = defaultdict(set)
total_rows = len(inter_data)
reconstructed_inter = {}

''' Iterate through all inter mappings assuming that inter consists of all ids '''
for inter_id in tqdm(inter_data, total=len(inter_data)):
    mapping = inter_data[inter_id]
    u = id_user_data[inter_id]
    min_start_timestep, max_last_timestep = id_timestep_data[inter_id][0], id_timestep_data[inter_id][1]
    
    ''' Get the intra chain for that inter id '''
    if inter_id in chained_dict:
        chain1 = chained_dict[inter_id]
    else:
        chain1 = []
    # user_id_match = inter_row["user_id_match"]
    ''' Get the chain for every protocol mapping of the inter id '''
    chain_ = inter_intra_mapper(mapping, chained_intra)

    ''' Append all these chains so that we have now chain of each protocol mapping to ideally same user id '''
    chain_.append(chain1)
    
    user_id_ = None
    lchain = []
    
    '''Due to computation this becomes slower, so we directly use the user_id available with the inter to verify the corrcetness'''
    ids = user_data[id_user_data[inter_id]]
    ''' Considering all protocols ids matching the user id (finally verification) '''
    for i, c in enumerate(chain_):
        if not c:
            continue
        if set(c).issubset(ids):
            lchain.extend(c)
        else:
            incorrectness[inter_id].update(c)
            corresponding_users.add(u)
    
    if not lchain:
        ''' Consider baseline'''
        reconstructed_inter[inter_id] = [inter_id]
        continue
    
    ''' Deriving final longest chain of ids (contains all protocol ids) '''
    reconstructed_inter[inter_id] = lchain
    

ml.logger.info("Processing now")
print("Processing now")
for inter_id in tqdm(reconstructed_inter, total=len(reconstructed_inter)):
    rchain = reconstructed_inter[inter_id]
    min_start_timestep, max_last_timestep, protocol_ = id_timestep_data[inter_id][0], id_timestep_data[inter_id][1], id_protocol[inter_id]
    u = id_user_data[inter_id]
    
    fetch_inter_mapping_timesteps = id_data[id_data['id'].isin(rchain)]
    min_start_timestep = min(fetch_inter_mapping_timesteps['start_timestep'].min(), min_start_timestep)
    max_last_timestep = max(fetch_inter_mapping_timesteps['last_timestep'].max(), max_last_timestep)

    duration = max_last_timestep - min_start_timestep + 1
    ''' Fetch min and max of rchain and process it '''
    multi_protocol.append({"id": inter_id, "start_timestep": min_start_timestep, "last_timestep": max_last_timestep, "total_time": duration, "user_id": u, "protocol": protocol_})

ml.logger.info(f"{len(incorrectness)} total incorrectness and {len(corresponding_users)} incorrect users")
print(f"{len(incorrectness)} total incorrectness and {len(corresponding_users)} incorrect users")
ml.logger.info(f"{incorrectness} incorrect mappings, {corresponding_users} incorrect users")

print("completed")
multi_protocol_df = pd.DataFrame(multi_protocol)
ml.logger.info(multi_protocol_df)
multi_protocol_df = pd.merge(multi_protocol_df, user_df[['user_id', 'ideal_duration']], left_on='user_id', right_on='user_id', how='left')
multi_protocol_df = pd.merge(multi_protocol_df, user_df[['user_id']], left_on='user_id', right_on='user_id', how='left')

multi_protocol_df['privacy_score'] = multi_protocol_df.apply(calculate_privacy_score, axis=1)
idx = multi_protocol_df.groupby('user_id')['privacy_score'].idxmax()
multi_protocol_df = multi_protocol_df.loc[idx].reset_index(drop=True)

multi_data = multi_protocol_df.to_dict(orient='records')

folder_path = f'output/data/{SCENARIO_NAME}/'
os.makedirs(folder_path, exist_ok=True)

multi_protocol_df.to_csv(f'{folder_path}multi_protocol_{SCENARIO_NAME}.csv', index=False)
