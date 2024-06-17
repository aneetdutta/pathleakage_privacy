import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.mongofn import MongoDB
from group.grouping_smart_algorithm import grouper
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import time
import itertools
import sys

md = MongoDB()
'''The below code converts the aggregated results into groups using the grouping distance algorithm
The groups of every sniffer are first calculated and then they are appended to single timestep.
So, we have the dict as 
{timestep: 0, grouped_data: [{LTE: "", WIFI: "", BLUETOOTH: ""}]}'''

md.set_collection("aggregated_sniffer")
'''grouped according to timestep and sniffer'''
sniffer_data = md.collection.find()

group_collection = md.db['groups']
''' Processing every timestep - contains dict : {sniffer_id : [data]}
Stores the processed group to mongodb collection '''

def process_batch(batch):
    grouping_list = []
    for document in batch:
        id = document["_id"]
        st_window = document["st_window"]
        sniffer_data = document["sniffer_data"]
        # print(id, timestep)
        group = grouper(sniffer_data)
        grouping_list.append({"st_window": st_window, "grouped_data": group})
    return grouping_list

def batch_data(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
        
batch_size, grouping_list = 2, []

now = time.time()
batches = list(batch_data(list(sniffer_data), batch_size))
# 
with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    futures = [executor.submit(process_batch, batch) for batch in batches]
    results = [future.result() for future in futures]

grouping_list = list(itertools.chain.from_iterable(results))

print(len(grouping_list))
grouping_list.sort(key=lambda x: x['st_window'])
group_collection.drop()
group_collection.insert_many(grouping_list)
print("Total time taken to group: ", time.time()-now)