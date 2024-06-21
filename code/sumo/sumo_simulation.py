import os, sys, libsumo as traci
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traceback
from services.general import dump_orjson, str_to_bool
from collections import deque
import time
from services.general import is_point_inside_polygon
from shapely.geometry import Polygon
import polars as pd
import pathlib

from modules.logger import MyLogger

SUMO_BIN_PATH = "/usr/bin/"
SUMO_CFG_FILE = f"{pathlib.Path().resolve()}/{'../scenario/most.sumocfg'}"

# Create a polygon object
print(os.getenv("POLYGON_COORDS"))
POLYGON_COORDS = eval(os.getenv("POLYGON_COORDS"))
USER_TIMESTEPS = int(os.getenv("USER_TIMESTEPS"))

ENABLE_USER_THRESHOLD = str_to_bool(os.getenv("USER_TIMESTEPS"))
TOTAL_NUMBER_OF_USERS = int(os.getenv("TOTAL_NUMBER_OF_USERS"))
DB_NAME = os.getenv("DB_NAME")

ml = MyLogger(f"sumo_simulation_{DB_NAME}")

polygon = Polygon(POLYGON_COORDS)

""" If not person id , save the person id and discard if visited next time"""
visited_person: set = set()

same_userset: set = set()

sumo_cmd = [os.path.join(SUMO_BIN_PATH, "sumo"), "-c", SUMO_CFG_FILE]

""" Start TRACI """
traci.start(sumo_cmd)

try:
    # Simulation loop
    user_data, users = deque(), dict()
    timestep = 14400
    """timestep - Get current simulation time
    user_ids - Get list of user IDs """
    now = time.time()
    while timestep < USER_TIMESTEPS:
        timestep = traci.simulation.getTime()
        user_ids = traci.person.getIDList()
        if timestep % 50 == 0:
            print(len(user_ids), timestep)
            
        for user_id in user_ids:
            user_location = traci.person.getPosition(user_id)
            stage = traci.person.getStage(user_id)
            # type_u = traci.person.getTypeID(user_id)
            # vehicle = traci.person.getVehicle(user_id)
            ''' Stage(type=3, vType=passenger3, line=pedestrian_GW2-1_2780_tr,
            edges=('153656', '152677#5'), travelTime=24.0, cost=INVALID, length=310.6909276073291, 
            depart=18006.0, departPos=INVALID, arrivalPos=44.55, description=driving)   '''
            # print(stage)
            mobility_factor = traci.person.getSpeed(user_id)
            """ If user exits the polygon, remove the user from the user data"""
            if not is_point_inside_polygon(user_location[0], user_location[1], polygon):
                visited_person.add(user_id)
                continue
            
            if ENABLE_USER_THRESHOLD:
                if user_id not in same_userset and len(same_userset) < TOTAL_NUMBER_OF_USERS:
                    same_userset.add(user_id)
                elif user_id not in same_userset:
                    continue
            
            
            """ If user enters the polygon after some time, remove the user again from the user data"""
            if user_id in visited_person:
                continue

            user_data.append(
                {
                    "timestep": timestep,
                    "user_id": user_id,
                    "mf": mobility_factor,
                    # "type":type_u,
                    # "vehicle": vehicle,
                    "description": stage.description,
                    # "type_": stage.type,
                    "loc_x": user_location[0],
                    "loc_y": user_location[1]
                }
            )        
        traci.simulationStep()
    print("Time taken: ", time.time() - now)
    traci.close()
except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
    traci.close()
    sys.exit(1)

ml.logger.info("Total time take to fetch user_data from sumo_simulation: ", time.time() - now)
user_file = f"data/raw_user_data_{DB_NAME}.csv"
ml.logger.info("Saved file to the directory")
df = pd.DataFrame(user_data)
total_unique_user_ids = df.select(pd.col('user_id').n_unique()).item()
ml.logger.info(f"Total unique user_id: {total_unique_user_ids}")

walking_user_ids = df.filter(pd.col('description') == 'walking')['user_id'].unique().to_list()
ml.logger.info(f"user_ids having 'walking' as their description: {len(walking_user_ids)}")


max_value = df['mf'].max()
min_value = df['mf'].min()
average_value = df['mf'].mean()
median_value = df['mf'].median()

ml.logger.info(f"Max Mobility: {max_value}")
ml.logger.info(f"Min Mobility: {min_value}")
ml.logger.info(f"Average Mobility: {average_value}")
ml.logger.info(f"Median Mobility: {median_value}")

df.write_csv(user_file)
