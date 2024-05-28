import libsumo as traci
from modules.sniffer import Sniffer
from modules.user import User
from env import *
from collections import deque
from services.general import random_identifier
from bson.objectid import ObjectId
def person_iterator(p_ids:deque, users:dict, sniffers:deque, timestep:float, usr_data: deque, detected_usrs: deque):
    # Iterate over each person ID
    for person_id in p_ids:
        lo = traci.person.getPosition(person_id)
        person_id = str(person_id)
        user:User
        if person_id in list(users):
            # user exists
            # print("user exists")
            user = users[person_id]
            user.location = lo
            user.randomize_identifiers()
        else:
            # print(f"user {person_id} does not exists")
            user_id = person_id
            location = lo
            bluetooth_id=random_identifier()
            wifi_id=random_identifier()
            lte_id=random_identifier()
            user = User(user_id,location,bluetooth_id=bluetooth_id, wifi_id=wifi_id, lte_id=lte_id, max_step_size=MAX_STEP_SIZE)              
            users[user_id] = user
            
        sniffer: Sniffer
        for sniffer in sniffers:
            detected_usrs.extend(sniffer.detect_users(user, timestep))

        usr_data.append({
                # "_id": ObjectId(),
                "timestep": timestep,
                "user_id": user.user_id,
                "location": user.location,
                # "bluetooth_id": user.bluetooth_id,
                "wifi_id": user.wifi_id,
                "lte_id": user.lte_id,
            })

    return usr_data, detected_usrs, users