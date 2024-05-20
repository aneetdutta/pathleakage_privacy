from modules.devicemanager import DeviceManager
from modules.device import Device
from funct.fn import calculate_distance_l
from env import DELTA_P

{
    "Bluetooth": [
        "7RBQFXP9V7XY"
    ],
    "WiFi": [
        "GC7I7ILS676L"
    ],
    "LTE": [
        "LTEDevice70"
    ]
}

def old_id_not_exists(old_id_t0, new_line_tn1, type_):
    '''To check if old identifier exists anywhere in the tn+1 mapping, if yes, then no linkage, else link them
    function written reversely : if old identifier exists, then return false, else return True'''
    for item_tn1 in new_line_tn1:
        if type_ in item_tn1:
            if old_id_t0 in item_tn1[type_]:
                # print(False)
                return False
    # print(True)
    return True

def rule_1(line1: list, line2: list, tn1_list:list, devices: list[Device], timestep, location_data, rule3_check):#invoked after checking the condition of time and location  
    mapping = None 
    sa_1, sb_1, sc_1 = line1["Bluetooth"] if "Bluetooth" in line1 else [], line1["WiFi"] if "WiFi" in line1 else [], line1["LTE"] if "LTE" in line1 else []
    sa_2, sb_2, sc_2 = line2["Bluetooth"] if "Bluetooth" in line2 else [], line2["WiFi"] if "WiFi" in line2 else [], line2["LTE"] if "LTE" in line2 else []
        
    # Prepare set operations and store in variables
    set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
    set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
    set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
    l1=set_sa_1.symmetric_difference(set_sa_2)
    l2=set_sb_1.symmetric_difference(set_sb_2)    
    l3=set_sc_1.symmetric_difference(set_sc_2)
    
    intersec_l1=set_sa_1.intersection(set_sa_2)
    intersec_l2=set_sb_1.intersection(set_sb_2)    
    intersec_l3=set_sc_1.intersection(set_sc_2)

    len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
    len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
        
    '''LTE Range'''
    if (len_sa_1, len_sb_1, len_sa_2, len_sb_2) == (0, 0, 0, 0) and len_sc_1 == len_sc_2:
        if len_sc_1 - len(intersec_l3) == 1 and set_sc_1!=set_sc_2:
            '''check if IDA from t0 exists in t1: entire set
            if old_id_checker, then IDA could be mapped to IDB, but now check distance based on threshold of 1 meter'''
            if old_id_not_exists(next(iter(set_sc_1.intersection(l3))), tn1_list, 'LTE'):
                ''' t0: IDA ; t1: IDB (distance calculation) 
                    |p0 - p1| < delta_p'''
                d = calculate_distance_l(location_data[str(int(timestep)-1)][f"{'LTE'}_{next(iter(set_sc_1.intersection(l3)))}"], location_data[timestep][f"{'LTE'}_{next(iter(set_sc_2.intersection(l3)))}"])
                mapping = l3 if d < DELTA_P else None
        '''Wifi Range for rule 3 internal'''
        
    elif (len_sa_1, len_sc_1, len_sa_2, len_sc_2) == (0, 0, 0, 0) and len_sb_1 == len_sb_2:
        if len_sb_1 - len(intersec_l2) == 1 and set_sb_1 != set_sb_2:
            '''check if IDA from t0 exists in t1: entire set'''
            if old_id_not_exists(next(iter(set_sb_1.intersection(l2))), tn1_list, 'WiFi'):
                ''' t0: IDA ; t1: IDB (distance calculation) 
                    |p0 - p1| < delta_p'''
                d = calculate_distance_l(location_data[str(int(timestep)-1)][f"{'WiFi'}_{next(iter(set_sb_1.intersection(l2)))}"], location_data[timestep][f"{'WiFi'}_{next(iter(set_sb_2.intersection(l2)))}"])
                mapping = l2 if d < DELTA_P else None
    else:
        mapping=None

    if mapping is not None and rule3_check:
        print("by rule 1")
        print(mapping)
        devices.append(mapping)
    return mapping, devices

def rule_2(manager: DeviceManager, line1, devices: list[Device]):
    sa_1, sb_1, sc_1 = line1["Bluetooth"] if "Bluetooth" in line1 else [], line1["WiFi"] if "WiFi" in line1 else [], line1["LTE"] if "LTE" in line1 else []
    d, d1, d2 = len(sa_1), len(sb_1), len(sc_1)
    set_sa_1, set_sb_1, set_sc_1  = set(sa_1), set(sb_1), set(sc_1)

    if d==1 and d1==1 and d2!=1:
        mapping = set()
        mapping.update(set_sa_1,set_sb_1)
        manager.create_device(next(iter(set_sa_1)),next(iter(set_sb_1)),None)
    elif d!=1 and d1==1 and d2==1:
        mapping = set()
        mapping.update(set_sb_1,set_sc_1)
        manager.create_device(None,next(iter(set_sb_1)),next(iter(set_sc_1)))
    elif d==1 and d1==1 and d2==1:
        mapping = set()
        mapping.update(set_sa_1,set_sb_1,set_sc_1)
        manager.create_device(next(iter(set_sa_1)),next(iter(set_sb_1)),next(iter(set_sc_1)))
    else:
        mapping=None
    
    if mapping is not None:
        print("by rule 2")
        print(mapping)
        devices.append(mapping)
    return devices
   
def rule_3(manager: DeviceManager, line1, line2,  tn1_list:list, devices: list[Device], timestep, location_data):
    mapping = None
    sa_1, sb_1, sc_1 = line1["Bluetooth"] if "Bluetooth" in line1 else [], line1["WiFi"] if "WiFi" in line1 else [], line1["LTE"] if "LTE" in line1 else []
    sa_2, sb_2, sc_2 = line2["Bluetooth"] if "Bluetooth" in line2 else [], line2["WiFi"] if "WiFi" in line2 else [], line2["LTE"] if "LTE" in line2 else []

    # Prepare set operations and store in variables
    set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
    set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
    set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
    l1=set_sa_1.intersection(set_sa_2)
    l2=set_sb_1.intersection(set_sb_2)    
    l3=set_sc_1.intersection(set_sc_2)
    
    l1_=set_sa_1.symmetric_difference(set_sa_2)
    l2_=set_sb_1.symmetric_difference(set_sb_2)    
    l3_=set_sc_1.symmetric_difference(set_sc_2)
    
    len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
    len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
    
    len_l1, len_l2, len_l3 = len(l1), len(l2), len(l3)                              
    
    last_rule = False
    ''' Conditions:
    1)  if wifi & bluetooth same, lte diff (rule 1 applicable with rule 3)
    #2)  if bluetooth same, but lte & wifi diff (rule 1 applicable with rule 3)
    3)  if lte & bluetooth same, wifi diff
    4)  if lte & wifi same, bluetooth diff
    5)  if wifi same, but lte & bluetooth diff (rule 1 applicable with rule 3),
    6)  if lte same, but wifi diff
    '''

    
    ''' Check if Bluetooth set is same'''
    if len_l1==len_sa_1 and len_l1==len_sa_2:
        ''' Check if Wifi set is same'''
        if len_l2==len_sb_1 and len_l2==len_sb_2 and len_l2!=0:
            ''' 1) Check if LTE set is different'''
            if len_l3==len_sc_1-1 and len_l3==len_sc_2-1 and len_l3!=0:
                
                ''' Here, Bluetooth and Wifi sets are same, but LTE Identifier set is different.
                Since range of LTE is greater than Bluetooth and Wifi, Rule 1 must be implemented for mapping'''
                mapping, _ = rule_1(line1, line2, tn1_list, devices, timestep, location_data, rule3_check=False)
                # mapping=(set_sc_1-set(l3),set_sc_1-set(l3))
                if mapping is not None:
                    print("Cond 1")
                    old_id, new_id = (set_sc_1-set(l3)).pop(), (set_sc_2-set(l3)).pop()                
                    manager.linking_id('LTE',old_id,new_id)
            ''' Check if Wifi set is different'''
        elif len_l2==len_sb_1-1 and len_l2==len_sb_2-1 and len_l2!=0:
            ''' 2) Check if LTE set is different'''
            if len_l3==len_sc_1-1 and len_l3==len_sc_2-1 and len_l3!=0:
                
                ''' Here, Bluetooth set is same, but LTE & Wifi Identifier set is different.
                Since range of LTE and Wifi is greater than Bluetooth , Rule 1 must be implemented for mapping'''
                mapping, _ = rule_1(line1, line2, tn1_list, devices, timestep, location_data, rule3_check=False)
                # mapping=(set_sc_1-set(l3),set_sc_1-set(l3))
                if mapping is not None:
                    print("Cond 2")
                    old_id, new_id = (set_sc_1-set(l3)).pop(), (set_sc_2-set(l3)).pop()                
                    manager.linking_id('LTE',old_id,new_id)
                    old_id, new_id = (set_sb_1-set(l2)).pop(), (set_sb_2-set(l2)).pop()   
                    manager.linking_id('WiFi',old_id,new_id)
            
            '''Check if LTE Set is same'''
        elif len_l3==len_sc_1 and len_l3==len_sc_2 and len_l3!=0:
            ''' 3) Check if Wifi Set is different'''
            if len_l2==len_sb_1-1 and len_l2==len_sb_2-1:
                print("Cond 3")
                ''' Here, Bluetooth and LTE sets are same, but Wifi Identifier set is different.
                Since range of Wifi is less than LTE, Rule 3 is correct'''
                print(next(iter(set_sb_1.intersection(l2_))))
                
                if old_id_not_exists(next(iter(set_sb_1.intersection(l2_))), tn1_list, 'WiFi'):
                    print(line1, line2)
                    ''' t0: IDA ; t1: IDB (distance calculation) 
                        |p0 - p1| < delta_p'''
                    print(True, "calculating distance")
                    d = calculate_distance_l(location_data[str(int(timestep)-1)][f"{'WiFi'}_{next(iter(set_sb_1.intersection(l2_)))}"], location_data[timestep][f"{'WiFi'}_{next(iter(set_sb_2.intersection(l2_)))}"])
                    print(d, "distance")
                    mapping={str(set(sb_1)-set(l2)),str(set(sb_2)-set(l2))} if d < DELTA_P else None
                    old_id=(set(sb_1)-set(l2)).pop()
                    new_id=(set(sb_2)-set(l2)).pop()
                    manager.linking_id('WiFi',old_id,new_id)

        ''' Check if Wifi set is same '''
    elif len_l2==len_sb_1 and len_l2==len_sb_2 and len_l2!=0:
        ''' Check if LTE set is same '''
        if len_l3==len_sc_1 and len_l3==len_sc_2 and len_l3!=0:
            ''' 4) Check if Bluetooth set is different '''
            if len_l1==len_sa_1-1 and len_l1==len_sa_2-1:
                print("Cond 4")
                ''' Here, Wifi and LTE sets are same, but Bluetooth Identifier set is different.
                Since range of Bluetooth is less than all, Rule 3 is correct'''
                if old_id_not_exists(next(iter(set_sa_1.intersection(l1_))), tn1_list, 'Bluetooth'):
                    print(line1, line2)
                    ''' t0: IDA ; t1: IDB (distance calculation) 
                        |p0 - p1| < delta_p'''
                    print(True, "calculating distance")
                    d = calculate_distance_l(location_data[str(int(timestep)-1)][f"{'Bluetooth'}_{next(iter(set_sa_1.intersection(l1_)))}"], location_data[timestep][f"{'Bluetooth'}_{next(iter(set_sa_2.intersection(l1_)))}"])
                    print(d, "distance")
                    mapping={str(set(sa_1)-set(l1)),str(set(sa_2)-set(l1))} if d < DELTA_P else None

                    old_id=(set(sa_1)-set(l1)).pop()
                    new_id=(set(sa_2)-set(l1)).pop()
                    manager.linking_id('Bluetooth',old_id,new_id)

            ''' Check if LTE set is different '''
        elif len_l3==len_sc_1-1 and len_l3==len_sc_2-1 and len_l3!=0:
            ''' 5) Check if Bluetooth set is different '''
            if len_l1==len_sa_1-1 and len_l1==len_sa_2-1:
                ''' Here, Wifi set is same, but LTE & Bluetooth Identifier set is different.
                Since range of LTE is greater than Wifi , Rule 1 must be implemented for mapping'''
                mapping, _ = rule_1(line1, line2, tn1_list, devices, timestep, location_data, rule3_check=False)
                # mapping=(set_sc_1-set(l3),set_sc_1-set(l3))
                if mapping is not None:
                    print("Cond 5")
                    old_id, new_id = (set_sc_1-set(l3)).pop(), (set_sc_2-set(l3)).pop()                
                    manager.linking_id('LTE',old_id,new_id)
                    old_id, new_id = (set_sa_1-set(l1)).pop(), (set_sa_2-set(l1)).pop()   
                    manager.linking_id('Bluetooth',old_id,new_id)
    
        '''Check if LTE Set is same'''
    elif len_l3==len_sc_1 and len_l3==len_sc_2 and len_l3!=0:
        ''' Check if Wifi Set is different '''
        if len_l2==len_sb_1-1 and len_l2==len_sb_2-1 and len_l2!=0:
            ''' 6) Check if Bluetooth set is different '''
            if len_l1==len_sa_1-1 and len_l1==len_sa_2-1:
                print("Cond 6")
                mapping = [{str(set(sa_1)-set(l1)),str(set(sa_2)-set(l1))}, {str(set(sb_1)-set(l2)),str(set(sb_2)-set(l2))}]
                old_id, new_id = (set_sb_1-set(l2)).pop(), (set_sb_2-set(l2)).pop()   
                manager.linking_id('WiFi',old_id,new_id)
                old_id, new_id = (set_sa_1-set(l1)).pop(), (set_sa_2-set(l1)).pop()   
                manager.linking_id('Bluetooth',old_id,new_id)        
    else:
        mapping=None
           
    #print(mapping)
    if mapping is not None:
        print("by rule 3")
        print(mapping)
        if not last_rule:
            devices.append(mapping)
        elif last_rule:
            devices.extend(mapping)
            
    return mapping, devices

def rule_4(manager: DeviceManager,line1,line2, devices: list[Device]):
    mapping = None
    sa_1, sb_1, sc_1 = line1["Bluetooth"] if "Bluetooth" in line1 else [], line1["WiFi"] if "WiFi" in line1 else [], line1["LTE"] if "LTE" in line1 else []
    sa_2, sb_2, sc_2 = line2["Bluetooth"] if "Bluetooth" in line2 else [], line2["WiFi"] if "WiFi" in line2 else [], line2["LTE"] if "LTE" in line2 else []
    
    # Prepare set operations and store in variables
    set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
    set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
    set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
    d=list(set_sa_1.intersection(set_sa_2))
    d1=list(set_sb_1.intersection(set_sb_2))
    d2=list(set_sc_1.intersection(set_sc_2))
    
    len_d, len_d1, len_d2 = len(d), len(d1), len(d2)
    len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
    len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)

    if len_d==0:
        if len_d1==1 and len_d2==1 and len_sc_1==len_sb_1 and len_sb_2==len_sc_2:
            mapping={d1[0],d2[0]}
            manager.create_device(None,d1[0],d2[0])
    elif len_d==1 and len_d1==1 and len_d2==1 and len_sc_1==len_sb_1 and len_sb_2==len_sc_2 and len_sa_1==len_sb_1 and len_sa_1==len_sc_1 and len_sa_2==len_sb_2 and len_sa_2==len_sc_2:
            mapping={d[0],d1[0],d2[0]}
            manager.create_device(d[0],d1[0],d2[0])
            
    if mapping is not None:    
        print("by rule 4")
        print(mapping)
        devices.append(mapping)
    
    return devices


def elimination(mapping, line1, line2):
    sa_1, sb_1, sc_1 = line1["Bluetooth"] if "Bluetooth" in line1 else [], line1["WiFi"] if "WiFi" in line1 else [], line1["LTE"] if "LTE" in line1 else []
    sa_2, sb_2, sc_2 = line2["Bluetooth"] if "Bluetooth" in line2 else [], line2["WiFi"] if "WiFi" in line2 else [], line2["LTE"] if "LTE" in line2 else []

    l = list(set(sa_1) - set(mapping))
    l1 = list(set(sa_2).intersection(set(l)))

    l2 = list(set(sb_1) - set(mapping))
    l3 = list(set(sb_2).intersection(set(l2)))

    l4 = list(set(sc_1) - set(mapping))
    l5 = list(set(sc_2).intersection(set(l4)))

    if len(l1) == 0:
        if len(l3) == 1 and len(l5) == 1:
            print(l3[0], l5[0])
    else:
        if len(l3) == 1 and len(l5) == 1 and len(l1) == 1:
            print(l1[0], l3[0], l5[0])
    
    # to do mapping
    
    
    
    
    
    
    
    
# def rule_5(manager: DeviceManager, line1,line2, devices: list[Device]):
#     sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
#     sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
#     sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    
#     sa_2 = [item[1] for item in line2 if item[0] == 'Bluetooth']
#     sb_2 = [item[1] for item in line2 if item[0] == 'WiFi']
#     sc_2 = [item[1] for item in line2 if item[0] == 'LTE']  
      
#     # Prepare set operations and store in variables
#     set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
#     set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
#     set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
#     d=list(set_sa_2.intersection(set_sa_1))
#     d1=list(set_sb_2.intersection(set_sb_1))
#     d2=list(set_sc_2.intersection(set_sc_1))
    
#     len_d = len(d)
#     len_d1 = len(d1)
#     len_d2 = len(d2)

#     l1=list(set(sa_2)-set(d))
#     l2=list(set(sb_2)-set(d1))
#     l3=list(set(sc_2)-set(d2))
    
#     len_l1, len_l2, len_l3 = len(l1), len(l2), len(l3)
    
#     len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
#     len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
    
#     if len_l1==0:
#         if len_l2==1 and len_l3==1 and len_d1==len_sb_2 and len_d2==len_sc_2:
#             mapping=((l2[0],l3[0]))
#             manager.create_device(None,l2[0],l3[0])
#         else:
#             mapping=None
#     else:
#         if len_l2==1  and len_l3==1 and len_l1==1 and len_d==len_sc_2 and len_d1==len_sb_2 and len_d2==len_sc_2:
#             mapping=((l1[0],l2[0],l3[0]))
#             manager.create_device(l1[0],l2[0],l3[0])
#         else:
#             mapping=None

#     if mapping is not None:
#         print("by rule 5")  
#         print(mapping)
#         devices.append(mapping)
    
#     return devices    
  
# def rule_6(manager: DeviceManager, line1,line2, devices: list[Device]):
#     sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
#     sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
#     sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    
#     sa_2 = [item[1] for item in line2 if item[0] == 'Bluetooth']
#     sb_2 = [item[1] for item in line2 if item[0] == 'WiFi']
#     sc_2 = [item[1] for item in line2 if item[0] == 'LTE']    

#     # Prepare set operations and store in variables
#     set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
#     set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
#     set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
#     d=list(set_sa_2.intersection(set_sa_1))
#     d1=list(set_sb_2.intersection(set_sb_1))
#     d2=list(set_sc_2.intersection(set_sc_1))
    
#     len_d = len(d)
#     len_d1 = len(d1)
#     len_d2 = len(d2)

#     l1=list(set(sa_1)-set(d))
#     l2=list(set(sb_1)-set(d1))
#     l3=list(set(sc_1)-set(d2))
    
#     len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
#     len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
    
#     len_l1, len_l2, len_l3 = len(l1), len(l2), len(l3)

#     if len_l1==0:
#         if len_l2==1 and len_l3==1 and len_d1==len_sb_1 and len_d2==len_sc_1:
#             mapping=[(l2[0],'WiFi'),(l3[0],'LTE')]
#             manager.create_device(None,l2[0],l3[0])
#         else:
#             mapping=None
#     else:
#         if len_l2==1  and len_l3==1 and len_l1==1 and len_d==len_sc_1 and len_d1==len_sb_1 and len_d2==len_sc_1:
#             mapping=[(l1[0],'Bluetooth'),(l2[0],'WiFi'),(l3[0],'LTE')]
#             manager.create_device(l1[0],l2[0],l3[0])
#         else:
#             mapping=None
    
#     if mapping is not None: 
#         print("by rule 6")   
#         print(mapping)
#         devices.append(mapping)

#     return devices


