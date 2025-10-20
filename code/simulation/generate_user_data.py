import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.user import User
from collections import deque
from modules.general import str_to_bool
from modules.general import random_identifier
from modules.general import calculate_distance_l
import polars as pd
from modules.logger import MyLogger
from collections import defaultdict
import json
import time

from line_profiler import profile


@profile
def main():
    SCENARIO_NAME = os.getenv("SCENARIO_NAME")
    DATA_SOURCE = os.getenv("DATA_SOURCE")

    ml = MyLogger(f"generate_user_data_{SCENARIO_NAME}")

    TOTAL_NUMBER_OF_USERS = int(os.getenv("TOTAL_NUMBER_OF_USERS"))
    USER_TIMESTEPS = int(os.getenv("USER_TIMESTEPS"))

    df = pd.read_csv(
        f"data/raw_user_data_{DATA_SOURCE}_{TOTAL_NUMBER_OF_USERS}.csv")  # _{TOTAL_NUMBER_OF_USERS}_filtered.csv")

    # raw_user_data = df.to_dicts()

    same_userset: set = set()

    user_dict = dict()
    user_data = []  # why the fuck a deque? nowhere is this even used

    user_proximity_dict = defaultdict(set)
    user_proximity_refresh_checker = defaultdict()

    for user_ in df.iter_rows(named=True):
        # print(user_)
        user_id = user_["user_id"]
        timestep = user_["timestep"]
        loc_x = user_["loc_x"]
        loc_y = user_["loc_y"]

        user: User
        if user_id in user_dict:  # the fuck? who converts every time a dict to list to test inclusivity?
            user = user_dict[user_id]
            user.location = [loc_x, loc_y]

            if timestep == USER_TIMESTEPS:
                user.transmit_identifiers_force()
            else:
                user.randomize_identifiers()
                user.transmit_identifiers()
        else:
            bluetooth_id = f"{user_id}_B_{random_identifier()}"
            wifi_id = f"{user_id}_W_{random_identifier()}"
            lte_id = f"{user_id}_L_{random_identifier()}"
            user = User(user_id, [loc_x, loc_y], bluetooth_id=bluetooth_id, wifi_id=wifi_id, lte_id=lte_id)
            user_dict[user_id] = user

        user_data.append({
            "timestep": timestep,
            "user_id": user.user_id,
            "loc_x": user.location[0],
            "loc_y": user.location[1],
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

    folder_path = f'data/{SCENARIO_NAME}/'
    file_path = os.path.join(folder_path, f'user_data_{SCENARIO_NAME}.csv')
    os.makedirs(folder_path, exist_ok=True)

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

    df.write_csv(file_path)
