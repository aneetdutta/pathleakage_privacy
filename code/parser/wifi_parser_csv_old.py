import pandas as pd
import numpy as np
import json

file_path = "/media/wisec/data/pcap_data/"

opn_mac = ['06:13:c3:47:36:0c', 'e6:52:92:eb:67:59', '26:99:f1:29:6e:51', 'a6:9d:0d:7f:df:0f', '6a:06:40:61:52:e2', 'b6:49:36:26:b5:06', '46:12:b9:a7:6a:11', '92:0b:8d:d5:69:65', 'fa:a0:b7:93:a4:57', '9a:ec:c2:fb:5c:24', '96:ab:e2:eb:8f:09', 'fe:af:a3:e3:98:26', '12:b0:6e:c5:09:e6', '3e:69:55:8a:c5:e5', '36:5f:3f:11:7a:cc', '72:19:10:9a:07:8e', '3a:ae:9c:83:9b:40', 'd2:33:98:20:e1:a7', '56:56:84:db:50:ff', '22:98:b2:7f:2c:55', 'da:24:e4:95:f3:b9', '8a:01:48:ac:e2:40', 'c2:58:79:04:de:8d', '5e:b6:54:01:2d:70', 'ae:b7:8d:c1:70:f9', 'de:6c:79:72:ef:3a', 'ee:64:7a:77:7c:56', '6e:8b:30:de:5b:47', '46:95:fc:6b:5a:4f', '6a:fb:d3:fc:87:af', 'e6:f2:b8:1e:49:6b', 'f2:d6:9a:d1:22:b9', 'd6:98:a1:22:9c:91', '96:9c:f2:92:17:aa', '42:0a:fd:f3:f7:34', 'ca:82:a6:ef:30:51', '7a:ee:c7:50:e4:0e', '3e:74:20:b9:ef:36', 'd2:86:c5:64:7d:ea', '7a:3e:e7:f9:b3:50', '96:ec:62:29:3a:54', 'fe:4a:ad:86:72:bc', '5a:8e:52:59:05:2a', '3a:e7:aa:90:00:f5', '26:3b:c3:f4:af:35', '0e:cd:44:d1:7a:9b', '82:b0:11:38:b5:31', 'da:5b:1b:67:58:df', '4e:bc:63:1b:20:ac', '62:9a:a5:50:e0:01', '1e:65:bd:e1:2f:a2']
redmi_mac = ['5a:db:69:e2:d1:83', 'ee:14:9d:6d:85:84', '56:43:df:07:69:0b', 'e8:5a:8b:6c:c3:2b', '3e:7e:0d:51:49:b1', 'ea:5a:8b:92:b1:b0', '42:cf:99:fd:16:77', '52:54:64:5a:ec:bf', 'cc:47:40:02:56:ef', '3a:b2:7a:60:98:ad', '42:0c:98:a2:6e:0f', 'fa:ee:3f:91:12:63', '8e:4a:47:a7:99:70', 'c2:84:2d:56:f8:c5', '02:b9:85:79:82:39', '4e:67:9b:96:8c:13', 'd2:7c:26:3c:d0:95', '36:bc:f7:4a:dc:69', '5a:ca:7e:4c:3c:5a', '42:a0:c5:56:0f:16', '7a:3b:ec:f9:68:62']

filenames = [("wifi_redmi_ideal_disconnected",redmi_mac) , ("wifi_opn_ideal_disconnected", opn_mac)]

wifi_dict = {}

for file in filenames:
    wifi_dict[file[0]] = {}
    df = pd.read_csv(f'{file_path}{file[0]}.csv')
    col_time_list = df['Time'].tolist()
    np_transmit = np.array(col_time_list)
    wifi_dict[file[0]]["transmission_interval"] = list(np.diff(np_transmit))
    mac_dict = {}
    mac = file[1]

    ids = set()
    randomization_time = []
    for index, row in df.iterrows():
        if row['Source'] in mac:
            if row['Source'] in mac_dict:
                mac_dict[row['Source']] +=1
            else:
                mac_dict[row['Source']] = 1
                randomization_time.append(row['Time'])
        elif row['Destination'] in mac:
            if row['Destination'] in mac_dict:
                mac_dict[row['Destination']] +=1
            else:
                mac_dict[row['Destination']] = 1
                randomization_time.append(row['Time'])
            
    # print(randomization_time, mac_dict)
    # print(np.mean(randomization_time))
    np_random = np.array(randomization_time)
    wifi_dict[file[0]]["randomization_interval"] = list(np.diff(np_random))
    wifi_dict[file[0]]["randomization_statistics"] = {"mean": np.mean(np_random), "median": np.median(np_random), "min": np.min(np_random), "max": np.max(np_random)}
    wifi_dict[file[0]]["transmission_statistics"] = {"mean": np.mean(np_transmit), "median": np.median(np_transmit), "min": np.min(np_transmit), "max": np.max(np_transmit)}

# print(wifi_dict)

j = json.dumps(wifi_dict, indent=4)
with open('/media/wisec/data/pcap_data/paper_pcap/json/wifi_data.json', 'w') as f:
    print(j, file=f)