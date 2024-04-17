import json
 
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

def rule_1(line1):
    print("By Rule 1")
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[1]=='Bluetooth':
            sa_1.append(item[0])
        elif item[1]=='WiFi':
            sb_1.append(item[0])
        else:
            sc_1.append(item[0])
    if len(sa_1)==1 and len(sb_1)==1:
        mapping=(sa_1[0],sb_1[0])
        
    else:
        mapping=None
    print(mapping)

def rule_2(line1):
     print("By Rule 2")
     sa_1=[]
     sb_1=[]
     sc_1=[]
     for item in line1:
         if item[1]=='Bluetooth':
             sa_1.append(item[0])
         elif item[1]=='WiFi':
             sb_1.append(item[0])
         else:
             sc_1.append(item[0])
             
     d=len(sa_1)
     d1=len(sb_1)
     d2=len(sc_1)
     
     if d==0 and d1!=0 and d2!=0:
         if d1==1 and d2==1:
             mapping=(set(sb_1),set(sc_1))
         else:
             mapping=None
     elif d==1 and d1==1 and d2==1:
         mapping=(set(sa_1),set(sb_1),set(sc_1))
     else:
         mapping=None
     
     print(mapping)
     
   
def rule_3(line1,line2):
    print("By rule 3")
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[1]=='Bluetooth':
            sa_1.append(item[0])
        elif item[1]=='WiFi':
            sb_1.append(item[0])
        else:
            sc_1.append(item[0])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        if item[1]=='Bluetooth':
            sa_2.append(item[0])
        elif item[1]=='WiFi':
            sb_2.append(item[0])
        else:
            sc_2.append(item[0])

    l1=set(sa_1)-set(sa_2)
    r1=set(sa_2)-set(sa_1)
    
    
    l2=set(sb_1)-set(sb_2)
    r2=set(sb_2)-set(sb_1)
    
    l3=set(sc_1)-set(sc_2)
    r3=set(sc_2)-set(sc_1)
    
    
    
    if len(l1)==0 and len(r1)==0 and len(l2)==0 and len(r2)==0 and len(l3)==1 and len(r3)==1:
        mapping=(l3,r3)
        
    
    elif len(l1)==0 and len(r1)==0 and len(l2)==1 and len(r2)==1 and len(l3)==0 and len(r3)==0:
        mapping=(l2,r2)
        
    
    elif len(l1)==1 and len(r1)==1 and len(l2)==0 and len(r2)==0 and len(l3)==0 and len(r3)==0:
        mapping=(l1,r1)
        
    else:
        mapping=None
        
    print(mapping)
    
    
        
     


def rule_4(line1,line2):
    print("by rule 4")
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[1]=='Bluetooth':
            sa_1.append(item[0])
        elif item[1]=='WiFi':
            sb_1.append(item[0])
        else:
            sc_1.append(item[0])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        if item[1]=='Bluetooth':
            sa_2.append(item[0])
        elif item[1]=='WiFi':
            sb_2.append(item[0])
        else:
            sc_2.append(item[0])
            
    d=set(sa_1).intersection(sa_2)
    d1=set(sb_1).intersection(sb_2)
    d2=set(sc_1).intersection(sc_2)
    
    if len(d)==0:
        if len(d1)==1 and len(d2)==1:
            mapping=(d1,d2)
        else:
            mapping=None
            #print("aneet")
    else:
        if len(d)==1 and len(d1)==1 and len(d2)==1:
            mapping=(d,d1,d2)
        else:
            mapping=None
            
    if len(d)==0 and len(d1)==0:
        if len(d2)==1:
            mapping=(set(sc_1)-set(sc_2),set(sc_2)-set(sc_1))
        else:
            mapping=None
            
    else:
        mapping=None
        
    print(mapping)
    
    
def rule_6(line1,line2):
    print("by rule 6")
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[1]=='Bluetooth':
            sa_1.append(item[0])
        elif item[1]=='WiFi':
            sb_1.append(item[0])
        else:
            sc_1.append(item[0])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        if item[1]=='Bluetooth':
            sa_2.append(item[0])
        elif item[1]=='WiFi':
            sb_2.append(item[0])
        else:
            sc_2.append(item[0])
    #print(sa_1)
    #print("aneet")
    d=set(sa_1)-set(sa_2)
    print(d)
    d1=set(sb_1)-set(sb_2)
    print(d1)
    d2=set(sc_1)-set(sc_2)
    #print(sc_1)
    
    if len(d)==0:
        if len(d1)==1 and len(d2)==1:
            mapping=(set(sc_1)-set(sc_2),set(sb_1)-set(sb_2))
            #print("aneet")
        else:
            mapping=None
    else:
        if len(d)==1 and len(d1)==1 and len(d2)==1:
            mapping=(set(sa_1)-set(sa_2),set(sb_1)-set(sb_2),set(sc_1)-set(sc_2))
        else:
            mapping=None
            
    if len(d)==0 and len(d1)==0:
        if len(d2)==1:
            mapping=(set(sc_1)-set(sc_2),set(sc_2)-set(sc_1))
        else:
            mapping=None
            
    else:
        mapping=None
        
    print(mapping)
    

    

       




def rule_5(line1,line2):
    print("by rule 5")
    sa_1=[]
    sb_1=[]
    sc_1=[]
    for item in line1:
        if item[1]=='Bluetooth':
            sa_1.append(item[0])
        elif item[1]=='WiFi':
            sb_1.append(item[0])
        else:
            sc_1.append(item[0])
            
    sa_2=[]
    sb_2=[]
    sc_2=[]
    
    for item in line2:
        if item[1]=='Bluetooth':
            sa_2.append(item[0])
        elif item[1]=='WiFi':
            sb_2.append(item[0])
        else:
            sc_2.append(item[0])
    
    d=set(sa_2)-set(sa_1)
    d1=set(sb_2)-set(sb_1)
    print(d1)
    d2=set(sc_2)-set(sc_1)
    print(d2)
    
    if len(d)==0:
        if len(d1)==1 and len(d2)==1:
            mapping=(set(sc_2)-set(sc_1),set(sb_2)-set(sb_1))
        else:
            mapping=None
            #print("aneet")
    else:
        if len(d)==1 and len(d1)==1 and len(d2)==1:
            mapping=(set(sa_2)-set(sa_1),set(sb_2)-set(sb_1),set(sc_2)-set(sc_1))
        else:
            mapping=None
            
    if len(d)==0 and len(d1)==0:
        if len(d2)==1:
            mapping=(set(sc_1)-set(sc_2),set(sc_2)-set(sc_1))
        else:
            mapping=None
    else:
        mapping=None
        
    print(mapping)
    

    
    
    
            
        


def find_sublist_containing_value(data, value):
    for sublist in data:
        if value in sublist:
            return sublist
    return None


def calculate_distance(line1, line2):
    # Assuming line1 and line2 are dictionaries with 'x' and 'y' keys representing coordinates
    return ((line1['location'][0] - line2['location'][0]) ** 2 + (line1['location'][1] - line2['location'][1]) ** 2) ** 0.5

def group_lines_by_distance(lines, threshold_distance):
    groups = []
    visited = set()

    for i, line1 in enumerate(lines):
        if i not in visited:
            group = [line1]
            visited.add(i)
            
            
            for j, line2 in enumerate(lines[i + 1:], start=i + 1):
                if j not in visited:
                    distance = calculate_distance(line1, line2)
                    #print(distance)
                    #print(line2['protocol'])
                    if line2['protocol'] == 'LTE':
                        threshold_distance = 20
                    else:
                        threshold_distance=0.1
                    if distance <= threshold_distance:
                        group.append(line2)
                        visited.add(j)
            groups.append(group)
            #print(group)

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
    

    
    for line in data:
        
        if line['timestep'] == target_time:
            #print(line['timestep'])
            lines_with_same_time.append(line)

   



target_time=0
T=[]
for target_time in range(0,500):
    lines_with_same_time = []
    print("----")
    #print(target_time)
    extract_lines_with_same_time(data,target_time)
    #print(lines_with_same_time)
    specific_values=[0,1,2,3,4]
    groups = group_lines_by_field(lines_with_same_time,'sniffer_id',specific_values)





    
    for items in groups:
        
        groups1=group_lines_by_distance(items,1)
        
        l=[]
        for g in groups1:
            #print(g)
            identifiers_group=[]
       
            for i in g:
                #print(len(i))
                if i['protocol'] == 'Bluetooth':
                    identifiers_group.append((i['bluetooth_id'],i['protocol']))
                if i['protocol'] == 'WiFi':
                    identifiers_group.append((i['WiFi_id'],i['protocol']))
                if i['protocol'] == 'LTE':
                   identifiers_group.append((i['lte_id'],i['protocol']))
            #print(len(identifiers_group))
            l.append(identifiers_group)
        print(l)
        T.append(l)
    #T[target_time]=l
    #print(l)
flag=0
for item in T:
    print("******")
    #print(item[0])
    if flag==0:
        prev_item=item
        flag=1
    else:
        for i in range(len(item)):
            rule_1(item[i])
            rule_2(item[i])
            for j in range(len(prev_item)):
                rule_3(prev_item[j],item[i])
                rule_4(prev_item[j],item[i])
                rule_5(prev_item[j],item[i])
                rule_6(prev_item[j],item[i])
                
        prev_item=item
