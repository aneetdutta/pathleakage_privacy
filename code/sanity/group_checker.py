import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.general import *
from tracking.tracking_algorithm import tracking_algorithm
from modules.mongofn import MongoDB
import json
from collections import defaultdict
from pprint import pprint
from modules.logger import MyLogger
import sys
''' Load the sumo_simulation result from mongodb '''

DB_NAME = os.getenv("DB_NAME")
md = MongoDB()
ml = MyLogger(f"group_checker_{DB_NAME}")

md.set_collection("groups")

all_groups = list(md.collection.find())

# print(all_groups)
single_groups = defaultdict(list)
total_groups = 0
for document in all_groups:
    st_window = document["st_window"]
    grouped_data = document["grouped_data"]
    for group in grouped_data:
        total_groups+=len(group)
        if len(group) < 2:
            single_groups[str(st_window)].append(group)

single_group_counter = 0
len_single_group = dict()
for i in single_groups:
    len_single_group[i] = len(single_groups[i])
    single_group_counter += len(single_groups[i])
    
ml.logger.info(f"Total Single groups for multiprotocol use-case: {single_group_counter}")
ml.logger.info(f"Total groups for multiprotocol use-case: {total_groups}")
ml.logger.info(len_single_group)
ml.logger.info(single_groups)
