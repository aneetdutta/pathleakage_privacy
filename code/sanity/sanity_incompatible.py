import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.general import *
from modules.mongofn import MongoDB
from services.general import str_to_bool
# from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
# import sys
md = MongoDB()
from modules.logger import MyLogger

DB_NAME = os.getenv("DB_NAME")
ml = MyLogger(f"sanity_incompatible_{DB_NAME}")

md.set_collection("aggregate_users")
documents = list(md.collection.find())
user_data = {document['user_id']: set(document['ids']) for document in documents}

user_df = pd.DataFrame(documents)

ENABLE_SMART_TRACKING = str_to_bool(os.getenv('ENABLE_SMART_TRACKING'))

if ENABLE_SMART_TRACKING:
    ml = MyLogger(f"sanity_incompatible_smart_{DB_NAME}")
    md.set_collection('incompatible_intra_smart')
    documents = list(md.collection.find())
    inter_df = pd.DataFrame(documents)
    incompatible_intra = {document['_id']: set(document['mapping']) for document in documents}

    problem = {}
    for id, mapping in incompatible_intra.items():
        for user, user_ids in user_data.items():
            if id in user_ids:
                common = mapping.intersection(user_ids)
                if common:
                    problem[id] = common
                    break

    ml.logger.info(f"Smart tracking: {ENABLE_SMART_TRACKING}")
    ml.logger.info(f"Total problematic mappings found with same intra ids: {len(problem)}")
    ml.logger.info(problem)    

md.set_collection('incompatible_inter')
documents = list(md.collection.find())
inter_df = pd.DataFrame(documents)
incompatible_inter_data = {document['_id']: set(document['mapping']) for document in documents}

problem = {}
for id, mapping in incompatible_inter_data.items():
    for user, user_ids in user_data.items():
        if id in user_ids:
            common = mapping.intersection(user_ids)
            if common:
                problem[id] = common
                break

# ml.logger.info(f"Smart tracking: {ENABLE_SMART_TRACKING}")
ml.logger.info(f"Total problematic mappings found with same inter ids: {len(problem)}")
ml.logger.info(problem)
                



