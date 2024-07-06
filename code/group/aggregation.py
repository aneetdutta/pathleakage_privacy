
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.mongofn import MongoDB
import time
md = MongoDB()

now = time.time()

md.set_collection("parsed_sniffed_data")

''' The below code converts the sniffer data into 2 collections 
- Aggregation by sniffers
- Aggregation by users
- Aggregation by timesteps '''

md.db['aggregated_sniffer'].drop()
aggregation_results = md.aggregate_st_window()
for document in aggregation_results:
    try:
        md.db['aggregated_sniffer'].insert_one(document)
    except Exception as e:
        print(f"Error inserting document: {str(e)}")
# md.db['aggregated_results'].drop()
# md.db['aggregated_results'].insert_many(md.aggregate_save())
md.db['aggregate_users'].drop()
md.db["aggregate_users"].insert_many(md.aggregate_users())
md.db['aggregate_timesteps'].drop()
md.db["aggregate_timesteps"].insert_many(md.aggregate_timestep())

print("Time taken to aggregate and save to mongodb: ", time.time() - now)