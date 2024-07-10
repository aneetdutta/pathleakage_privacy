import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.sniffer import Sniffer
import traceback
from services.general import extract_orjson, str_to_bool
from collections import deque
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import itertools
from typing import List, Dict, Any
import polars as pl
import pandas as pd

BLUETOOTH_RANGE = int(os.getenv("BLUETOOTH_RANGE"))
WIFI_RANGE = int(os.getenv("WIFI_RANGE"))
LTE_RANGE = int(os.getenv("LTE_RANGE"))
SNIFFER_PROCESSING_BATCH_SIZE = int(os.getenv("SNIFFER_PROCESSING_BATCH_SIZE"))
DB_NAME = os.getenv("DB_NAME")
ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH"))
ENABLE_WIFI = str_to_bool(os.getenv("ENABLE_WIFI"))
ENABLE_LTE = str_to_bool(os.getenv("ENABLE_LTE"))

ENABLE_PARTIAL_COVERAGE = str_to_bool(os.getenv("ENABLE_PARTIAL_COVERAGE"))
LIMIT_USER_AFTER_USER_DATA = str_to_bool(os.getenv("LIMIT_USER_AFTER_USER_DATA"))

# print(BLUETOOTH_RANGE, WIFI_RANGE, LTE_RANGE, SNIFFER_PROCESSING_BATCH_SIZE, ENABLE_BLUETOOTH)

if not ENABLE_PARTIAL_COVERAGE:
    # if ENABLE_BLUETOOTH:
    #     sniffer_location = extract_orjson("data/full_coverage_ble_sniffer_location.json")
    # else:
    ''' SINCE BLE AND WIFI have same coverage now'''
    sniffer_location = extract_orjson("data/full_coverage_wifi_sniffer_location.json")
else:
    print("Partial Coverage enabled")
    sniffer_location = extract_orjson("data/partial_coverage_sniffer_location.json")

if LIMIT_USER_AFTER_USER_DATA:
    raw_user_data_df = pl.read_csv(f"data/user_data_limit_{DB_NAME}.csv")
else:
    raw_user_data_df = pl.read_csv(f"data/user_data_{DB_NAME}.csv")
raw_user_data = raw_user_data_df.to_dicts()

def process_batch(batch: List[Dict[str, Any]], sniffers: List['Sniffer'], enable_bluetooth: bool=ENABLE_BLUETOOTH, enable_wifi: bool=ENABLE_WIFI, enable_lte: bool=ENABLE_LTE) -> deque:
    detected_users = deque()

    # Pre-extracting the required attributes to avoid repetitive dictionary accesses
    # if enable_bluetooth:
    for user_data in batch:
        if not enable_bluetooth:
            user_data["bluetooth_id"] = None
            user_data["transmit_ble"] = False
        if not enable_lte:
            user_data["lte_id"] = None
            user_data["transmit_lte"] = False
        if not enable_wifi:
            user_data["wifi_id"] = None
            user_data["transmit_wifi"] = False
            
        user_location = [user_data["loc_x"], user_data["loc_y"]]
        for sniffer in sniffers:
            a = sniffer.detect_raw_users(
                timestep=user_data["timestep"],
                user_id=user_data["user_id"],
                user_location=user_location,
                user_lte_id=user_data["lte_id"],
                user_wifi_id=user_data["wifi_id"],
                user_bluetooth_id=user_data["bluetooth_id"],
                transmit_ble=user_data["transmit_ble"],
                transmit_wifi=user_data["transmit_wifi"],
                transmit_lte=user_data["transmit_lte"]
            )
            if a:
                detected_users.extend(a)
    # else:
    # for user_data in batch:
    #     user_location = [user_data["loc_x"], user_data["loc_y"]]
    #     for sniffer in sniffers:
    #         a = sniffer.detect_raw_users(
    #             timestep=user_data["timestep"],
    #             user_id=user_data["user_id"],
    #             user_location=user_location,
    #             user_lte_id=user_data["lte_id"],
    #             user_wifi_id=user_data["wifi_id"],
    #             transmit_wifi=user_data["transmit_wifi"],
    #             transmit_lte=user_data["transmit_lte"]
    #         )
    #         if a:
    #             detected_users.extend(a)

    return detected_users


def batch_data(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]

# Simulation loop
detected_users, user_data, users, sniffers = deque(), deque(), dict(), deque()
sniffer_locs = sniffer_location["sniffer_location"]

sniffers = [
    Sniffer(i, sniffer_loc, BLUETOOTH_RANGE, WIFI_RANGE, LTE_RANGE)
    for i, sniffer_loc in enumerate(sniffer_locs)
]

batches = list(batch_data(raw_user_data, SNIFFER_PROCESSING_BATCH_SIZE))

# can add max_workers=nprocs, however was getting same results
with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    futures = [executor.submit(process_batch, batch, sniffers) for batch in batches]
    results = [future.result() for future in futures]

# Combine results from all batches
detected_users = list(itertools.chain.from_iterable(results))

sniffed_file = f"data/sniffed_data_{DB_NAME}.csv"
df = pd.DataFrame(detected_users)
# df.to_csv(sniffed_file, index=False)
df.to_csv(sniffed_file, index=False)

print("Saved file to the directory")

# dump_orjson(sniffed_file, list(detected_users))
