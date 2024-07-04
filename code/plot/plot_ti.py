import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import json

with open("data/ti.json") as f:
    json_data = json.load(f)
    
total_devices = 3#len(list(json_data))
total_items = 5
# list_of_empty_lists = [[1] for _ in range(total_items)]
data_by_device = [[1] * total_items for _ in range(len(json_data))]
print(data_by_device)

i=0
for device, data in json_data.items():
    # print(device)
    # print(i)
    for d, item_ in data.items():
        if d == "lte_inactive":
            data_by_device[i][0] = item_["transmission_interval"]
        if d == "lte_active":
            data_by_device[i][1] = item_["transmission_interval"]
        if d == "wifi_disconnected":
            data_by_device[i][2] = item_["transmission_interval"] 
        if d == "wifi_connected_inactive":
            data_by_device[i][3] = item_["transmission_interval"]       
        if d == "wifi_connected_active":
            data_by_device[i][4] = item_["transmission_interval"]  
        print(i, d)
        print(data_by_device)
    i=i+1
    # print(filename, list(data))
# print(data_by_device)
print("in")
# Sample data for 3 devices, each with 5 elements
# Organize the data by device
# data_by_device = [data[i*5:(i+1)*5] for i in range(total_devices)]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Colors for the violin plots and box plots
violin_colors = plt.cm.viridis(np.linspace(0, 1, 5))
box_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700']
modes = ['LTE (Inactive Mode)', 'LTE (Active Mode)', 'WiFi (Disconnected Mode)', 'WiFi (Connected, Inactive Mode)', 'WiFi (Connected, Active Mode)']

# Plotting violins and boxes for each device
positions = np.arange(1, 16)  # Total 15 positions for 3 devices * 5 elements each
for i, device_data in enumerate(data_by_device):
    # Offset positions for each device
    # print(i)
    # print(device_data)
    offset = i * 5
    if not device_data:
        device_data = []
    violin_parts = ax.violinplot(device_data, positions=positions[offset:offset+5], showmeans=False, showmedians=False, showextrema=False)
    
    # Customize the violin plot colors
    for j, pc in enumerate(violin_parts['bodies']):
        pc.set_facecolor(violin_colors[j])
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)  # Add transparency

    # Create a box plot on top of the violin plot with smaller width
    box_parts = ax.boxplot(device_data, positions=positions[offset:offset+5], patch_artist=True, widths=0.1, showfliers=False)
    
    # Customize the box plot colors
    for box, color in zip(box_parts['boxes'], box_colors):
        box.set(color='darkblue', linewidth=1.5)
        box.set(facecolor=color)
    
    for whisker in box_parts['whiskers']:
        whisker.set(color='darkblue', linewidth=1.5)
    
    for cap in box_parts['caps']:
        cap.set(color='darkblue', linewidth=1.5)
    
    for median in box_parts['medians']:
        median.set(color='red', linewidth=1.5)
    
    for flier in box_parts['fliers']:
        flier.set(marker='o', color='red', alpha=0.5)

# Add grid lines for better readability
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5)

# Set labels and title
ax.set_xlabel('Device', fontsize=14)
ax.set_ylabel('Transmission Interval', fontsize=14)
ax.set_title('Transmission Interval for each device', fontsize=16)

# Set xticks and xticklabels
devices = ['d'] * total_devices
devices[0] = 'OnePlus Nord'
devices[1] = 'Samsung Galaxy M11'
xticks = [2.5, 7.5, 12.5]  # Centered positions for each device
ax.set_xticks(xticks)
ax.set_xticklabels(devices, fontsize=12)

# Add legends
legend_elements = [Patch(facecolor=violin_colors[i], edgecolor='black', label=mode) for i, mode in enumerate(modes)]
legend_elements += [
    Patch(facecolor=box_colors[i], edgecolor='darkblue', label=f'Box - {mode}') for i, mode in enumerate(modes)
]
legend_elements.append(Line2D([0], [0], color='red', lw=1.5, label='Median'))

ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# Improve layout
plt.tight_layout()
plt.savefig('images/plot_ti.pdf', dpi=600)
# Show plot
plt.show()
