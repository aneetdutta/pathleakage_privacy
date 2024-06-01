import sys, libsumo as traci
from modules.sniffer import Sniffer
import traceback
from env import *
from services.general import extract_orjson, dump_orjson
from collections import deque
import json
from concurrent.futures import ProcessPoolExecutor


sniffer_location = extract_orjson("new_sniffer_location.json")
raw_user_data = extract_orjson("user_data.json")

def process_batch(batch, sniffers):
    detected_users = []
    for user_data in batch:
        sniffer: Sniffer
        for sniffer in sniffers:
            detected_users.extend(
                sniffer.detect_raw_users(
                    timestep=user_data["timestep"],
                    user_id=user_data["user_id"],
                    user_location=user_data["location"],
                    user_lte_id=user_data["lte_id"],
                    user_wifi_id=user_data["wifi_id"],
                )
            )
    return detected_users

def batch_data(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
        
batch_size = 100

        

import time

now = time.time()



try:
    # Simulation loop
    detected_users, user_data, users, sniffers = deque(), deque(), dict(), deque()
    sniffer_locs = (
        sniffer_location["sniffer_location"]# + sniffer_location2["sniffer_location"]
    )
    sniffers = [
        Sniffer(i, sniffer_loc, BLUETOOTH_RANGE, WIFI_RANGE, LTE_RANGE)
        for i, sniffer_loc in enumerate(sniffer_locs)
    ]
    
    batches = list(batch_data(raw_user_data, batch_size))


    """
    timestep - Get current simulation time
    person_ids - Get list of person IDs
    """
    
    # can add max_workers=nprocs, however was getting same results
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_batch, batch, sniffers) for batch in batches]
        results = [future.result() for future in futures]

    # Combine results from all batches
    detected_users = [user for result in results for user in result]
            
    traci.close()

except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
    traci.close()
    sys.exit(1)


print("Total time take to fetch sniffer_data from user_data: ", time.time()-now)

sniffed_file = "sniffed_data.json"

print("Saved file to the directory")

dump_orjson(sniffed_file, list(detected_users))