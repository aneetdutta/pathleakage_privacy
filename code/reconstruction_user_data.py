from services.general import *
from modules.mongofn import MongoDB
from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
# import sys
md = MongoDB()

md.set_collection("aggregate_timesteps")
documents = md.collection.find()
timestep_data = pd.DataFrame(documents)

md.set_collection("aggregate_users")
documents = md.collection.find()
user_df = pd.DataFrame(documents)

start_timestep:list = []
last_timestep:list = []
''' Fetch user duration over the timesteps '''
for _, user_row in user_df.iterrows():
    first_row, lt = True, ""
    for _, timestep_row in timestep_data.iterrows():
        common_id = set(user_row["ids"]).intersection(set(timestep_row["ids"]))
        if common_id and first_row:
            start_timestep.append(timestep_row["timestep"])
            first_row = False
            
        if common_id and not first_row:
            lt = timestep_row["timestep"]
        
    last_timestep.append(lt)    
    
user_df["start_timestep"] = start_timestep
user_df["last_timestep"] = last_timestep
user_df["duration"] = user_df["last_timestep"]  - user_df["start_timestep"]

user_data = user_df.to_dict(orient='records')

md.set_collection("aggregate_users")
md.collection.drop()
md.collection.insert_many(user_data)
