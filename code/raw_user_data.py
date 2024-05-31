import os, sys, libsumo as traci
from datetime import datetime
from modules.sniffer import Sniffer
from modules.user import User
import traceback
from env import *
from services.general import extract_orjson
from services.iteration import user_data_generate
from modules.mongofn import MongoDB
from collections import deque
from services.general import random_identifier
import json
import time

md = MongoDB()

# config_elements = {
#     "area_size": AREA_SIZE,
#     "duration_simulation": DURATION_SIMULATION,
#     "identifier_length": IDENTIFIER_LENGTH,
# }

sumo_cmd = [os.path.join(SUMO_BIN_PATH, "sumo"), "-c", SUMO_CFG_FILE]

''' Start TRACI '''
traci.start(sumo_cmd)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# {timestamp}_user_data_{TIMESTEPS}
user_collection = md.db['user_data']
# {timestamp}_sniffer_data_{TIMESTEPS}

now = time.time()

try:
    # Simulation loop
    user_data, users = deque(), dict()
    timestep = 14400
    '''
    timestep - Get current simulation time
    person_ids - Get list of person IDs
    '''
    now = time.time()
    while timestep < TIMESTEPS:
        timestep = traci.simulation.getTime()
        person_ids = traci.person.getIDList()
        if timestep > 18000:
            print(len(person_ids), timestep)
        user_data, users = user_data_generate(person_ids, users, timestep, user_data)
        traci.simulationStep()
    # Clean up
    print("Time taken: ", time.time() - now)
    traci.close()
    
except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
    traci.close()
    sys.exit(1)

print("Total time take to fetch user_data from sumo_simulation: ", time.time()-now)
# user_file = f"{timestamp}_user_data_{TIMESTEPS}.json"
user_file = "raw_user_data.json"

print("Saved file to the directory")

with open(user_file, "w") as f:
    json.dump(list(user_data), f)

