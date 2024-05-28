import os, sys, libsumo as traci
from datetime import datetime
from modules.sniffer import Sniffer
from modules.user import User
import traceback
from env import *
from services.general import extract_orjson
from services.iteration import person_iterator
from modules.mongofn import MongoDB
from collections import deque
from services.general import random_identifier
import uuid
from bson.objectid import ObjectId

md = MongoDB()

config_elements = {
    "area_size": AREA_SIZE,
    "duration_simulation": DURATION_SIMULATION,
    "identifier_length": IDENTIFIER_LENGTH,
}

sniffer_location = extract_orjson("sniffer_location.json")

sumo_cmd = [os.path.join(SUMO_BIN_PATH, "sumo"), "-c", SUMO_CFG_FILE]

''' Start TRACI '''
traci.start(sumo_cmd)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# {timestamp}_user_data_{TIMESTEPS}
user_collection = md.db['user_data']
# {timestamp}_sniffer_data_{TIMESTEPS}
sniffer_collection = md.db['sniffer_data']

try:
    # Simulation loop
    detected_users, user_data, users, sniffers = deque(), deque(),dict(), deque()
    timestep = 14400
    sniffer_locs= sniffer_location["sniffer_location"]
    sniffers = [Sniffer(i, sniffer_loc, BLUETOOTH_RANGE, WIFI_RANGE, LTE_RANGE) for i, sniffer_loc in enumerate(sniffer_locs)]

    '''
    timestep - Get current simulation time
    person_ids - Get list of person IDs
    '''
    while timestep < TIMESTEPS:
        timestep = traci.simulation.getTime()
        person_ids = traci.person.getIDList()
        if timestep > 18000:
            print(len(person_ids), timestep)
        user_data, detected_users, users = person_iterator(person_ids, users, sniffers, timestep, user_data, detected_users)
        
        
        for user in user_data:
            document = user.copy()
            document['_id'] = ObjectId()
            user_collection.insert_one(document)
            # user_collection.insert_one(user)
            
        for duser in detected_users:
            document = duser.copy()
            document['_id'] = ObjectId()
            sniffer_collection.insert_one(document)
        # for duser in detected_users:
        #     sniffer_collection.insert_one(duser)
        # md.batch_insert(user_collection, list(user_data), batch_size=100)
        # md.batch_insert(sniffer_collection, list(detected_users), batch_size=100)
        # print(detected_users)
        traci.simulationStep()
    # Clean up
    traci.close()
    
except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
    traci.close()
    sys.exit(1)


# user_file = f"{timestamp}_user_data_{TIMESTEPS}.json"
# sniffed_file = f"{timestamp}_sniffed_data_{TIMESTEPS}.json"

# print("Saved file to the directory")

# with open(user_file, "w") as f:
#     json.dump(list(user_data), f)

# with open(sniffed_file, "w") as f:
#     json.dump(list(detected_users), f)

