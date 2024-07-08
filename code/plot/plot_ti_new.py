import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def remove_outliers(values):
    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return [x for x in values if lower_bound <= x <= upper_bound]



# Load your JSON data (replace 'your_json_data' with the actual JSON string or load from a file)
# your_json_data = """
# {
#     "ble_opn": [10, 20, 30],
#     "ble_sm11": [5, 15, 25],
#     "lte_opn_active": [100, 200, 300],
#     "lte_opn_inactive": [150, 250, 350],
#     "lte_rk50_active": [110, 210, 310],
#     "lte_rk50_inactive": [160, 260, 360],
#     "lte_sm11_active": [120, 220, 320],
#     "lte_sm11_inactive": [170, 270, 370],
#     "wifi_opn_connected_active": [50, 100, 150],
#     "wifi_opn_connected_inactive": [60, 110, 160],
#     "wifi_opn_disconnected": [70, 120, 170],
#     "wifi_rk50_connected_active": [80, 130, 180],
#     "wifi_rk50_connected_inactive": [90, 140, 190],
#     "wifi_rk50_disconnected": [40, 90, 140],
#     "wifi_sm11_connected_inactive": [30, 80, 130],
#     "wifi_sm11_disconnected": [20, 70, 120],
      
# }
# """
with open(f"data/ti.json", 'r') as f:
    data = json.load(f)

data["ble_sm11_randomization"] = [662, 897, 817]
data["ble_opn_randomization"] = [723, 795, 546, 431]
# Prepare a list to collect the relevant data
records = []

# Parse the JSON data
for key, values in data.items():
    print(key)
    
    protocol, device, *mode = key.split('_')
    mode = '_'.join(mode) if mode else None
    
    if (protocol == "ble") or (protocol == "wifi" and device == "opn" and mode == "connected_active") or (protocol == "wifi" and device == "sm11" and mode == "connected_active"):
        pass
    else:
        values = remove_outliers(values)
        
    for value in values:
        records.append({
            'protocol': protocol,
            'device': device,
            'mode': mode,
            'transmission_time': value
        })

# Convert the list of records to a pandas DataFrame
df = pd.DataFrame(records)

if (df['transmission_time'] < 0).any():
    raise ValueError("Negative values found in transmission_time data.")


# Define a mapping for device labels
device_labels = {
    'opn': 'OnePlus Nord',
    'sm11': 'Samsung Galaxy M11',
    'rk50': 'Xiaomi Redmi k50i'
}

device_palette = {
    device_labels['opn']: '#EF9C66',
    device_labels['sm11']: '#FCDC94',
    device_labels['rk50']: '#C8CFA0'
}

# Add a new column to the dataframe for device labels
df['device_label'] = df['device'].map(device_labels)

# Define the conditions for each plot
conditions = [
    {'protocol': 'lte', 'mode': 'inactive'},
    {'protocol': 'lte', 'mode': 'active'},
    {'protocol': 'wifi', 'mode': 'connected_inactive'},
    {'protocol': 'wifi', 'mode': 'connected_active'},
    {'protocol': 'wifi', 'mode': 'disconnected'},
    {'protocol': 'ble', 'mode': None},
    {'protocol': 'ble', 'mode': 'randomization'}
]

# Set font sizes for a 12pt research paper
plt.rcParams.update({
    'font.size': 24,
    'axes.titlesize': 24,
    'axes.labelsize': 24,
    'xtick.labelsize': 22,
    'ytick.labelsize': 22,
    'legend.fontsize': 22,
    # 'figure.titlesize': 16
})

# Plot violin plots with box plots for each condition and save them as PDF files
for condition in conditions:
    protocol = condition['protocol']
    mode = condition['mode']
    
    if mode:
        subset = df[(df['protocol'] == protocol) & (df['mode'] == mode)]
        title = f'{protocol.upper()} - {mode.replace("_", " ").capitalize()}'
        filename = f'{protocol}_{mode}.pdf'
    else:
        subset = df[df['protocol'] == protocol]
        title = f'{protocol.upper()}'
        filename = f'{protocol}.pdf'
    
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='device_label', y='transmission_time', data=subset, inner='box', scale='width', palette=device_palette, cut=0)
    # plt.title(title)
    plt.xlabel('Device')
    if condition["mode"] == "randomization":
        plt.ylabel('Randomization Interval')
    else:
        plt.ylabel('Transmission Interval')
    plt.ylim(0, None)  # Ensure the y-axis starts at 0 to avoid negative values display
    plt.tight_layout()
    
    # Save plot to PDF
    with PdfPages(filename) as pdf:
        pdf.savefig()
    plt.close()