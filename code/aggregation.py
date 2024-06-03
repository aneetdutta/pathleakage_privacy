
from modules.mongofn import MongoDB
import time
md = MongoDB()

now = time.time()

md.set_collection("sniffed_data")

''' The below code converts the sniffer data into 3 collections 
- Aggregation by sniffers and timesteps 
- Aggregation by users
- Aggregation by timesteps '''
md.db['aggregated_results'].drop()
md.db['aggregated_results'].insert_many(md.aggregate_save())
md.db['aggregate_users'].drop()
md.db["aggregate_users"].insert_many(md.aggregate_users())
md.db['aggregate_timesteps'].drop()
md.db["aggregate_timesteps"].insert_many(md.aggregate_timestep())

print("Time taken to aggregate and save to mongodb: ", time.time() - now)