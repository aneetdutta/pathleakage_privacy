import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.sniffer import Sniffer
import traceback
from env import *
from services.general import extract_orjson
from collections import deque
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import itertools
from typing import List, Dict, Any
import polars as pl
import pandas as pd

sniffer_location = extract_orjson("data/new_sniffer_location.json")
raw_user_data_df = pl.read_csv("data/user_data.csv")
raw_user_data = raw_user_data_df.to_dicts()

def process_batch(batch: List[Dict[str, Any]], sniffers: List['Sniffer'], enable_bluetooth: bool=ENABLE_BLUETOOTH) -> deque:
    detected_users = deque()
    
    # Pre-extracting the required attributes to avoid repetitive dictionary accesses
    if enable_bluetooth:
        for user_data in batch:
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
    else:
        for user_data in batch:
            user_location = [user_data["loc_x"], user_data["loc_y"]]
            for sniffer in sniffers:
                a = sniffer.detect_raw_users(
                    timestep=user_data["timestep"],
                    user_id=user_data["user_id"],
                    user_location=user_location,
                    user_lte_id=user_data["lte_id"],
                    user_wifi_id=user_data["wifi_id"],
                    transmit_wifi=user_data["transmit_wifi"],
                    transmit_lte=user_data["transmit_lte"]
                )
                if a:
                    detected_users.extend(a)

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

sniffed_file = "data/sniffed_data.csv"
df = pd.DataFrame(detected_users)
# df.to_csv(sniffed_file, index=False)
df.to_csv(sniffed_file, index=False)

print("Saved file to the directory")

# dump_orjson(sniffed_file, list(detected_users))
