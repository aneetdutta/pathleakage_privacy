import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.user import User
from collections import deque
from services.general import str_to_bool
from services.general import random_identifier
import polars as pd
from modules.logger import MyLogger

DB_NAME = os.getenv("DB_NAME")

ENABLE_USER_THRESHOLD = str_to_bool(os.getenv("ENABLE_USER_THRESHOLD"))
TOTAL_NUMBER_OF_USERS = int(os.getenv("TOTAL_NUMBER_OF_USERS"))
ml = MyLogger(f"generate_user_data_{DB_NAME}")

df = pd.read_csv(f"data/raw_user_data_{DB_NAME}.csv")
raw_user_data = df.to_dicts()

# print(ENABLE_USER_THRESHOLD)

same_userset: set = set()

user_dict = dict()
user_data = deque()

check_users = False

for user_ in raw_user_data:
    # print(user_)
    user_id = user_["user_id"]
    timestep = user_["timestep"]
    mf = user_["mf"]
    loc_x = user_["loc_x"]
    loc_y = user_["loc_y"]
    
    if ENABLE_USER_THRESHOLD:
        # print(ENABLE_USER_THRESHOLD)
        if user_id not in same_userset and len(same_userset) < TOTAL_NUMBER_OF_USERS:
            same_userset.add(user_id)
        elif user_id not in same_userset:
            continue
    
    if len(same_userset) >= TOTAL_NUMBER_OF_USERS and not check_users:
        ml.logger.info(f"Total number of users {len(same_userset)} capped at {timestep}")
        check_users = True