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

for filename in sorted(glob.glob(os.path.join(folder_path, '*.pcap'))):
    temp_dict = {}
    randomization_interval = set()
    ri = set()
    new_filename = filename.replace(folder_path, "").replace(".pcap", "")
    if new_filename != "wifi_opn_disconnected":
        print(new_filename)
        continue
    s = new_filename.split("_")

    t=False
    if s[0] == "wifi" and s[1] == "opn":
        with pyshark.FileCapture(filename, display_filter="", keep_packets=True) as cap:
            for i, packet in enumerate(cap):
                # print(packet.wlan._all_fields)
                # if "sa" in packet
                ta = str(packet.wlan.ta)
                # print(sa)
                randomization_interval.add((math.floor(float(packet.frame_info.time_relative)),ta))
                # break
        for i, j in randomization_interval:
            ri.add(i)
        t=True
        
    transmission_interval = np.diff(sorted(list(ri)))
    print(len(transmission_interval))
    max = int(np.max(transmission_interval))
    min = int(np.min(transmission_interval))
    avg = float(np.average(transmission_interval))
    print(min, max, avg)
    if t:
        break

    print(new_filename)
    # break
    # transmission_interval = np.diff(sorted(list(tranmission_times)))
    # print(len(transmission_interval))
    # max = int(np.max(transmission_interval))
    # min = int(np.min(transmission_interval))
    # avg = float(np.average(transmission_interval))
    # stats = {"min": min, "max": max, "avg": avg}
    # temp_dict[new_filename.replace(f"_{s[1]}", "")] = {"stats": stats, "transmission_interval": list(transmission_interval)}
    # file_dict[s[1]].update(temp_dict)


# j = json.dumps(file_dict, indent=4,  cls=NumpyEncoder)
# with open(f'data/ri.json', 'w') as f:
#     print(j, file=f)
