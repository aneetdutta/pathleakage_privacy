import os, sys, libsumo as traci
from datetime import datetime
from modules.sniffer import Sniffer
from modules.user import User
import traceback
from env import *
from services.general import extract_orjson
from services.iteration2 import person_iterator
from modules.mongofn import MongoDB
from collections import deque
from services.general import random_identifier
import uuid
import json
from bson.objectid import ObjectId


sniffer_location = extract_orjson("sniffer_location.json")
sniffer_location2 = extract_orjson("sniffer_location2.json")
raw_user_data = extract_orjson("raw_user_data.json")

import time

now = time.time()


try:
    # Simulation loop
    detected_users, user_data, users, sniffers = deque(), deque(), dict(), deque()
    sniffer_locs = (
        sniffer_location["sniffer_location"] + sniffer_location2["sniffer_location"]
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


sniffed_file = "raw_sniffed_data.json"

print("Saved file to the directory")

with open(sniffed_file, "w") as f:
    json.dump(list(detected_users), f)

