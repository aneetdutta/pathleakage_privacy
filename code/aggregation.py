
from modules.mongofn import MongoDB
import time
md = MongoDB()

''' The below code converts the sumo_simulation results to aggregated results of the sniffer
It is modelled as below
{timestep: 0, sniffer_data: {0: [{groups}]}}'''

md.set_collection("sniffed_data")
results = md.aggregate_save()

new_collection = md.db['aggregated_results']# Insert the aggregated results into the new collection
now = time.time()
for result in results: 
    new_collection.insert_one(result)
print("Time taken to aggregate and save to mongodb: ", time.time() - now)
