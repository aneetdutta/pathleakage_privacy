from env import BLUETOOTH_LOCALIZATION_ERROR, WIFI_LOCALIZATION_ERROR, LTE_LOCALIZATION_ERROR
import copy
from services.general import remove_subsets_and_duplicates

def group_distances(sniffer_groups):
    
    protocol_to_id = {
        "Bluetooth": "bluetooth_id",
        "WiFi": "WiFi_id",
        "LTE": "lte_id",
    }
    
    groups = []  # Initialize list to store final groups

    '''iterate through sniffer_groups'''
    sniffer_groups: dict
    for sg in sniffer_groups:
        # print(sg)
        # print(sg["protocol"], sg[protocol_to_id[sg["protocol"]]], sg['dist_S_U'], "sg_tup")
        sg_tup = (sg["protocol"],sg[protocol_to_id[sg["protocol"]]],sg['dist_S_U'])
        if not groups:
            first_group = set()
            first_group.add(tuple(sg_tup))
            groups.append(first_group)
        incompatible_set: set = set()
        compatible_set: set = set()
        i = 0
        # print(groups, "check")
        groups: list
        while i < len(groups):
            # print(i,group)
            group = groups[i]
            # print(i, group, "check")
            compatible = True  # Flag to check if distance is compatible with the group
            group: list
            for d in group:
                abs_dist = abs(int(d[2]) - int(sg['dist_S_U']))
                # print(d, sg['WiFi_id'], abs_dist)
                if d[0] == "LTE" and sg["protocol"] == "LTE" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "LTE" and sg["protocol"] == "WiFi" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "LTE" and sg["protocol"] == "Bluetooth" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "WiFi" and sg["protocol"] == "LTE" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "WiFi" and sg["protocol"] == "WiFi" and abs_dist <= WIFI_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "WiFi" and sg["protocol"] == "Bluetooth" and abs_dist <= WIFI_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "Bluetooth" and sg["protocol"] == "LTE" and abs_dist <= LTE_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "Bluetooth" and sg["protocol"] == "WiFi" and abs_dist <= WIFI_LOCALIZATION_ERROR:
                    compatible = True
                elif d[0] == "Bluetooth" and sg["protocol"] == "Bluetooth" and abs_dist <= BLUETOOTH_LOCALIZATION_ERROR:
                    compatible = True
                else: 
                    compatible = False
                    # print(compatible, sg['lte_id'], sg['WiFi_id'])
                
                if compatible == True:
                    if d not in compatible_set:
                        compatible_set.add(d)
                        
                elif compatible == False:
                    if d not in incompatible_set:
                        incompatible_set.add(d)
        
            i = i+1
            
        if not compatible_set:
            fg = set()
            fg.add(tuple(sg_tup))
            groups.append(fg)
        else:
            temp_group = copy.deepcopy(groups)
            diff_checker = True
            for i, group in enumerate(groups):
                
                ''' Intersection of Compatible Set and Group - Get common items'''
                common_set = group.intersection(compatible_set)

                if not common_set:
                    continue
                diff = group - compatible_set
                if not diff:
                    temp_group[i].add(sg_tup)
                    diff_checker = False
            if diff_checker:
                compatible_set.add(sg_tup)
                temp_group.append(compatible_set)
            groups = temp_group
    
    '''
    [
        {('WiFi', 'W1', 40), ('LTE', 'L1', 40), ('LTE', 'L2', 30), ('Bluetooth', 'B1', 40)},
        {('LTE', 'L1', 40), ('WiFi', 'W2', 30), ('LTE', 'L2', 30), ('Bluetooth', 'B2', 30)},
        {('WiFi', 'W2', 30), ('LTE', 'L3', 20), ('LTE', 'L2', 30), ('Bluetooth', 'B2', 30)},
        {('WiFi', 'W3', 20), ('LTE', 'L3', 20), ('Bluetooth', 'B3', 20), ('LTE', 'L2', 30)},
        {('WiFi', 'W3', 20), ('Bluetooth', 'B3', 20), ('LTE', 'L4', 10), ('LTE', 'L3', 20)},
        {('Bluetooth', 'B4', 10), ('LTE', 'L3', 20), ('WiFi', 'W4', 10), ('LTE', 'L4', 10)}
    ]
    '''
            
    group_list:list = []
    for element in groups:
        temp_dict = dict()
        for devtup in list(element):
            if devtup[0] in {"Bluetooth", "WiFi", "LTE"}:
                # print(devtup[0], devtup[1])
                if devtup[0] not in temp_dict:
                    temp_dict[devtup[0]] = [devtup[1]]
                else:
                    temp_dict[devtup[0]].append(devtup[1])     
        group_list.append(temp_dict)       
    # defaultdict(list, ((k, list(v)) for k, v in temp_dict.items()))
    return group_list

def grouper(sniffer_data):
    grouped_list = []
    for sniffer_id, data in sniffer_data.items():
        distance_groups = group_distances(data)
        grouped_list.extend(distance_groups)
    
    grouped_list = remove_subsets_and_duplicates(grouped_list)
    
    return grouped_list