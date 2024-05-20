from modules.device import Device
import pickle
from funct.fn import extract_orjson


pickle_file='rule2.pkl'
with open(pickle_file, 'rb') as file:
    manager = pickle.load(file)

data_user = extract_orjson('20240506150753_sniffed_data.json')

count=0
user_devices=[]
devices_mapped=[]

device: Device
for device in manager.device_list:
    a,b,c=device.bluetooth_id, device.wifi_id, device.lte_id
    print(a, b, c)
    user_id1=1001
    user_id2=1908
    user_id3=4678
    user_id=9829

    for line in data_user:
        line_values = line.values()
        if a in line_values:
            user_id1=line['user_id']
        if b in line_values:
            user_id2=line['user_id']
        if c in line_values:
            user_id3=line['user_id']
        if a is None and user_id2==user_id3:
            count=count+1
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif user_id1==user_id2 and user_id1==user_id3:
            count=count+1
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif b is None and user_id1==user_id3:
            count=count+1
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
        elif c is None and user_id1==user_id2:
            count=count+1
            if line['user_id'] not in user_devices:
                user_devices.append(line['user_id'])
            break
    print("-----------")    
    print(user_id1, user_id2, user_id3)
    print("-----------")

print(count)
print(count/len(manager.device_list))     



    
