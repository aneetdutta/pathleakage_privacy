import xml.etree.ElementTree as ET
import json
root_folder = "/home/anonymous"
filepath = f"{root_folder}/MoSTScenario/scenario/in/most.net.xml"
tree = ET.parse(filepath)
root = tree.getroot()

sniffer_location = [(junction.attrib['x'], junction.attrib['y']) for junction in root.iter('junction')]


with open('sniffer_location.json', 'w', encoding='utf-8') as f:
    json.dump({"sniffer_location": sniffer_location}, f, ensure_ascii=False, indent=4)
    