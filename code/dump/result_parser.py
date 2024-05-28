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


def generate_traces(bluetooth_id,wifi_id,lte_id):
    flag=0
    flag1=0
    flag2=0
    for line in data:
        if line['protocol']=='Bluetooth' and line['bluetooth_id']==bluetooth_id:
            #print(line)
            tracking.append(line['timestep'])
            r.append(bluetooth_id)
        if line['protocol']=='WiFi' and line['WiFi_id']==wifi_id:
            #print(line)
            r.append(wifi_id)
            tracking.append(line['timestep'])
        if line['protocol']=='LTE' and line['lte_id']==lte_id:
            #print(line)
            tracking.append(line['timestep'])
            r.append(lte_id)
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












r=[]
count=0
user_devices=[]
for device in manager.device_list:
    #generate_traces(str(device.bluetooth_id),str(device.wifi_id),str(device.lte_id))
    a=device.bluetooth_id
    b=device.wifi_id
    c=device.lte_id
    print(a)
    print(b)
    print(c)
    
    for line in data_user:
        user_id1=0
        user_id2=0
        user_id3=0
        user_id=0
        user_id=line['user_id']
        if a is not None and line['bluetooth_id']==a:
            user_id1=line['user_id']
        if b is not None and line['wifi_id']==b:
            user_id2=line['user_id']
        if c is not None and line['lte_id']==c:
            user_id3=line['user_id']
        if a is None and user_id2==user_id3:
            print(line['user_id'])
            count=count+1
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif user_id1==user_id2 and user_id1==user_id3:
            count=count+1
            print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif b is None and user_id1==user_id3:
            count=count+1
            print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif c is None and user_id1==user_id2:
            count=count+1
            print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        
        
            
            
    #print("------------------")
print(len(manager.device_list))
print(count)
print(len(user_devices))
print(user_devices)

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
        l.append(set(tracking))
    else:
        l=[]
        l.append(set(tracking))
        user_traces[user_id]=l
    tracking=[]
    print(user_traces['user_id'])
    print("----")
#print(user_traces)



file_path = "user_traces_1.pkl"



    

with open(file_path, 'wb') as file:
    pickle.dump(user_traces, file)


