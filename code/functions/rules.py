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
   
def rule_3(manager,line1,line2):
    sa_1 = [item[1] for item in line1 if item[0] == 'Bluetooth']
    sb_1 = [item[1] for item in line1 if item[0] == 'WiFi']
    sc_1 = [item[1] for item in line1 if item[0] == 'LTE']
    
    sa_2 = [item[1] for item in line2 if item[0] == 'Bluetooth']
    sb_2 = [item[1] for item in line2 if item[0] == 'WiFi']
    sc_2 = [item[1] for item in line2 if item[0] == 'LTE']

    # Prepare set operations and store in variables
    set_sa_1 = set(sa_1)
    set_sa_2 = set(sa_2)

    set_sb_1 = set(sb_1)
    set_sb_2 = set(sb_2)

    set_sc_1 = set(sc_1)
    set_sc_2 = set(sc_2)
    
    l1=set_sa_1.intersection(set_sa_2)
    l2=set_sb_1.intersection(set_sb_2)    
    l3=set_sc_1.intersection(set_sc_2)
    
    sa_lengths = (len(l1), len(sa_1), len(sa_2))
    sb_lengths = (len(l2), len(sb_1), len(sb_2))
    sc_lengths = (len(l3), len(sc_1), len(sc_2))

    
    if len(l1)==len(sa_1) and len(l1)==len(sa_2):
        if len(l2)==len(sb_1) and len(l2)==len(sb_2) and len(l2)!=0:
            if len(l3)==len(sc_1)-1 and len(l3)==len(sc_2)-1:
                print("hello")
                
                mapping=(set(sc_1)-set(l3),set(sc_2)-set(l3))
                old_id=(set(sc_1)-set(l3)).pop()
                new_id=(set(sc_2)-set(l3)).pop()
                
                manager.linking_id('LTE',old_id,new_id)
                #print(mapping)
            else:
                mapping=None
        else:
            mapping=None
    #else:
     #   mapping=None
    elif len(l1)==len(sa_1) and len(l1)==len(sa_2):
        if len(l3)==len(sc_1) and len(l3)==len(sc_2) and len(l3)!=0:
            if len(l2)==len(sb_1)-1 and len(l2)==len(sb_2)-1:
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
    elif len(l2)==len(sb_1) and len(l2)==len(sb_2) and len(l2)!=0:
        if len(l3)==len(sc_1) and len(l3)==len(sc_2)and len(l3)!=0:
            if len(l1)==len(sa_1)-1 and len(l1)==len(sa_2)-1:
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
        #print(line2)   
        #print(len(l2))
        #print(sb_1)
        #print(len(sb_2))
        print(mapping)
        devices.append(mapping)
    return mapping
    
    
        
     

def rule_4(manager,line1,line2):
    #print("by rule 4")
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[0]=='Bluetooth':
            sa_1.append(item[1])
        elif item[0]=='WiFi':
            sb_1.append(item[1])
        elif item[0]=='LTE':
            sc_1.append(item[1])
    #print(sa_1)
    #print(sb_1)
    #print(sc_1)        
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        if item[0]=='Bluetooth':
            sa_2.append(item[1])
        elif item[0]=='WiFi':
            sb_2.append(item[1])
        elif item[0]=='LTE':
            sc_2.append(item[1])
            
    d=list(set(sa_1).intersection(sa_2))
    d1=list(set(sb_1).intersection(sb_2))
    d2=list(set(sc_1).intersection(sc_2))
    #print(d1)
    #print(d2)
    if len(d)==0:
        if len(d1)==1 and len(d2)==1 and len(sc_1)==len(sb_1) and len(sb_2)==len(sc_2):
            mapping=((d1[0],d2[0]))
            manager.create_device(None,d1[0],d2[0])
        else:
            mapping=None
            #print("aneet")
    else:
        if len(d)==1 and len(d1)==1 and len(d2)==1 and len(sc_1)==len(sb_1) and len(sb_2)==len(sc_2) and len(sa_1)==len(sb_1) and len(sa_1)==len(sc_1) and len(sa_2)==len(sb_2) and len(sa_2)==len(sc_2):
            mapping=((d[0],d1[0],d2[0]))
            manager.create_device(d[0],d1[0],d2[0])
        else:
            mapping=None
            
    #if len(d)==0 and len(d1)==0:
     #   if len(d2)==1:
      #      mapping=(set(sc_1)-set(sc_2),set(sc_2)-set(sc_1))
      #  else:
       #     mapping=None
            
   # else:
    #    mapping=None
    if mapping is not None:    
        #print(len(mapping))
        print("by rule 4")
        print(line1)
        print(line2)
        print(mapping)
        devices.append(mapping)
    
    
def rule_6(line1,line2):
    
    
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[0]=='Bluetooth':
            sa_1.append(item[1])
        elif item[0]=='WiFi':
            sb_1.append(item[1])
        else:
            sc_1.append(item[1])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        if item[0]=='Bluetooth':
            sa_2.append(item[1])
        elif item[0]=='WiFi':
            sb_2.append(item[1])
        else:
            sc_2.append(item[1])
    #print(sa_1)
    #print("aneet")
    d=list(set(sa_2).intersection(set(sa_1)))
    l1=list(set(sa_1)-set(d))
    d1=list(set(sb_2).intersection(set(sb_1)))
    #print(d1)
    l2=list(set(sb_1)-set(d1))
    d2=list(set(sc_2).intersection(set(sc_1)))
    #print(d2)
    l3=list(set(sc_1)-set(d2))
    #print(sb_2)
    #print(sc_1)
    
    if len(l1)==0:
        if len(l2)==1 and len(l3)==1 and len(d1)==len(sb_1) and len(d2)==len(sc_1):
            #mapping=(set(sc_1)-set(sc_2),set(sb_1)-set(sb_2))
            #e1=set(sb_1)-set(sb_2)
            #e2=set(sc_1)-set(sc_2)
            mapping=[(l2[0],'WiFi'),(l3[0],'LTE')]
            manager.create_device(None,l2[0],l3[0])
            #e1=set(sb_1)-set(sb_2)
            #e2=set(sc_1)-set(sc_2)
            #print("&&&&&&&&&&")
            #print(mapping)
            #print(T[i])
            
           # for del_item in mapping:
                
                #print(del_item)
            #    T[i][0].pop(T[i][0].index(del_item))
            #print(T[i])
            #print(len(T[i]))
            
           
           # if len(T[i][0])==0:
            #    T[i][0]=mapping
           # else:
            #mapping=[[(l2[0],'WiFi'),(l3[0],'LTE')]]
            #manager.create_device(l1[0],l2[0],l3[0])
            #    T[i].append(mapping)
            #print(T[i])
            #print("&&&&&&&&&&")
            #print("aneet")
        else:
            mapping=None
    else:
        if len(l2)==1  and len(l3)==1 and len(l1)==1 and len(d)==len(sc_1) and len(d1)==len(sb_1) and len(d2)==len(sc_1):
            #mapping=(set(sa_1)-set(sa_2),set(sb_1)-set(sb_2),set(sc_1)-set(sc_2))
            #e1=set(sa_1)-set(sa_2)
            #e2=set(sb_1)-set(sb_2)
            #e3=set(sc_1)-set(sc_2)
            mapping=[(l1[0],'Bluetooth'),(l2[0],'WiFi'),(l3[0],'LTE')]
            manager.create_device(l1[0],l2[0],l3[0])
            #print(mapping)
            #print(T[i][0])
            #for del_item in mapping:
                
               #print(del_item)
             #  T[i][0].pop(T[i][0].index(del_item))
            #print(T[i])
            #print(len(T[i]))
            
            #if len(T[i][0])==0:
             #   T[i]=mapping
            #else:
             #   mapping=[mapping]
              #  T[i].append(mapping)
            #print(T[i][0])
            
        else:
            mapping=None
            
   # if len(d)==0 and len(d1)==0:
    #    if len(d2)==1:
     #       mapping=(set(sc_1)-set(sc_2),set(sc_2)-set(sc_1))
      #  else:
       #     mapping=None
            
   # else:
    #    mapping=None
    
    if mapping is not None: 
        print("by rule 6")   
        print(mapping)
        #print(line1)
        #print(line2)
        devices.append(mapping)
    #print(mapping)
    #T[i][0]="Aneet"
    #rint(T[i][0])
    

       




def rule_5(line1,line2):
    #print("by rule 5")
    #print(line1)
    #print(line2)
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[0]=='Bluetooth':
            sa_1.append(item[1])
        elif item[0]=='WiFi':
            sb_1.append(item[1])
        elif item[0]=='LTE':
            sc_1.append(item[1])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        if item[0]=='Bluetooth':
            sa_2.append(item[1])
        elif item[0]=='WiFi':
            sb_2.append(item[1])
        elif item[0]=='LTE':
            sc_2.append(item[1])
    #print(sb_1)
    #print(sb_2)
    d=list(set(sa_2).intersection(set(sa_1)))
    l1=list(set(sa_2)-set(d))
    
    d1=list(set(sb_2).intersection(set(sb_1)))
    #print(d1)
    l2=list(set(sb_2)-set(d1))
    
    d2=list(set(sc_2).intersection(set(sc_1)))
    #print(d2)
    l3=list(set(sc_2)-set(d2))
    #print(sb_2)
    #print(sb_1)
    #print(d1)
    #print(l2)
    
    if len(l1)==0:
        if len(l2)==1 and len(l3)==1 and len(d1)==len(sb_2) and len(d2)==len(sc_2):
            mapping=((l2[0],l3[0]))
            manager.create_device(None,l2[0],l3[0])
            
            
        else:
            mapping=None
            #print("aneet")
    else:
        if len(l2)==1  and len(l3)==1 and len(l1)==1 and len(d)==len(sc_2) and len(d1)==len(sb_2) and len(d2)==len(sc_2):
            mapping=((l1[0],l2[0],l3[0]))
            manager.create_device(l1[0],l2[0],l3[0])
        else:
            mapping=None
            
    #if len(d)==0 and len(d1)==0:
     #   if len(d2)==1:
            #mapping=(set(sc_1)-set(sc_2),set(sc_2)-set(sc_1))
      #  else:
       #     mapping=None
   # else:
    #    mapping=None
    if mapping is not None:
        print("by rule 5")  
        #print(sb_1)
        #print(line1)
        #print(line2)
        #print(sb_2)  
        print(mapping)
        devices.append(mapping)
    
    #if mapping is not None:
    
    #print(T[i])
    #print("Aneet")
    #T[i][0]=["Aneet"]
    #print(T[i][0])
    
