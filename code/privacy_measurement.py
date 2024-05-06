import csv
import json
import numpy as np
import multiprocessing
import pickle
import matplotlib.pyplot as plt



privacy=dict()

f=open('user_traces.json')
user_traces=json.load(f)
f.close()

f1 = open('20240505194120_sniffed_data.json')
data = json.load(f1)
f1.close()

observed=dict()

for user_id in user_traces.keys():
     maxim=-1
     traces=user_traces[user_id]
     for item in traces:
         length=len(item)
         if length>maxim:
             maxim=length
     count=0  
     l=[]
     for line in data:
         if user_id in line.values():
              if line['timestep'] not in l:
                   l.append(line['timestep'])
                   count=count+1
     observed[user_id]=l
     
     privacy[user_id]=maxim/len(observed[user_id])
     
print(observed)
values = list(privacy.values())

user=[]
for i in range(200): 
    user_id = "User{}".format(i + 1)
    user.append(user_id)

for item in user:
    if item not in privacy.keys():
        privacy[item]=0
# Calculate PDF using numpy


values = list(privacy.values())
pdf, bins = np.histogram(values, bins=len(set(values)), density=True)

plt.bar(bins[:-1], pdf, width=np.diff(bins), edgecolor='black', align='edge')
plt.xlabel('Privacy Score')
plt.ylabel('Frequncy of users having the privacy score')
plt.title('PDF of Privacy Scores of Users')
plt.show()
plt.savefig("privacy_score_distribution.pdf")




print(privacy)
print(len(user_traces.keys()))

#for item not in user_traces.keys():
 #   privacy[item]=0



              
     
