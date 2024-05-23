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


print(len(linked_ids))


f1 = open('20240507122632_sniffed_data_19400.json')
 
# returns JSON object as 
# a dictionary
data_user = json.load(f1)
 

f1.close()
count=0
userid1=12312321
userid2=104343243240
flag1, flag2 = False, False
for key,value in linked_ids.items():
    print(key,value)
    for line in data_user:
        if key in line.values():
            userid1=line['user_id']
            flag1 = True
        if value in line.values():
            userid2=line['user_id']
            flag2 = True
        if userid1==userid2:
            print(userid2)
            flag1, flag2 = False, False
            userid1=12312321
            userid2=104343243240
            count=count+1
            break
        
        if flag1 and flag2:
            flag2, flag1 = False, False
            print("Not mapped", userid1, userid2)
            
print(count/len(linked_ids))

            
print(count1/len(linked_ids))

count=0


linked_ids_reconstruct = dict()

for key,value in linked_ids.items():
    if key not in linked_ids_reconstruct.values():
        linked_ids_reconstruct[value]=key

file_path = "linked_ids.json"

# Open the file in write mode
with open(file_path, 'w') as json_file:
    # Serialize the dictionary to JSON and write it to the file
    json.dump(linked_ids_reconstruct, json_file)




user_devices=[]
devices_mapped=[]

for device in manager.device_list:
    #generate_traces(str(device.bluetooth_id),str(device.wifi_id),str(device.lte_id))
    a=device.bluetooth_id
    b=device.wifi_id
    c=device.lte_id
    print(a)
    print(b)
    print(c)
    user_id1=1001
    user_id2=1908
    user_id3=4678
    user_id=9829

    
    for line in data_user:
        
        
        if a in line.values():
            user_id1=line['user_id']
        if b in line.values():
            user_id2=line['user_id']
        if c in line.values():
            user_id3=line['user_id']
        if a is None and user_id2==user_id3:
            #print(line['user_id'])
            count=count+1
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif user_id1==user_id2 and user_id1==user_id3:
            count=count+1
            #print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif b is None and user_id1==user_id3:
            count=count+1
            #print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif c is None and user_id1==user_id2:
            count=count+1
            #print(line['user_id'])
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break

    print("-----------")    
    print(user_id1)
    print(user_id2)
    print(user_id3)
    print("-----------")


print(len(user_devices))


print("Number of device binding")
print(count)
print(len(manager.device_list))
print(count/len(manager.device_list))     

print("Linking")
print(count1)
print(len(linked_ids))
    

 
        
