import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.user import User
from collections import deque
from services.general import str_to_bool
from services.general import random_identifier
import polars as pd
from modules.logger import MyLogger

DB_NAME = os.getenv("DB_NAME")

LIMIT_USER_AFTER_USER_DATA = str_to_bool(os.getenv("LIMIT_USER_AFTER_USER_DATA"))
LIMIT_USER_NUM_USERS = int(os.getenv("LIMIT_USER_NUM_USERS"))

if not LIMIT_USER_AFTER_USER_DATA:
    print(f"LIMIT_USER_AFTER_USER_DATA: {LIMIT_USER_AFTER_USER_DATA}")
    sys.exit()
    
ml = MyLogger(f"generate_user_data_{DB_NAME}")
df = pd.read_csv(f"data/raw_user_data_{DB_NAME}.csv")

# Step 1: Identify the first 50 unique users
unique_users = df['user_id'].unique()[:LIMIT_USER_NUM_USERS]

# Step 2: Filter the DataFrame to keep only the rows corresponding to these users
filtered_df = df[df['user_id'].isin(unique_users)]

print(filtered_df)


same_userset: set = set()

user_dict = dict()
user_data = deque()
