import sys, libsumo as traci
from modules.sniffer import Sniffer
import traceback
from env import *
from services.general import extract_orjson, dump_orjson
from collections import deque
import json

sniffer_location = extract_orjson("new_sniffer_location.json")
raw_user_data = extract_orjson("user_data.json")

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

    """
    timestep - Get current simulation time
    person_ids - Get list of person IDs
    """
    detected_users = []
    for user_data in raw_user_data:
        # print(user_data["timestep"])
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