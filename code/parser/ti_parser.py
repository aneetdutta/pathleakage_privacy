import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import pyshark.packet

import pyshark
from services.general import group_identifiers
from collections import defaultdict
import math
import numpy as np
import glob
# filename = 'data/sample3.pcap'

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        # Add other types here if needed
        return super(NumpyEncoder, self).default(obj)


rnti_dict = defaultdict(list)
tmsi_dict = defaultdict(list)
random_dict = defaultdict(list)
pcap_data = []

folder_path = '/media/wisec/data/paper_pcaps_final/'
file_dict = defaultdict(defaultdict)
temp2_dict= {}

for filename in sorted(glob.glob(os.path.join(folder_path, '*.pcap'))):
    temp_dict = {}
    tranmission_times = set()
    new_filename = filename.replace(folder_path, "").replace(".pcap", "")
    s = new_filename.split("_")
    print(new_filename)
    
    if s[0] == "wifi":
        with pyshark.FileCapture(filename, display_filter="", keep_packets=True) as cap:
            for i, packet in enumerate(cap):
                tranmission_times.add((float(packet.frame_info.time_relative)))
    elif s[0] == "lte":
        with pyshark.FileCapture(filename, display_filter="mac-lte.direction == 0", keep_packets=True, ) as cap:
            for i, packet in enumerate(cap):
                # print(packet.frame_info._all_fields)
                # print(packet.frame_info.time_relative)
                tranmission_times.add((float(packet.frame_info.time_relative)))
    elif s[0] == "ble":
        with pyshark.FileCapture(filename, display_filter="", keep_packets=True, ) as cap:
            for i, packet in enumerate(cap):
                # print(packet.frame_info._all_fields)
                # print(packet.frame_info.time_relative)
                tranmission_times.add((float(packet.frame_info.time_relative)))
                # break
        # print(sorted(list(tranmission_times)))
    transmission_interval = np.diff(sorted(list(tranmission_times)))
    print(len(transmission_interval))
    max = int(np.max(transmission_interval))
    min = int(np.min(transmission_interval))
    avg = float(np.average(transmission_interval))
    stats = {"min": min, "max": max, "avg": avg}
    temp2_dict[new_filename] = list(transmission_interval)
    temp_dict[new_filename.replace(f"_{s[1]}", "")] = {"stats": stats, "transmission_interval": list(transmission_interval)}
    
    file_dict[s[1]].update(temp_dict)

j = json.dumps(file_dict, indent=4,  cls=NumpyEncoder)
with open(f'data/ti_full.json', 'w') as f:
    print(j, file=f)
j = json.dumps(temp2_dict, indent=4,  cls=NumpyEncoder)
with open(f'data/ti.json', 'w') as f:
    print(j, file=f)