import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.user import User
from collections import deque
from services.general import str_to_bool
from services.general import random_identifier
import polars as pd
from modules.logger import MyLogger

DB_NAME = os.getenv("DB_NAME")
DATA_USECASE = os.getenv("DATA_USECASE")

ml = MyLogger(f"generate_user_data_{DB_NAME}")

df = pd.read_csv(f"data/raw_user_data_{DATA_USECASE}.csv")
print(df)
raw_user_data = df.to_dicts()

ENABLE_USER_THRESHOLD = str_to_bool(os.getenv("ENABLE_USER_THRESHOLD"))
# GENERATE_SNIFFER_DATA = str_to_bool(os.getenv("GENERATE_SNIFFER_DATA"))
TOTAL_NUMBER_OF_USERS = int(os.getenv("TOTAL_NUMBER_OF_USERS"))

same_userset: set = set()

user_dict = dict()
user_data = deque()

check_users = False

for user_ in raw_user_data:
    # print(user_)
    user_id = user_["user_id"]
    timestep = user_["timestep"]
    mf = user_["mf"]
    loc_x = user_["loc_x"]
    loc_y = user_["loc_y"]
    
    if ENABLE_USER_THRESHOLD:
        # print(ENABLE_USER_THRESHOLD)
        if user_id not in same_userset and len(same_userset) < TOTAL_NUMBER_OF_USERS:
            same_userset.add(user_id)
        elif user_id not in same_userset:
            continue
        
    if len(same_userset) >= TOTAL_NUMBER_OF_USERS and not check_users:
        ml.logger.info(f"Total number of users {len(same_userset)} capped at {timestep}")
        check_users = True
    
    user:User
    if user_id in list(user_dict):
        user = user_dict[user_id]
        user.location = [loc_x, loc_y]
        user.mf = mf
        user.randomize_identifiers()
        user.transmit_identifiers()
    else:
        bluetooth_id=random_identifier()
        wifi_id=random_identifier()
        lte_id=random_identifier()
        user = User(user_id,[loc_x,loc_y],bluetooth_id=bluetooth_id, wifi_id=wifi_id, lte_id=lte_id, mf=mf) 
        user_dict[user_id] = user
    
    user_data.append({
        "timestep": timestep,
        "user_id": user.user_id,
        "loc_x": user.location[0],
        "loc_y": user.location[1],
        "mf": user.mf,
        "bluetooth_id": user.bluetooth_id,
        "wifi_id": user.wifi_id,
        "lte_id": user.lte_id,
        "transmit_ble": user.transmit_bluetooth,
        "transmit_wifi": user.transmit_wifi,
        "transmit_lte": user.transmit_lte,
        "randomized_ble": user.randomized_bluetooth,
        "randomized_wifi": user.randomized_wifi,
        "randomized_lte": user.randomized_lte,
    })

user_file = f"data/user_data_{DB_NAME}.csv"
print("Saved file to the directory")
df = pd.DataFrame(list(user_data))
columns_to_replace = ['randomized_ble', 'randomized_wifi', 'randomized_lte']

for col_name in columns_to_replace:
    df = df.with_columns(
        pd.when(pd.col(col_name) == False)
        .then(None)
        .otherwise(pd.col(col_name))
        .alias(col_name)
    )
# print(df['randomized_ble'])
df.write_csv(user_file)
