from services.general import *
from modules.mongofn import MongoDB
from collections import defaultdict
''' Load the sumo_simulation result from mongodb '''
import pandas as pd
# import sys
md = MongoDB()

md.set_collection("aggregate_users")
documents = md.collection.find()
user_data = pd.DataFrame(documents)

md.set_collection("aggregate_timesteps")
documents = md.collection.find()
timestep_data = pd.DataFrame(documents)

md.set_collection('intra_mappings')

intra_docs = md.collection.find()
intra_data = {}
for document in intra_docs:
    intra_data[document['_id']] = document['mapping']
    
    
md.set_collection('inter_mappings')

inter_docs = md.collection.find()
inter_data = {}
for document in inter_docs:
    inter_data[document['_id']] = document['mapping']


''' To create something like:
user_id, linked_id, duration_of_linked_id_through_tracking, duration_of_linked_id_in_sniffed_data, privacy score

Algorithm -
a) Take a key (single identifier) - measure duration of tracking after tracking
b) Take user_id corresponding to the linked_id, - measure its duration in sniffed data
c) Privacy score = duration_of_linked_id_through_tracking / duration_of_linked_id_in_sniffed_data'''



''' Baseline single protocol'''

''' '''
# for 




''' Baseline single protocol - with randomization '''


''' Multiple protocol with randomization - LTE + Wifi '''


