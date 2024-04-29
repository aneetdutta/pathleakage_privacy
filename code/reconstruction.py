import csv
import json
import numpy as np
import multiprocessing
import pickle
# Opening JSON file



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






pickle_file='manager.pkl'
with open(pickle_file, 'rb') as file:
    manager = pickle.load(file)


f2=open('linked_ids.json')
linked_ids=json.load(f2)
f2.close()


f1 = open('user_data.json')
 
# returns JSON object as 
# a dictionary
data_user = json.load(f1)
 

f1.close()


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

























ground_truth=[]
reconstructed=[]




def generate_traces(bluetooth_id,wifi_id,lte_id):
    flag=0
    
    for line in data:
        if line['protocol']=='Bluetooth' and line['bluetooth_id']==bluetooth_id:
            #print(line)
            tracking.append(line['timestep'])
            #r.append(bluetooth_id)
        if line['protocol']=='WiFi' and line['WiFi_id']==wifi_id:
            #print(line)
            #r.append(wifi_id)
            tracking.append(line['timestep'])
        if line['protocol']=='LTE' and line['lte_id']==lte_id:
            #print(line)
            tracking.append(line['timestep'])
            #r.append(lte_id)
        
        
                
            
       
    if lte_id in linked_ids.keys():
        lte_id=linked_ids[lte_id]
            #print(lte_id)
        flag=1
        
    if bluetooth_id in linked_ids.keys():
        bluetooth_id=linked_ids[bluetooth_id]  
        flag=1
        
    if wifi_id in linked_ids:
        wifi_id=linked_ids[wifi_id]
        flag=1
        
    if flag==1:
        generate_traces(bluetooth_id,wifi_id,lte_id)
    else:
        
        
        return
        

tracking=[]
user_traces=dict()
for device in manager.device_list:
    a=device.bluetooth_id
    b=device.wifi_id
    c=device.lte_id
    print(a)
    print(b)
    print(c)
    user_id=0
    for line in data_user:
        if a is not None and line['bluetooth_id']==a:
            user_id=line['user_id']
            break
        if b is not None and line['wifi_id']==b:
            user_id=line['user_id']
            break
        if c is not None and line['lte_id']==c:
            user_id=line['user_id']
            break
        
    generate_traces(a,b,c)
    if user_id in user_traces.keys():
        l=user_traces[user_id]
        l.append(list(set(tracking)))
    else:
        l=[]
        l.append(list(set(tracking)))
        user_traces[user_id]=l
    tracking=[]
    if len(user_traces[user_id])==1:
        print(user_id)
        print(user_traces[user_id])
    else:
        print(user_id)
        for item in user_traces[user_id]:
            print(item)
            print("****")
    print("----------------------------------------")
    
    #print("----")
    


