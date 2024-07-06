import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.mongofn import MongoDB
from group.grouping_algorithm_seq import grouper
from group.grouping_algorithm_tri_seq import grouper_tri
from services.general import str_to_bool
from collections import defaultdict
from modules.logger import MyLogger
import time
md = MongoDB()
DB_NAME = os.getenv("DB_NAME")
ml = MyLogger(f"grouping_seq_{DB_NAME}")
'''The below code converts the aggregated results into groups using the grouping distance algorithm
The groups of every sniffer are first calculated and then they are appended to single timestep.
So, we have the dict as 
{timestep: 0, grouped_data: [{LTE: "", WIFI: "", BLUETOOTH: ""}]}'''

md.set_collection("aggregated_sniffer")
'''grouped according to timestep and sniffer'''
sniffer_data_ =list(md.collection.find(no_cursor_timeout=True))

group_collection = md.db['groups']
''' Processing every timestep - contains dict : {sniffer_id : [data]}
Stores the processed group to mongodb collection '''

group_collection.drop()
now = time.time()
grouping_list = []
incompatible_ids: defaultdict[set] = defaultdict(set)

ENABLE_MULTILATERATION = str_to_bool(os.getenv("ENABLE_MULTILATERATION"))

for document in sniffer_data_:
    id = document["_id"]
    st_window = document["st_window"]
    ml.logger.info(f"Time window: {st_window}")
    
    sniffer_data = document["sniffer_data"]
    # print(id, timestep)
    if ENABLE_MULTILATERATION:
        incompatible_ids, group = grouper_tri(sniffer_data, incompatible_ids)
        grouping_list.append({"st_window": st_window, "grouped_data": group})
    else:
        incompatible_ids, group = grouper(sniffer_data, incompatible_ids)
        grouping_list.append({"st_window": st_window, "grouped_data": group})

grouping_list.sort(key=lambda x: x['st_window'])
group_collection.drop()
group_collection.insert_many(grouping_list)
ml.logger.info("Total time taken: ", time.time() - now)