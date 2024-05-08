import os, sys, libsumo as traci, csv, random, string, json, time
from datetime import datetime
from modules.sniffer import Sniffer
from modules.user import User
import traceback
from env import *
from funct.fn import random_identifier
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

# Open CSV file for writing
# csv_file = open("person_locations.csv", "w", newline='')
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(["Timestep", "PersonID", "X", "Y"])
    
# @jit(parallel=True)
def person_iterator(p_ids:deque, users:deque, sniffers:deque, timestep:deque, user_data:deque, detected_usrs: deque):
    # Iterate over each person ID
    for person_id in p_ids:
        # Get person's position
        # import time
        # now = time.time()
        user_exists = next((user for user in users if user.user_id == person_id), None) # can be optimized
        # print(time.time() - now, timestep)
        
        user_exists:User
        if user_exists:
            user_exists.location = traci.person.getPosition(person_id)
            user_exists.randomize_identifiers()
            sniffer:Sniffer
            for sniffer in sniffers:
                detected_usrs = sniffer.detect_users(user_exists, timestep, detected_usrs)
            user_data.extend([
                {
                    "timestep": timestep,
                    "user_id": user_exists.user_id,
                    "location": user_exists.location,
                    "bluetooth_id": user_exists.bluetooth_id,
                    "wifi_id": user_exists.wifi_id,
                    "lte_id": user_exists.lte_id,
                }]
            )
        else:
            user_id = person_id
            location = traci.person.getPosition(person_id)
            user = User(
                user_id,
                location,
                max_step_size=MAX_STEP_SIZE,
            )                
            users.extend([user]) #data structure can be changed to dict
            sniffer:Sniffer
            for sniffer in sniffers:
                detected_usrs = sniffer.detect_users(user, timestep, detected_usrs)
            user_data.extend([
                {
                    "timestep": timestep,
                    "user_id": user.user_id,
                    "location": user.location,
                    "bluetooth_id": user.bluetooth_id,
                    "wifi_id": user.wifi_id,
                    "lte_id": user.lte_id,
                }]
            )
    return user_data, detected_usrs

try:
    # Simulation loop
    detected_users, user_data, users, sniffers = deque(), deque(),deque(), deque()
    timestep = 14400
    sniffer_locs=[(9832.86,5109.03),(3075.86,686.18),(4749.59,1973.95),(5053.60,2440.58),(4106.14,1580.96),(5022.89,2397.47),(2447.68,335.84),(1541.62,594.71),(2333.54,663.48),(4823.42,2244.27),(8251.47,4557.67),(5085.25,2361.61)]
    for i in range(len(sniffer_locs)):
        sniffers.extend([Sniffer(i, sniffer_locs[i], BLUETOOTH_RANGE, WIFI_RANGE, LTE_RANGE)])

    '''
    timestep - Get current simulation time
    person_ids - Get list of person IDs
    '''
    while timestep < TIMESTEPS: #18400:
        timestep = traci.simulation.getTime()
        # print(timestep)
        person_ids = traci.person.getIDList()
        if timestep > 18300:
            print(len(person_ids), timestep)
        
        user_data, detected_users = person_iterator(person_ids, users, sniffers, timestep, user_data, detected_users)
        # Advance simulation
        traci.simulationStep()

    # Clean up
    traci.close()
    # csv_file.close()
    # sys.exit()

except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
    traci.close()
    # csv_file.close()
    sys.exit(1)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
user_file = f"{timestamp}_user_data_{TIMESTEPS}.json"
sniffed_file = f"{timestamp}_sniffed_data_{TIMESTEPS}.json"

print("Saved file to the directory")
with open(user_file, "w") as f:
    json.dump(list(user_data), f)

with open(sniffed_file, "w") as f:
    json.dump(list(detected_users), f)
