import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.user import User
from collections import deque
from services.general import str_to_bool
from services.general import random_identifier
from services.general import calculate_distance_l
import polars as pd
from modules.logger import MyLogger
from collections import defaultdict
import json
import time

DB_NAME = os.getenv("DB_NAME")
DATA_USECASE = os.getenv("DATA_USECASE")

ml = MyLogger(f"filter_user_data_{DB_NAME}")

df = pd.read_csv(f"data/raw_user_data_{DATA_USECASE}.csv")
# print(df.columns)
# sys.exit()
raw_user_data = df.to_dicts()

TOTAL_NUMBER_OF_USERS = int(os.getenv("TOTAL_NUMBER_OF_USERS"))
MAX_MOBILITY_FACTOR = float(os.getenv('MAX_MOBILITY_FACTOR'))
ENABLE_USER_THRESHOLD = str_to_bool(os.getenv("ENABLE_USER_THRESHOLD"))
TOTAL_NUMBER_OF_USERS = int(os.getenv("TOTAL_NUMBER_OF_USERS"))

same_userset: set = set()

user_dict = dict()
user_data = deque()

check_users = False
user_mobility = defaultdict()
max_mobility_checker = defaultdict(list)
user_first_timestep = defaultdict()

for user_ in raw_user_data:
    user_id = user_["user_id"]
    timestep = user_["timestep"]
    if user_id not in user_first_timestep:
        user_first_timestep[user_id] = timestep
    mf = user_["mf"]
    loc_x = user_["loc_x"]
    loc_y = user_["loc_y"]
    if user_id in max_mobility_checker:
        dis = calculate_distance_l(max_mobility_checker[user_id][0], [loc_x, loc_y])
        tim = (timestep - max_mobility_checker[user_id][1])
        user_mobility[user_id] = max(dis/tim, user_mobility[user_id])
            # time.sleep(0.2)
    else:
        user_mobility[user_id] = 0
        
    max_mobility_checker[user_id] = [[loc_x, loc_y], float(timestep)]

users_with_less_mobility = set()

for user_id, value in user_mobility.items(): 
    if value < MAX_MOBILITY_FACTOR:
        users_with_less_mobility.add((user_id, user_first_timestep[user_id]))
        
sorted_list = sorted(users_with_less_mobility, key=lambda x: x[1])
# users_with_less_mobility = list(users_with_less_mobility)
users_with_less_mobility = [x[0] for x in sorted_list]

if ENABLE_USER_THRESHOLD:
    users_with_less_mobility = users_with_less_mobility[:TOTAL_NUMBER_OF_USERS]

df = df.sort('timestep')
filtered_df = df.filter(pd.col('user_id').is_in(users_with_less_mobility))
filtered_df = filtered_df.drop(['mf', 'description'])
# filtered_df = df[df['user_id'].isin(users_with_less_mobility)]

# print(filtered_df)
# filtered_df.to_csv('data/raw_user_data_{DATA_USECASE}_.csv', index=False)
filtered_df.write_csv(f'data/raw_user_data_{DATA_USECASE}_filtered.csv', has_header=True)


max_key= max(user_mobility, key=user_mobility.get)

count_users = sum(1 for value in user_mobility.values() if value > MAX_MOBILITY_FACTOR)
count_users_ = sum(1 for value in user_mobility.values() if value <= MAX_MOBILITY_FACTOR)


ml.logger.info(f"Max mobility achieved per user: {max_key}, value: {user_mobility[max_key]}")
ml.logger.info(f"Number of users having mobility greater than {MAX_MOBILITY_FACTOR} {count_users}")
ml.logger.info(f"Number of users having mobility less than or equal to {MAX_MOBILITY_FACTOR} {count_users_}")



ml.logger.info(f"Total filtered users with mobility less than {MAX_MOBILITY_FACTOR}: {len(users_with_less_mobility)}")
ml.logger.info(list(users_with_less_mobility))