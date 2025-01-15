import os, sys
sys.path.append(os.getcwd())
from modules.general import *
import numpy as np
import copy
from modules.general import *

ENABLE_PARTIAL_COVERAGE=False
SCENARIO_NAME = os.getenv("SCENARIO_NAME")

intramap=np.load(f'data/{SCENARIO_NAME}/intramap_{SCENARIO_NAME}.npy', allow_pickle=True).item()
intermap=np.load(f'data/{SCENARIO_NAME}/intermap_{SCENARIO_NAME}.npy', allow_pickle=True).item()

PARQUET_FILE_PATH = f"data/{SCENARIO_NAME}/aggregated_id_{SCENARIO_NAME}.parquet"
df = pl.read_parquet(PARQUET_FILE_PATH)
id_protocol_dict = {row["id"]: row["protocol"] for row in df.to_dicts()}

def filter_intermap(intermp):
    for id1 in intermp.keys():
        user_id = '_'.join(id1.split("_")[0:3])
        p1 = id_protocol_dict[id1]
        for p in intermp[id1]:
            set_id1=intermp[id1][p]
            temp_list=set()
            for id2 in set_id1:
                if id1 not in intermp[id2][p1]:
                    if '_'.join(id2.split("_")[0:3]) == user_id:
                        print(user_id, id1, id2)
                    temp_list.add(id2)
            intermp[id1][p]=set(intermp[id1][p]-temp_list)
    return intermp


def compute_common_id(intramp, intermp):
    common_id = defaultdict(set)
    for id1 in intramp.keys():
        intra_mapping=intramp[id1]
       # if len(intra_mapping)==1:
        #    continue
        temp_list = set()
        for id2 in intra_mapping:
            if id1 == id2:
                continue
            remove = False
            if id1 not in intermp:
                continue
            for p in intermp[id1]:
                
                set_id1= set(intermp[id1][p])
                if id2 not in intermp.keys():
                    continue
                set_id2= set(intermp[id2][p])    
            
                common = set_id1.intersection(set_id2)
                
                if not common: # no common set found     
                    break
                else:
                    common_id[id1].update(common)
    return common_id


def refine_intramap(intramp, intermp, chnge):
   
    for id1 in intramp.keys():
        intra_mapping=intramp[id1]
        if len(intra_mapping)==1:
            continue
        temp_list = set()
        for id2 in intra_mapping:
            #if id1 == id2:
             #   continue
            remove = False
            for p in intermp[id1]:
                set_id1= set(intermp[id1][p])
                if id2 not in intermp.keys():
                    continue
                set_id2= set(intermp[id2][p])    
            
                common = set_id1.intersection(set_id2)
                                
                if not common: # no common set found
                    remove = True        
                    break
                # else:
                #     common_id[id1].update(common)
                
                if not ENABLE_PARTIAL_COVERAGE:
                    if not set_id1 or not set_id2:
                        remove = True
                        break
                else:
                    if not set_id1 or not set_id2:
                        continue
            if remove:
                chnge = True
                temp_list.add(id2)
        intramp[id1]=list(set(intramp[id1])-temp_list)          
    return intramp, chnge

def refine_intermap(intramp, intermp, chnge, common_id):
    for id1 in intermp.keys():
        common_set_id = common_id[id1]
        for p in intermp[id1]:
            set_id1= set(intermp[id1][p])
            if len(set_id1)==1:
                continue
            if common_set_id: # no common set found
                ''' If common set id, remove common id from intermap(id1) '''
                id1_remaining = set()
                id1_remaining = set_id1 - common_set_id
                
                LHS = set()
                for id2 in id1_remaining:
                    if id2 in intramp.keys():
                        if set(intramp[id2]).intersection(common_set_id):
                            LHS.add(id2)

                id1_remaining=id1_remaining-LHS

                while(True):
                    l = len(LHS)
                    for id2 in id1_remaining:
                        if id2 in intramp.keys():
                            if set(intramp[id2]).intersection(LHS):
                                LHS.add(id2)
                                
                    if len(LHS) == l:
                        break

                discard_id1_mappings=id1_remaining-LHS
                user_id = '_'.join(id1.split("_")[0:3])
                for i in discard_id1_mappings:
                    if user_id in i:
                        print(id1, i)
                        
                ''' Remove discard_id1_mappings from  intermap - Refining procedure '''
                a = len(intermp[id1][p])
                intermp[id1][p] = intermp[id1][p] - discard_id1_mappings
                if not (len(intermp[id1][p]) == a):
                    chnge = True
    return intramp, intermp, chnge

change = True
while(change):
    change = False
    ''' Refine Intramap Procedure '''
    intramap, change = refine_intramap(intramap, intermap, change)
    intramap = clean_mappings(intramap)
    ''' Refine Intermap Procedure '''    
    common_id = compute_common_id(intramap, intermap)
    intramap, intermap, change = refine_intermap(intramap, intermap, change, common_id)
    intermap=filter_intermap(intermap)

    print("Refining")


np.save(f'data/{SCENARIO_NAME}/refined_intermap_{SCENARIO_NAME}.npy', intermap, allow_pickle=True)
np.save(f'data/{SCENARIO_NAME}/refined_intramap_{SCENARIO_NAME}.npy', intramap, allow_pickle=True)

print("Refine completed")