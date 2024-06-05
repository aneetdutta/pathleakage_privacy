import libsumo as traci
from modules.user import User
from env import *
from services.general import is_point_inside_polygon
from collections import deque
from services.general import random_identifier
from shapely.geometry import Polygon

polygon_coords = [
    (3499.77,1500.07),
    (5798.43,3799.93),
    (6452.11,3150.56),
    (5401.44,2099.71),
    (5751.91,1749.63),
    (4500.10,498.92),
]

# Create a polygon object
polygon = Polygon(polygon_coords)

''' If not person id , save the person id and discard if visited next time'''
visited_person:set = set()

def user_data_generate(p_ids:deque, users:dict, timestep:float, usr_data: deque):
    # Iterate over each person ID
    for person_id in p_ids:
        lo = traci.person.getPosition(person_id)
        ''' If user exits the polygon, remove the user from the user data'''
        if not is_point_inside_polygon(lo[0],lo[1],polygon):
            visited_person.add(person_id)
            continue
        
        ''' If user enters the polygon after some time, remove the user again from the user data'''
        if person_id in visited_person:
            continue
        
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

        usr_data.append({
                # "_id": ObjectId(),
                "timestep": timestep,
                "user_id": user.user_id,
                "location": user.location,
                "bluetooth_id": user.bluetooth_id,
                "wifi_id": user.wifi_id,
                "lte_id": user.lte_id,
            })

    return usr_data, users