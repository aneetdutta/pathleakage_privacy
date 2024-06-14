from modules.mongofn import MongoDB
from services.grouping_algorithm import grouper
import time
md = MongoDB()
'''The below code converts the aggregated results into groups using the grouping distance algorithm
The groups of every sniffer are first calculated and then they are appended to single timestep.
So, we have the dict as 
{timestep: 0, grouped_data: [{LTE: "", WIFI: "", BLUETOOTH: ""}]}'''

md.set_collection("aggregated_results")
'''grouped according to timestep and sniffer'''
sniffer_data = md.collection.find().sort('timestep', 1)

group_collection = md.db['groups']
''' Processing every timestep - contains dict : {sniffer_id : [data]}
Stores the processed group to mongodb collection '''

group_collection.drop()
now = time.time()
grouping_list = []
for document in sniffer_data:
    id = document["_id"]
    timestep = document["timestep"]
    sniffer_data = document["sniffer_data"]
    print(id, timestep)
    group = grouper(sniffer_data)
    grouping_list.append({"timestep": timestep, "grouped_data": group})
   
group_collection.insert_many(grouping_list)
print("Total time taken: ", time.time() - now)