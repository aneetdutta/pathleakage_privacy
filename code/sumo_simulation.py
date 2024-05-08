import os, sys, libsumo as traci, csv, random, string, json, time
from datetime import datetime

from numpy import int64
from modules.sniffer import Sniffer
from modules.user import User
import traceback
from env import *
import polars as pl

from collections import deque

# from numba import jit
# from numba.typed import List

config_elements = {
    "area_size": AREA_SIZE,
    "duration_simulation": DURATION_SIMULATION,
    "identifier_length": IDENTIFIER_LENGTH,
}

# sumo_cmd = [sumo_binary, "-c", "most.sumocfg"]
# sumo_process = subprocess.Popen(sumo_cmd, stdout=sys.stdout, stderr=sys.stderr)

sumo_cmd = [os.path.join(SUMO_BIN_PATH, "sumo"), "-c", SUMO_CFG_FILE]

traci.start(sumo_cmd)
# Connect to TraCI
# traci.connect()

def person_iterator(p_ids:deque, users:dict, sniffers:deque, timestep:float, usr_data: deque, detected_usrs: deque):
    # Iterate over each person ID
    for person_id in p_ids:
        user:User
        if person_id in users:
            # user exists
            user = users[person_id]
            user.location = traci.person.getPosition(person_id)
            user.randomize_identifiers()
        else:
            user_id = person_id
            location = traci.person.getPosition(person_id)
            user = User(user_id,location,max_step_size=MAX_STEP_SIZE)              
            users[user_id] = user
            
        sniffer: Sniffer
        for sniffer in sniffers:
            detected_usrs.extend(sniffer.detect_users(user, timestep))

        usr_data.append({
                "timestep": timestep,
                "user_id": user.user_id,
                "location": user.location,
                "bluetooth_id": user.bluetooth_id,
                "wifi_id": user.wifi_id,
                "lte_id": user.lte_id,
            })

    return usr_data, detected_usrs

try:
    # Simulation loop
    detected_users, user_data, users, sniffers = deque(), deque(),dict(), deque()
    
    timestep = 14400
    sniffer_locs=[(9832.86,5109.03),(3075.86,686.18),(4749.59,1973.95),(5053.60,2440.58),(4106.14,1580.96),(5022.89,2397.47),(2447.68,335.84),(1541.62,594.71),(2333.54,663.48),(4823.42,2244.27),(8251.47,4557.67),(5085.25,2361.61)]
    sniffers = [Sniffer(i, sniffer_loc, BLUETOOTH_RANGE, WIFI_RANGE, LTE_RANGE) for i, sniffer_loc in enumerate(sniffer_locs)]

    '''
    timestep - Get current simulation time
    person_ids - Get list of person IDs
    '''
    while timestep < TIMESTEPS:
        timestep = traci.simulation.getTime()
        person_ids = traci.person.getIDList()
        if timestep > 18000 and timestep % 50 == 0:
            print(len(person_ids), timestep)
        user_data, detected_users = person_iterator(person_ids, users, sniffers, timestep, user_data, detected_users)
        # print(detected_users)
        traci.simulationStep()

    # Clean up
    traci.close()
    
except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
    traci.close()
    sys.exit(1)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
user_file = f"{timestamp}_user_data_{TIMESTEPS}.json"
sniffed_file = f"{timestamp}_sniffed_data_{TIMESTEPS}.json"

print("Saved file to the directory")

with open(user_file, "w") as f:
    json.dump(list(user_data), f)

with open(sniffed_file, "w") as f:
    json.dump(list(detected_users), f)

