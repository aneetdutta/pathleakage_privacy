# wlan.tag.oui == 0x8cfdf0
import pyshark

filename =  '/media/wisec/data/pcap_data/wifi_opn_ideal_random.pcapng'#'/media/wisec/data/pcap_data/redminote8pro_ideal_disconnected.pcapng' #wifi_opn_ideal_random.pcapng'

a = {"wifi_opn_ideal_random":"(wlan.tag.oui == 0x8cfdf0 ) && (wlan.fc.type_subtype == 0x0004)", "redminote8pro_ideal_disconnected": "(wlan.tag.oui == 0x0050f2) && (wlan.fc.type_subtype == 0x0004)"}

mac = set()
with pyshark.FileCapture(filename, display_filter=a["wifi_opn_ideal_random"],keep_packets=True) as cap:
    for i, packet in enumerate(cap):
        packet_mac_dict = dict(packet["wlan"]._all_fields)
        mac.add(packet_mac_dict["wlan.sa"])
        mac.add(packet_mac_dict["wlan.sa"])

print(list(mac))
filter = ""
for i in mac:
    if i == len(mac)-1:
        filter += f"wlan.sa == {i} || "
        filter += f"wlan.ra == {i}"
        break
        
    filter += f"wlan.sa == {i} || "
    filter += f"wlan.ra == {i} || "


print(filter)
# # print(mac)


# with pyshark.FileCapture(filename, display_filter=filter,keep_packets=True) as cap:
#     for i, packet in enumerate(cap):
#         print(packet)