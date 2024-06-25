import os, sys

import pyshark.packet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyshark
from services.general import group_identifiers
from collections import defaultdict
filename = 'data/sample.pcap'

rnti_dict = defaultdict(list)
tmsi_dict = defaultdict(list)
random_dict = defaultdict(list)
pcap_data = []
with pyshark.FileCapture(filename, display_filter="mac-lte", keep_packets=True) as cap:
    for i, packet in enumerate(cap):
        packet_mac_dict = dict(packet["mac-lte"]._all_fields)
        time_epoch = float(packet.frame_info.time_epoch)
        identifiers = set()
        if int(packet_mac_dict['mac-lte.rnti-type']) == 2:
            type_ = "RAR"
            '''RAR Packet'''
            if packet_mac_dict["mac-lte.rar.ta"]:
                ta = packet_mac_dict["mac-lte.rar.ta"]
            else:
                ta = None
            
            rnti = f'RNTI_{str(packet_mac_dict["mac-lte.rar.temporary-crnti"])}'
            identifiers.add(rnti)
        
        if int(packet_mac_dict["mac-lte.rnti-type"]) == 3:
            if "mac-lte.control.timing-advance.command" in packet_mac_dict:
                ta = packet_mac_dict["mac-lte.control.timing-advance.command"]
            else:
                ta = None
            
            type_ = "SCH"
            rnti = f'RNTI_{str(packet_mac_dict["mac-lte.rnti"])}'
            identifiers.add(rnti)
            
            if "lte-rrc.rrcConnectionRequest_element" in packet_mac_dict:
                type_ = "Request"
                # RRC Connection Request
                if "lte-rrc.m_TMSI" in packet_mac_dict:
                    # M-TMSI Exists
                    tmsi = f'TMSI_{int(str(packet_mac_dict["lte-rrc.m_TMSI"]).replace(":",""), 16)}'  
                    identifiers.add(tmsi)                       
                    
                elif "lte-rrc.randomValue" in packet_mac_dict:
                    random = f'RANDOM_{str(packet_mac_dict["lte-rrc.randomValue"].replace(":", ""))}'    
                    identifiers.add(random)  
                                            
            elif "lte-rrc.rrcConnectionSetupComplete_element" in packet_mac_dict:
                type_ = "SetupComplete"
                # RRC Connection Setup
                if "nas_eps.emm.m_tmsi" in packet_mac_dict:
                    # M-TMSI Exists
                    tmsi = f'TMSI_{str(packet_mac_dict["nas_eps.emm.m_tmsi"])}'
                    identifiers.add(tmsi)
                                            
            elif "lte-rrc.rrcConnectionReconfiguration_element" in packet_mac_dict:
                type_ = "Reconfiguration"
                # RRC Reconfiguration
                if "nas_eps.emm.m_tmsi" in packet_mac_dict:
                    # M-TMSI Exists
                    tmsi = f'TMSI_{str(packet_mac_dict["nas_eps.emm.m_tmsi"])}'
                    identifiers.add(tmsi)


            elif "lte-rrc.rrcConnectionReestablishmentRequest_element" in packet_mac_dict:
                # RRC Reestablishment Req
                type_ = "ReestablishmentRequest"
                if "lte-rrc.c_RNTI" in packet_mac_dict:
                    c_rnti_old = f'RNTI_{int(str(packet_mac_dict["lte-rrc.c_RNTI"]).replace(":",""), 16)}'
                    identifiers.add(c_rnti_old)
            
        for id in identifiers:
            if "RNTI" in id:
                rnti_dict[id].append((i, time_epoch, type_, identifiers, ta))
            if "TMSI" in id:
                tmsi_dict[id].append((i, time_epoch, type_, identifiers, ta))
            if "RANDOM" in id:
                random_dict[id].append((i, time_epoch, type_, identifiers, ta))
 
        
        pcap_data.append((i, time_epoch, type_, identifiers, ta))
        
# print(pcap_data)
# print(rnti_dict)
# print(len(pcap_data))  
   
chained_data = []

i= 0

# groups = []
# identifier_to_group = {}

# for i, time_epoch, type_, identifiers, ta in pcap_data:
#     current_group = None
    
#     # Find the group for the current tuple
#     for identifier in identifiers:
#         if identifier in identifier_to_group:
#             current_group = identifier_to_group[identifier]
#             break
    
#     # If no existing group is found, create a new one
#     if current_group is None:
#         current_group = len(groups)
#         groups.append(set())
    
#     # Add the identifiers to the found/created group
#     groups[current_group].update(identifiers)
    
#     # Update the identifier to group mapping
#     for identifier in identifiers:
#         identifier_to_group[identifier] = current_group

final_list =  group_identifiers(pcap_data)#[set(group) for group in groups]

print(final_list)
# while i < len(pcap_data)-1:
#     print(i)
#     chain = []
#     print(len(chained_data), "len")
#     if chained_data:
#         i = chained_data[-1][-1][0]+1
#     if i >=len(pcap_data):
#         break
#     temp_packet = pcap_data[i]
#     chain.append(temp_packet)
#     # print(chain)
#     appended_in_loop = False
#     for packet in pcap_data[i+1::]:
#         # print(packet)
#         if packet[3].intersection(temp_packet[3]):
#             chain.append(packet)
#             temp_packet = packet
#             print('Intersected')
#             # print(chain)
#         # elif any("RANDOM" in s for s in packet[3]):
#         #     chained_data.append(chain)
#         #     appended_in_loop = True
#         #     break
#     # print(i, chain)
#     # if chain in chained_data:
#     #     i=i+1
#     if not appended_in_loop:
#         print('Appended chain')
#         chained_data.append(chain)
#         appended_in_loop = False
        
with open("data/file.txt", 'w') as file:
    for item in final_list:
        file.write(f"{item}\n")
        
# import json
# with open("data/file.json", "w") as f:
#     json.dump(convert_sets_to_lists(chained_data), f)
# print(chained_data)