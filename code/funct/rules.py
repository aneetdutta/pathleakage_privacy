from modules.devicemanager import DeviceManager
from modules.device import Device


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

def old_id_checker(old_id_t0, new_line_tn1, type_):
    '''To check if old identifier exists anywhere in the tn+1 mapping, if yes, then no linkage, else link them'''
    for item_tn1 in new_line_tn1:
        if old_id_t0 in item_tn1[type_]:
            return True
    return False

def rule_1(line1: list, line2: list, tn1_list:list, devices: list[Device]):#invoked after checking the condition of time and location  
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

    len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
    len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
    
    len_l1, len_l2, len_l3 = len(l1), len(l2), len(l3)    

    if (len_sb_1, len_sc_1, len_sb_2, len_sc_2) == (0, 0, 0, 0): #if rest other protocols are null,
        if len_sa_1 == len_sa_2:
            if len_l1 == 1 and set_sa_1 != set_sa_2: #check if intersection of bluetooth is 1
                print(set_sa_1, set_sa_2, "Bluetooth")
                mapping=l1 if old_id_checker(line1["Bluetooth"][0], tn1_list, 'Bluetooth') else None
    elif (len_sa_1, len_sc_1, len_sa_2, len_sc_2) == (0, 0, 0, 0):
        if len_sb_1 == len_sb_2:
            if len_l2 == 1 and set_sb_1 != set_sb_2:
                print(set_sb_1, set_sb_2, "wifi")
                mapping=l2 if old_id_checker(line1["WiFi"][0], tn1_list, 'WiFi') else None
    elif (len_sa_1, len_sb_1, len_sa_2, len_sb_2) == (0, 0, 0, 0):
        if len_sc_1 == len_sc_2:
            if len_l3 == 1 and set_sc_1!=set_sc_2:
                print(set_sc_1, set_sc_2, "lte")
                mapping=l3 if old_id_checker(line1["LTE"][0], tn1_list, 'LTE') else None
    else:
        mapping=None

    if mapping is not None:
        print("by rule 1")
        print(mapping)
        devices.append(mapping)
    return mapping, devices

def rule_2(manager: DeviceManager, line1, devices: list[Device]):
    sa_1, sb_1, sc_1 = line1["Bluetooth"] if "Bluetooth" in line1 else [], line1["WiFi"] if "WiFi" in line1 else [], line1["LTE"] if "LTE" in line1 else []
    d, d1, d2 = len(sa_1), len(sb_1), len(sc_1)
    set_sa_1, set_sb_1, set_sc_1  = set(sa_1), set(sb_1), set(sc_1)

    if d==1 and d1==1 and d2!=1:
        mapping=(set_sa_1,set_sb_1)
        manager.create_device(next(iter(set_sa_1)),next(iter(set_sb_1)),None)
    elif d!=1 and d1==1 and d2==1:
        mapping=(set_sb_1,set_sc_1)
        manager.create_device(None,next(iter(set_sb_1)),next(iter(set_sc_1)))
    elif d==1 and d1==1 and d2==1:
        mapping=(set_sa_1,set_sb_1,set_sc_1)
        manager.create_device(next(iter(set_sa_1)),next(iter(set_sb_1)),next(iter(set_sc_1)))
    else:
        mapping=None
    
    if mapping is not None:
        # print("by rule 2")
        # print(mapping)
        devices.append(mapping)
    return devices
   
def rule_3(manager: DeviceManager, line1, line2, devices: list[Device]):
    sa_1, sb_1, sc_1 = line1["Bluetooth"] if "Bluetooth" in line1 else [], line1["WiFi"] if "WiFi" in line1 else [], line1["LTE"] if "LTE" in line1 else []
    sa_2, sb_2, sc_2 = line2["Bluetooth"] if "Bluetooth" in line2 else [], line2["WiFi"] if "WiFi" in line2 else [], line2["LTE"] if "LTE" in line2 else []


    # Prepare set operations and store in variables
    set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
    set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
    set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
    l1=set_sa_1.intersection(set_sa_2)
    l2=set_sb_1.intersection(set_sb_2)    
    l3=set_sc_1.intersection(set_sc_2)
    set_l1, set_l2, set_l3 = set(l1), set(l2), set(l3)
    
    len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
    len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
    
    len_l1, len_l2, len_l3 = len(l1), len(l2), len(l3)

    
    if len_l1==len_sa_1 and len_l1==len_sa_2:
        if len_l2==len_sb_1 and len_l2==len_sb_2 and len_l2!=0:
            if len_l3==len_sc_1-1 and len_l3==len(sc_2)-1:
                mapping=(set_sc_1-set(l3),set_sc_1-set(l3))
                old_id=(set_sc_1-set(l3)).pop()
                new_id=(set_sc_2-set(l3)).pop()
                
                manager.linking_id('LTE',old_id,new_id)
                #print(mapping)
            else:
                mapping=None
        else:
            mapping=None
    #else:
     #   mapping=None
    elif len_l1==len_sa_1 and len_l1==len_sa_2:
        if len_l3==len_sc_1 and len_l3==len_sc_2 and len_l3!=0:
            if len_l2==len_sb_1-1 and len_l2==len_sb_2-1:
                mapping=(set(sb_1)-set(l2),set(sb_2)-set(l2))
                old_id=(set(sb_1)-set(l2)).pop()
                new_id=(set(sb_2)-set(l2)).pop()
                manager.linking_id('WiFi',old_id,new_id)
            else:
                mapping=None
        else:
            mapping=None
    #else:
     #   mapping=None
    elif len_l2==len_sb_1 and len_l2==len_sb_2 and len_l2!=0:
        if len_l3==len_sc_1 and len_l3==len_sc_2 and len_l3!=0:
            if len_l1==len_sa_1-1 and len_l1==len_sa_2-1:
                mapping=(set(sa_1)-set(l1),set(sa_2)-set(l1))
                old_id=(set(sa_1)-set(l1)).pop()
                new_id=(set(sa_2)-set(l1)).pop()
                manager.linking_id('Bluetooth',old_id,new_id)
            else:
                mapping=None
        else:
            mapping=None
    else:
        mapping=None
           
    #print(mapping)
    if mapping is not None: 
        print("by rule 3")
        print(line1)
        print(mapping)
        devices.append(mapping)
    return mapping, devices

def rule_4(manager: DeviceManager,line1,line2, devices: list[Device]):
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

    d=list(set(sa_1).intersection(sa_2))
    d1=list(set(sb_1).intersection(sb_2))
    d2=list(set(sc_1).intersection(sc_2))

    if len_d==0:
        if len_d1==1 and len_d2==1 and len_sc_1==len_sb_1 and len_sb_2==len_sc_2:
            mapping=((d1[0],d2[0]))
            manager.create_device(None,d1[0],d2[0])
        else:
            mapping=None
            #print("aneet")
    else:
        if len_d==1 and len_d1==1 and len_d2==1 and len_sc_1==len_sb_1 and len_sb_2==len_sc_2 and len_sa_1==len_sb_1 and len_sa_1==len_sc_1 and len_sa_2==len_sb_2 and len_sa_2==len_sc_2:
            mapping=((d[0],d1[0],d2[0]))
            manager.create_device(d[0],d1[0],d2[0])
        else:
            mapping=None
            
    if mapping is not None:    
        #print(len(mapping))
        print("by rule 4")
        print(line1)
        print(line2)
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


