from modules.devicemanager import DeviceManager

def rule_1(line1: list,line2: list, devices):#invoked after checking the condition of time and location            
    sa_1 = [item[0] for item in line1 if item[1] == 'Bluetooth']
    sb_1 = [item[0] for item in line1 if item[1] == 'WiFi']
    sc_1 = [item[0] for item in line1 if item[1] == 'LTE']

    sa_2 = [item[0] for item in line2 if item[1] == 'Bluetooth']
    sb_2 = [item[0] for item in line2 if item[1] == 'WiFi']
    sc_2 = [item[0] for item in line2 if item[1] == 'LTE']
    
    lengths_1 = (len(sa_1), len(sb_1), len(sc_1))
    lengths_2 = (len(sa_2), len(sb_2), len(sc_2))
            
    if lengths_1 == (1, 0, 0) and lengths_2 == (1, 0, 0):
        mapping=(sa_1[0],sb_2[0])
    elif lengths_1 == (0, 1, 0) and lengths_2 == (0, 1, 0):
        mapping=(sb_1[0],sb_2[0])
    elif lengths_1 == (0, 0, 1) and lengths_2 == (0, 0, 1):
        mapping=(sc_1[0],sc_2[0])
    else:
        mapping=None

    if mapping is not None:
        print("by rule 1")
        print(mapping)
        devices.append(mapping)
    return mapping, devices

def rule_2(manager: DeviceManager, line1, devices):
    sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
    sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
    sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    d, d1, d2 = len(sa_1), len(sb_1), len(sc_1)
    set_sa_1, set_sb_1, set_sc_1  = set(sa_1), set(sb_1), set(sc_1)
    
    if d==1 and d1==1 and d2!=1:
        mapping=(set_sa_1,set_sb_1)
        manager.create_device(set_sa_1.pop(),set_sb_1.pop(),None)
    elif d!=1 and d1==1 and d2==1:
        mapping=(set_sb_1,set_sc_1)
        manager.create_device(None,set_sb_1.pop(),set_sc_1.pop())
    elif d==1 and d1==1 and d2==1:
        mapping=(set_sa_1,set_sb_1,set_sc_1)
        manager.create_device(set_sa_1.pop(),set_sb_1.pop(),set_sc_1.pop())
    else:
        mapping=None
    
    if mapping is not None:
        print("by rule 2")
        print(mapping)
        devices.append(mapping)
    return devices
   
def rule_3(manager: DeviceManager, line1, line2, devices):
    sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
    sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
    sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    
    sa_2 = [item[1] for item in line2 if item[0] == 'Bluetooth']
    sb_2 = [item[1] for item in line2 if item[0] == 'WiFi']
    sc_2 = [item[1] for item in line2 if item[0] == 'LTE']

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

def rule_4(manager: DeviceManager,line1,line2, devices):
    sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
    sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
    sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    
    sa_2 = [item[1] for item in line2 if item[0] == 'Bluetooth']
    sb_2 = [item[1] for item in line2 if item[0] == 'WiFi']
    sc_2 = [item[1] for item in line2 if item[0] == 'LTE']
    
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


def rule_5(manager: DeviceManager, line1,line2, devices):
    sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
    sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
    sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    
    sa_2 = [item[1] for item in line2 if item[0] == 'Bluetooth']
    sb_2 = [item[1] for item in line2 if item[0] == 'WiFi']
    sc_2 = [item[1] for item in line2 if item[0] == 'LTE']  
      
    # Prepare set operations and store in variables
    set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
    set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
    set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
    d=list(set_sa_2.intersection(set_sa_1))
    d1=list(set_sb_2.intersection(set_sb_1))
    d2=list(set_sc_2.intersection(set_sc_1))
    
    len_d = len(d)
    len_d1 = len(d1)
    len_d2 = len(d2)

    l1=list(set(sa_2)-set(d))
    l2=list(set(sb_2)-set(d1))
    l3=list(set(sc_2)-set(d2))
    
    len_l1, len_l2, len_l3 = len(l1), len(l2), len(l3)
    
    len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
    len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
    
    if len_l1==0:
        if len_l2==1 and len_l3==1 and len_d1==len_sb_2 and len_d2==len_sc_2:
            mapping=((l2[0],l3[0]))
            manager.create_device(None,l2[0],l3[0])
        else:
            mapping=None
    else:
        if len_l2==1  and len_l3==1 and len_l1==1 and len_d==len_sc_2 and len_d1==len_sb_2 and len_d2==len_sc_2:
            mapping=((l1[0],l2[0],l3[0]))
            manager.create_device(l1[0],l2[0],l3[0])
        else:
            mapping=None

    if mapping is not None:
        print("by rule 5")  
        print(mapping)
        devices.append(mapping)
    
    return devices    
  
def rule_6(manager: DeviceManager, line1,line2, devices):
    sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
    sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
    sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    
    sa_2 = [item[1] for item in line2 if item[0] == 'Bluetooth']
    sb_2 = [item[1] for item in line2 if item[0] == 'WiFi']
    sc_2 = [item[1] for item in line2 if item[0] == 'LTE']    

    # Prepare set operations and store in variables
    set_sa_1, set_sa_2 = set(sa_1), set(sa_2)
    set_sb_1, set_sb_2 = set(sb_1), set(sb_2)
    set_sc_1, set_sc_2 = set(sc_1), set(sc_2)
    
    d=list(set_sa_2.intersection(set_sa_1))
    d1=list(set_sb_2.intersection(set_sb_1))
    d2=list(set_sc_2.intersection(set_sc_1))
    
    len_d = len(d)
    len_d1 = len(d1)
    len_d2 = len(d2)

    l1=list(set(sa_1)-set(d))
    l2=list(set(sb_1)-set(d1))
    l3=list(set(sc_1)-set(d2))
    
    len_sa_1, len_sb_1, len_sc_1 = len(sa_1), len(sb_1), len(sc_1)
    len_sa_2, len_sb_2, len_sc_2 = len(sa_2), len(sb_2), len(sc_2)
    
    len_l1, len_l2, len_l3 = len(l1), len(l2), len(l3)

    if len_l1==0:
        if len_l2==1 and len_l3==1 and len_d1==len_sb_1 and len_d2==len_sc_1:
            mapping=[(l2[0],'WiFi'),(l3[0],'LTE')]
            manager.create_device(None,l2[0],l3[0])
        else:
            mapping=None
    else:
        if len_l2==1  and len_l3==1 and len_l1==1 and len_d==len_sc_1 and len_d1==len_sb_1 and len_d2==len_sc_1:
            mapping=[(l1[0],'Bluetooth'),(l2[0],'WiFi'),(l3[0],'LTE')]
            manager.create_device(l1[0],l2[0],l3[0])
        else:
            mapping=None
    
    if mapping is not None: 
        print("by rule 6")   
        print(mapping)
        devices.append(mapping)

    return devices
