import csv
import json
import numpy as np
import multiprocessing
import pickle
# Opening JSON file




f2=open('linked_ids.json')
linked_ids=json.load(f2)
f2.close()


print(len(linked_ids))


f1 = open('user_data.json')
 
# returns JSON object as 
# a dictionary
data_user = json.load(f1)
 

f1.close()

count=0
userid1=1
userid2=100
for key,value in linked_ids.items():
    print(key,value)
    for line in data_user:
        if key in line.values():
            userid1=line['user_id']
            print(userid1)
        if value in line.values():
            #print(line['user_id'])
            userid2=line['user_id']
            print(userid2)
        if userid1==userid2:
            count=count+1
            break
            
            
print(count/len(linked_ids))
        
        
