
	

import json
import numpy as np
import multiprocessing
# Opening JSON file
f = open('sniffed_user.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
#for i in data:
 #   print(i['timestep'])
 
# Closing file
f.close()

mapped_devices=dict()
linked_ids=dict()


class Device:
    def __init__(self, bluetooth_id, wifi_id, lte_id):
        self.bluetooth_id = bluetooth_id
        self.lte_id = lte_id
        self.wifi_id = wifi_id

class DeviceManager:
    def __init__(self):
        self.devices = {}
        self.device_list = []

    def create_device(self,bluetooth_id,wifi_id,lte_id):
        flag=0
        flag1=0
        flag2=0
        for device in self.device_list:
            if getattr(device,'bluetooth_id') is not None and getattr(device,'bluetooth_id')==bluetooth_id:
                
                flag=1
            if getattr(device,'wifi_id') is not None and getattr(device,'wifi_id')==wifi_id:
                
                flag1=1
            if getattr(device,'lte_id') is not None and getattr(device,'lte_id')==lte_id:
                
                flag2=1
                
            if flag==1 or flag1==1 or flag2==1:
                self.update_device(device,bluetooth_id,wifi_id,lte_id)  
                return  
            #elif flag==0 and flag1==1 and flag2==1:
             #   self.update_device(device,bluetooth_id,wifi_id,lte_id)
              #  return
            #elif flag==1 and flag1==1 and flag2==1:
             #   return
            #else:  
             #   print("new device") 
              #  new_device = Device(bluetooth_id,wifi_id,lte_id)
        #self.devices[new_device.field1] = new_device
               # self.device_list.append(new_device)
                #return
                
        new_device = Device(bluetooth_id,wifi_id,lte_id)
        #self.devices[new_device.field1] = new_device
        self.device_list.append(new_device)
        #print(f"Device with {field_to_check} '{value_to_check}' created.")

    def update_device(self,device,bluetooth_id,wifi_id,lte_id):
        
        if bluetooth_id is not None and device.bluetooth_id!=bluetooth_id:
            linked_ids[device.bluetooth_id]=bluetooth_id
            device.bluetooth_id = bluetooth_id
            
        if wifi_id is not None and device.wifi_id!=wifi_id:
            linked_ids[device.wifi_id]=wifi_id
            device.wifi_id = wifi_id
            
        if lte_id is not None and device.lte_id!=lte_id:
            linked_ids[device.lte_id]=lte_id
            device.lte_id = lte_id
            
                
        return
        
        
    def linking_id(self,protocol,old_id,new_id):
        print("link device")
        for device in self.device_list:
            
            if protocol=='Bluetooth':
                if getattr(device,'bluetooth_id') == old_id:
                    device.bluetooth_id = new_id
            if protocol=='WiFi':
                if getattr(device,'wifi_id') == old_id:
                    device.wifi_id=new_id
            if protocol=='LTE':
                if getattr(device,'lte_id') == old_id:
                    device.lte_id=new_id
                    
                
        return







def maptoran(item1,item2):
    l=[]
    l1=[]
    #print(item1[0])
    #print(type(item1))
    for item in item1:
        #print(type(item))
        l.append(list(item))
    #print(l)
    l_new=list(np.concatenate(l))
    for item in item2:
        l1.append(list(item))
    #print(type(set(l)))
    l1_new=list(np.concatenate(l1))
    d=set(l_new).intersection(set(l1_new))
    if len(d)!=0:
        m.append((set(l_new)-set(l1_new),set(l1_new)-set(l_new)))
        

def rule_1(line1,line2):#invoked after checking the condition of time and location
    #print("By Rule 1")
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[1]=='Bluetooth':
            sa_1.append(item[0])
        elif item[1]=='WiFi':
            sb_1.append(item[0])
        elif item[1]=='LTE':
            sc_1.append(item[0])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    for item in line2:
        if item[1]=='Bluetooth':
            sa_1.append(item[0])
        elif item[1]=='WiFi':
            sb_1.append(item[0])
        elif item[1]=='LTE':
            sc_1.append(item[0])
    if len(sa_1)==1 and len(sb_1)==0 and len(sc_1)==0 and len(sa_2)==1 and len(sb_2)==0 and len(sc_2)==0:
        mapping=(sa_1[0],sb_2[0])
    elif len(sa_1)==0 and len(sb_1)==1 and len(sc_1)==0 and len(sa_2)==0 and len(sb_2)==1 and len(sc_2)==0:
        mapping=(sb_1[0],sb_2[0])
    elif len(sa_1)==0 and len(sb_1)==0 and len(sc_1)==1 and len(sa_2)==0 and len(sb_2)==0 and len(sc_2)==1:
        mapping=(sc_1[0],sc_2[0])
        
        
        
        
    else:
        mapping=None
    #print(mapping)
    if mapping is not None:
        print("by rule 1")
        print(mapping)
        devices.append(mapping)

def rule_2(manager,line1):
     #print("By Rule 2")
     #manager = DeviceManager()
     sa_1=[]
     sb_1=[]
     sc_1=[]
     for item in line1:
         #print(item)
         if item[0]=='Bluetooth':
             sa_1.append(item[1])
         elif item[0]=='WiFi':
             sb_1.append(item[1])
         elif item[0]=='LTE':
             sc_1.append(item[1])
             
     d=len(sa_1)
     d1=len(sb_1)
     d2=len(sc_1)
     #print(d)
     #print(d1)
     #print(d2)
     if d==1 and d1==1 and d2!=1:
         #print("hi")
         mapping=(set(sa_1),set(sb_1))
         manager.create_device(set(sa_1).pop(),set(sb_1).pop(),None)
         
         
     elif d!=1 and d1==1 and d2==1:
         mapping=(set(sb_1),set(sc_1))
         manager.create_device(None,set(sb_1).pop(),set(sc_1).pop())
     elif d==1 and d1==1 and d2==1:
         mapping=(set(sa_1),set(sb_1),set(sc_1))
         manager.create_device(set(sa_1).pop(),set(sb_1).pop(),set(sc_1).pop())
     
     else:
         mapping=None
     
     if mapping is not None:
         print("by rule 2")
         print(mapping)
         devices.append(mapping)
     #print(mapping)
     
   
def rule_3(manager,line1,line2):
    #print("By rule 3")
    #print(line1)
    #print(line2)
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[0]=='Bluetooth':
            sa_1.append(item[1])
        elif item[0]== 'WiFi':
            #print(item[0])
            sb_1.append(item[1])
        elif item[0]=='LTE':
            sc_1.append(item[1])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        #print(item[i])
        if item[0]=='Bluetooth':
            sa_2.append(item[1])
        elif item[0] == 'WiFi':
            sb_2.append(item[1])
        elif item[0]=='LTE':
            
            sc_2.append(item[1])

    l1=set(sa_1).intersection(set(sa_2))
    #r1=set(sa_2).intersection(set(sa_1)
    
    
    l2=set(sb_1).intersection(set(sb_2))
    #r2=set(sb_2)-set(sb_1)
    
    l3=set(sc_1).intersection(set(sc_2))
    #print(l1)
    #print(l2)
    #print(l3)
    #r3=set(sc_2)-set(sc_1)
    #print(sb_1)
    #print(sb_2)
    #print(l3)
    #print(r3)
    
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
def elimination(mapping,line1,line2):
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
            
    l=list(set(sa_1)-set(mapping))
    l1=list(set(sa_2).intersection(set(l)))
    
    l2=list(set(sb_1)-set(mapping))
    l3=list(set(sb_2).intersection(set(l2)))
            
    l4=list(set(sc_1)-set(mapping))
    l5=list(set(sc_2).intersection(set(l4)))
    
    if len(l1)==0:
        if len(l3)==1 and len(l5)==1:
            print(l3[0],l5[0])
    else:
        if len(l3)==1 and len(l5)==1 and len(l1)==1:
            print(l1[0],l3[0],l5[0])   
            
        


def find_sublist_containing_value(data, value):
    for sublist in data:
        if value in sublist:
            return sublist
    return None


def calculate_distance(line1, line2):
    # Assuming line1 and line2 are dictionaries with 'x' and 'y' keys representing coordinates
    #print(line1)
    #print(line2)
    return ((line1['location'][0] - line2['location'][0]) ** 2 + (line1['location'][1] - line2['location'][1]) ** 2) ** 0.5

def group_lines_by_distance(lines, threshold_distance):
    #print(line)
    groups = []
    #groups = []
    flag=0
    for line in lines:
        #print("+++")
        #if line['protocol']=='LTE':
         #   if line['lte_id']=='LTEDevice7':
          #      print(line)
           #     print("=====================")
        #print(line)
        #print("+++")
        #if line['protocol']=='WiFi':
         #   if line['WiFi_id']=='MDRP782HZS39':
            
          #      print(line)
           #     flag=1
            #    print("--------")
        distance_threshold_lte=10
        distance_threshold=1
        added_to_existing_group = False
        lte=False
        list2=[]
        for group in groups:
 
    	    for line_in_group in group:
    	        
                distance = calculate_distance(line, line_in_group)
               # if flag==1:
                #print(line_in_group)
                #print("---------------")
                 #   print(distance)
                #if line_in_group['protocol']=='LTE' or line['protocol']=='LTE':
                 #   distance_threshold=20
                #else:
                #	distance_threshold=1 
                #if line['protocol']=='LTE':
                
                 #   if line['lte_id']=='LTEDevice7':
                  #      print(line_in_group)
                   #     print("********")
                        #print(line_in_group)
                   
                if distance <= distance_threshold_lte and distance<=distance_threshold:
                    #print(line)
                    group.append(line)
                    added_to_existing_group = True
                    break
                elif distance<=distance_threshold_lte and distance>distance_threshold:
                    if line['protocol']=='LTE':
                        #print(line)
                        group.append(line)
                        added_to_existing_group = True
                        #break
                    elif line_in_group['protocol']=='LTE':
                        list2.append(line_in_group)
                        #print(list2)
                        lte=True
                        added_to_existing_group = False
                        
                  #  lte=True
                   # group2.append(line_in_group)
             #   	if flag==1:
              #  	    print(added_to_existing_group)
                	#break
    	    if added_to_existing_group:
        	    continue
	# If the line does not fit into any existing group, create a new group
        if not added_to_existing_group and not lte:
            groups.append([line])
        if not added_to_existing_group and lte:
            list2.append(line)
            #for item in list2:
                #print(item)
            groups.append(list2)
            #groups.append([line])
            #print(line)
            #group.append(line)
        #elif not added_to_existing_group and lte:
         #   for item in group2:
          #      print(item)
                #groups.append(item)
            #groups.append(line)
        #print(groups)
    #print("----------")
    return groups


    




def group_lines_by_field(timed_data,sniffer_id,specific_values):
    #groups = {}
    groups = [[] for _ in range(len(specific_values))]
    for line in timed_data:
        #print(line)
        if sniffer_id in line and line[sniffer_id] in specific_values:
                index = specific_values.index(line[sniffer_id])
                groups[index].append(line)
    
    return groups




def extract_lines_with_same_time(data, target_time):
    #lines_with_same_time=[]

    
    for line in data:
        
        if line['timestep'] == target_time:
            #print(line['timestep'])
            lines_with_same_time.append(line)
            

   



target_time=0
T=[]
devices=[]
D=dict()
for target_time in range(0,500):
    lines_with_same_time = []
    print("----")
    #print(target_time)
    extract_lines_with_same_time(data,target_time)
    #print(lines_with_same_time)
    #specific_values=[0,1,2,3,4]
    groups = group_lines_by_distance(lines_with_same_time,0.1)
    #print(groups)
    for item in groups:
        #print(item)
        l=[]
        for i in range(len(item)):
            if item[i]['protocol']=='Bluetooth':
                #print(item[i]['protocol'])
                l.append((item[i]['protocol'],item[i]['bluetooth_id']))
            elif item[i]['protocol']=='WiFi':
                l.append((item[i]['protocol'],item[i]['WiFi_id']))
            elif item[i]['protocol']=='LTE':
                l.append((item[i]['protocol'],item[i]['lte_id']))
        l=list(set(l))    
        #print(l)        
        #print("*********")
        if target_time in D.keys():
            L=D[target_time]
            L.append(l)
            D[target_time]=L
        else:
            L=[]
            L.append(l)
            D[target_time]=L
 
r={}  
binding={}    
manager = DeviceManager()     
for target_time in range(0,499):
    if target_time in D.keys():
        l=D[target_time]
    
    new_target=target_time+1
    for j in range(new_target,new_target+1):
         
        if j in D.keys():
            l1=D[j]
        else:
           j = new_target+1
           continue
    
        for item in l:
        #print(item)
            rule_2(manager,item)
            for item1 in l1:
                mapping=rule_3(manager,item,item1)
                if mapping is not None:
                    #print("---")
                    #print(mapping)
                    linked_ids[mapping[0].pop()]=mapping[1].pop()
                mapping=rule_1(item,item1)
                if mapping is not None:
                    #print("---")
                    #print(mapping)
                    linked_ids[mapping[0].pop()]=mapping[1].pop()
                
                rule_4(manager,item,item1)
                rule_5(item,item1)
                rule_6(item,item1)
    print("=========")

#print(D)
#print(linked_ids)

#for item in r.keys():
 #   print(item)
  #  print(r[item])
   # print("----------------")
#({'IDI8ZODMQ4U8'}, {'ONF66ZSF9Q93'})



for device in manager.device_list:
    print(device.bluetooth_id, device.wifi_id, device.lte_id)

print(linked_ids)    

tracking=[]
def generate_traces(bluetooth_id,wifi_id,lte_id):
    flag=0
    flag1=0
    flag2=0
    for line in data:
        if line['protocol']=='Bluetooth' and line['bluetooth_id']==bluetooth_id:
            #print(line)
            tracking.append(line['timestep'])
        if line['protocol']=='WiFi' and line['WiFi_id']==wifi_id:
            #print(line)
            tracking.append(line['timestep'])
        if line['protocol']=='LTE' and line['lte_id']==lte_id:
            #print(line)
            tracking.append(line['timestep'])
    for key,value in linked_ids.items():
        if value==lte_id:
            lte_id=str(key)
            #print(lte_id)
            flag=1
        
        if value==bluetooth_id:
            bluetooth_id=str(key)
            flag=1
        
        if value==wifi_id:
            wifi_id=str(key)
            flag=1
        
    if flag==1:
        generate_traces(bluetooth_id,wifi_id,lte_id)
    else:
        return


for device in manager.device_list:
    #generate_traces(str(device.bluetooth_id),str(device.wifi_id),str(device.lte_id))
    a=device.bluetooth_id
    b=device.wifi_id
    c=device.lte_id
    generate_traces(a,b,c)
    print(set(tracking))
    tracking=[]
    #print("------------------")
with open('mapping.json', 'w') as f:
    json.dump(devices, f)
    
with open("linked_ids.json", "w") as f:
    json.dump(linked_ids, f)