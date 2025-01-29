import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def remove_outliers(values, percentile=90):
    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, percentile)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return [x for x in values if lower_bound <= x <= upper_bound]

with open(f"/home/aneet_wisec/usenix_2025/path-leakage/real_world/ti.json", 'r') as f:
    data = json.load(f)


data["ble_opn_randomization"] = [723, 795, 546, 431]
data["ble_sm11_randomization"] = [662, 897, 817]

data["ble_opn_disconnected"] = data["ble_opn"]
data["ble_sm11_disconnected"] = data["ble_sm11"]

records = []

# Parse the JSON data
for key, values in data.items():
    print(key)
    
    protocol, device, *mode = key.split('_')
    mode = '_'.join(mode) if mode else None
    
    # if protocol == "ble":
    #     print(values)
    
    if (protocol == "wifi"):
        if (mode == "connected_inactive"):
            values = remove_outliers(values, percentile=90)
        if (mode == "connected_active"):
            values = remove_outliers(values, percentile=90)
            
    if (protocol == "lte"):
        if mode == "inactive":
            values = remove_outliers(values, percentile=98)
        if mode == "active":
            values = remove_outliers(values, percentile=98)
        
    for value in values:
        records.append({
            'protocol': protocol,
            'device': device,
            'mode': mode,
            'transmission_time': value
        })

# Convert the list of records to a pandas DataFrame
df = pd.DataFrame(records)

# print(df.max())
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

d = ['OnePlus Nord', 'Xiaomi Redmi k50i', 'Samsung Galaxy M11']

# Add a new column to the dataframe for device labels
df['device_label'] = df['device'].map(device_labels)

# Define the conditions for each plot
conditions = [
    {'protocol': 'lte', 'mode': 'inactive'},
    {'protocol': 'lte', 'mode': 'active'},
    {'protocol': 'wifi', 'mode': 'connected_inactive'},
    {'protocol': 'wifi', 'mode': 'connected_active'},
    # {'protocol': 'wifi', 'mode': 'connected'},
    {'protocol': 'wifi', 'mode': 'disconnected'},
    {'protocol': 'ble', 'mode': 'randomization'},
    {'protocol': 'ble', 'mode': 'disconnected'},
]

# Set font sizes for a 12pt research paper
plt.rcParams.update({
    'font.size': 24,
    'axes.titlesize': 24,
    'axes.labelsize': 24,
    'xtick.labelsize': 22,
    'ytick.labelsize': 22,
    'legend.fontsize': 20,
    # 'figure.titlesize': 16
})


def half_violinplot(data, ax, x, y, **kwargs):
    sns.violinplot(data=data, ax=ax, x=x, y=y, **kwargs)
    for patch in ax.artists:  # Loop through all violin components
        patch.set_edgecolor('black')  # Set edge color for violins
        patch.set_linewidth(1)

    # Get unique x-ticks and clip the right half of the violin for each tick
    for collection in ax.collections:
        path = collection.get_paths()[0]
        # x_mean = np.mean(path.vertices[:, 0])
        # path.vertices[:, 0] = np.clip(path.vertices[:, 0], a_min=None, a_max=x_mean)
        path.vertices[:, 0] = np.clip(path.vertices[:, 0], a_min=None, a_max=np.mean(path.vertices[:, 0]))
        
    for tick, label in enumerate(data[x].unique()):
            subset = data[data[x] == label][y]
            
            # Calculate statistics
            # mean_val = subset.mean()
            median_val = subset.median()
            
            # Get x-coordinate for the tick
            x_coord = tick
            
            # Plot mean line
            # ax.hlines(y=mean_val, xmin=x_coord - 0.05, xmax=x_coord + 0.05, 
            #         colors='blue', linestyle='-', linewidth=2, label='Mean')
            
            # Plot median line
            ax.hlines(y=median_val, xmin=x_coord - 0.05, xmax=x_coord + 0.05, 
                    colors='blue', linestyle='-', linewidth=1, label='Median')
            

    x_min, x_max = ax.get_xlim()
    ax.set_xlim(x_min, x_max - 0.4)
    
    for line in ax.lines:  # Loop through box plot lines
        line.set_color("red")  # Set box plot color
        line.set_linewidth(1.0)  

# # --------------------------------------------------------------
# #                   LTE Mode
# # --------------------------------------------------------------
#     # Filter subsets for LTE active and inactive
lte_active = df[(df['protocol'] == 'lte') & (df['mode'] == 'active')]
lte_inactive = df[(df['protocol'] == 'lte') & (df['mode'] == 'inactive')]

# # Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(3.3,2.1), sharey=False)
plt.subplots_adjust(wspace=0.7)
# # Plot LTE active
half_violinplot(
     x='device_label', y='transmission_time', data=lte_inactive, 
     inner='box', scale='width', palette=device_palette, cut=0, ax=axes[0]
)
axes[0].set_title('LTE - Inactive',fontsize=8)
# # axes[0].set_xlabel('Device')
axes[0].set_ylabel('Trans Intv (s)',fontsize=8)
#axes[0].set_yscale('log')
axes[0].set_ylim(0,55)
axes[0].set_xlabel('') 
axes[0].set_xticks([])
 # axes[0].tick_params(axis='x', pad=-100, margin=0)

# # Plot LTE inactive
half_violinplot(
     x='device_label', y='transmission_time', data=lte_active, 
     inner='box', scale='width', palette=device_palette, cut=0, ax=axes[1]
)
axes[1].set_title('LTE - Active',fontsize=8)
axes[1].set_ylim(0, 5.5)
axes[1].set_ylabel('')
axes[1].set_xlabel('') 
axes[1].set_xticks([])



handles, labels = axes[0].get_legend_handles_labels()
for ax in axes:
    ax.tick_params(axis='both', which='major', labelsize=8)

fig.legend(
     handles=[*[mpatches.Patch(color=device_palette[label], label=label) for label in d],
         Line2D([0], [0], color='blue', linestyle='-', linewidth=1, label='Mean'),
         # Line2D([0], [0], color='black', linestyle='--', linewidth=2, label='Median'),
     ],
     labels=d,
     loc='lower center',
     ncol=len(device_labels),
     fontsize=5,
     handleheight=0.8,  # Reduce patch height
     handlelength=0.8,  # Reduce patch length
)
#plt.subplots_adjust(bottom=0.25)
plt.rc('savefig', bbox='tight')
plt.rc('savefig', pad_inches=0.02)
filename = '/home/aneet_wisec/usenix_2025/path-leakage/real_world/lte_combined_active_inactive.pdf_new.pdf'
plt.savefig(filename)
# plt.subplots_adjust(bottom=0.16)  # Adjust bottom to fit legend

# # Save the combined plot
# filename = 'real_world/lte_combined_active_inactive.pdf'
# with PdfPages(filename) as pdf:
#     pdf.savefig(dpi=600, bbox_inches='tight')
# plt.close()


# --------------------------------------------------------------
#                   WIFI Mode
# --------------------------------------------------------------


wifi_disconnected = df[(df['protocol'] == 'wifi') & (df['mode'] == 'disconnected')]
wifi_connected_inactive = df[(df['protocol'] == 'wifi') & (df['mode'] == 'connected_inactive')]
wifi_connected_active = df[(df['protocol'] == 'wifi') & (df['mode'] == 'connected_active')]

# Create a figure with three subplots
fig, axes = plt.subplots(1, 3, figsize=(7, 1.65), sharey=False)

# Plot WiFi disconnected
half_violinplot(
    x='device_label', y='transmission_time', data=wifi_disconnected, 
    inner='box', scale='width', palette=device_palette, cut=0, ax=axes[0]
)
axes[0].set_title('WiFi - Disconnected',fontsize=8)
axes[0].set_ylim(0, 320)  # Adjust Y-axis limits for WiFi disconnected
axes[0].set_ylabel('Trans Intv (s)',fontsize=8)
axes[0].set_xlabel('')
axes[0].set_xticks([])

# Plot WiFi connected inactive
half_violinplot(
    x='device_label', y='transmission_time', data=wifi_connected_inactive, 
    inner='box', scale='width', palette=device_palette, cut=0, ax=axes[1]
)
axes[1].set_title('WiFi - Connected Inactive',fontsize=8)
axes[1].set_ylim(0, 55)  # Adjust Y-axis limits for WiFi connected inactive
axes[1].set_ylabel('')
axes[1].set_xlabel('')
axes[1].set_xticks([])

# Plot WiFi connected active
half_violinplot(
    x='device_label', y='transmission_time', data=wifi_connected_active, 
    inner='box', scale='width', palette=device_palette, cut=0, ax=axes[2]
)
axes[2].set_title('WiFi - Connected Active',fontsize=8)
axes[2].set_ylim(0, 0.4)  # Adjust Y-axis limits for WiFi connected active
axes[2].set_ylabel('')
axes[2].set_xlabel('')
axes[2].set_xticks([])

# Add a common legend
handles, labels = axes[0].get_legend_handles_labels()
for ax in axes:
    ax.tick_params(axis='both', which='major', labelsize=8)
    


fig.legend(
    handles=[*[mpatches.Patch(color=device_palette[label], label=label) for label in d],
        Line2D([0], [0], color='blue', linestyle='-', linewidth=1, label='Mean'),
        # Line2D([0], [0], color='black', linestyle='--', linewidth=2, label='Median'),
    ],
    labels=d,
    loc='lower center',
    ncol=len(device_labels),
    fontsize=8,
    handleheight=0.9,  # Reduce patch height
    handlelength=0.9,  # Reduce patch length
)



plt.subplots_adjust(bottom=0.23)

#plt.rc('figure', figsize=(THIRD_WIDTH,THIRD_WIDTH*HEIGHT_RATIO))

#7 Inches it the entire page, 3.33 is a column and 2.1 works if you want 3 next to each other with decent spacing
plt.rc('savefig', bbox='tight')
plt.rc('savefig', pad_inches=0.02) # 0 and 0.01 crop the frame/axis labels

# Adjust layout to fit the legend
# plt.subplots_adjust(bottom=0.14, left=0.05, right=0.95, top=0.9)
#plt.subplots_adjust(bottom=0.16) 
# Save the combined plot
filename = '/home/aneet_wisec/usenix_2025/path-leakage/real_world/wifi_combined_disconnected_connected_new.pdf'
plt.savefig(filename)
#with PdfPages(filename) as pdf:
 #   pdf.savefig(dpi=600, bbox_inches='tight')
plt.close()




# # --------------------------------------------------------------
# #                   BLE Mode
# # --------------------------------------------------------------

d = ['OnePlus Nord', 'Samsung Galaxy M11']

ble_ti = df[(df['protocol'] == 'ble') & (df['mode'] == 'disconnected')]
ble_ri = df[(df['protocol'] == 'ble') & (df['mode'] == 'randomization')]

# # Create a figure with three subplots
fig, axes = plt.subplots(1, 2, figsize=(3.3, 1.5), sharey=False)
plt.subplots_adjust(wspace=0.7)
# # Plot WiFi disconnected
half_violinplot(
   x='device_label', y='transmission_time', data=ble_ti, 
   inner='box', scale='width', palette=device_palette, cut=0, ax=axes[0]
)
axes[0].set_title('')
axes[0].set_ylim(0, None)  # Adjust Y-axis limits for WiFi disconnected
axes[0].set_ylabel('Trans Intv (s)',fontsize=8)
axes[0].set_xlabel('')
axes[0].set_xticks([])

# # Plot WiFi connected inactive
half_violinplot(
    x='device_label', y='transmission_time', data=ble_ri, 
    inner='box', scale='width', palette=device_palette, cut=0, ax=axes[1]
)
axes[1].set_title('')
axes[1].set_ylim(0, None)  # Adjust Y-axis limits for WiFi connected inactive
axes[1].set_ylabel('Rand Intv (s)',fontsize=8)
axes[1].set_xlabel('')
axes[1].set_xticks([])

# # Add a common legend
handles, labels = axes[0].get_legend_handles_labels()
for ax in axes:
   ax.tick_params(axis='both', which='major', labelsize=8)
    

fig.legend(
    handles=[*[mpatches.Patch(color=device_palette[label], label=label) for label in d],
        Line2D([0], [0], color='blue', linestyle='-', linewidth=1, label='Mean'),
         # Line2D([0], [0], color='black', linestyle='--', linewidth=2, label='Median'),
    ],
    labels=d,
    loc='lower center',
    ncol=len(device_labels),
    fontsize=5,
    handleheight=0.8,  # Reduce patch height
    handlelength=0.8,  # Reduce patch length
)
plt.subplots_adjust(bottom=0.2)
plt.rc('savefig', bbox='tight')
plt.rc('savefig', pad_inches=0.02)
filename = '/home/aneet_wisec/usenix_2025/path-leakage/real_world/ble_combined_ti_ri_new.pdf'
plt.savefig(filename)
# # Adjust layout to fit the legend
# # plt.subplots_adjust(bottom=0.14, left=0.05, right=0.95, top=0.9)
# plt.subplots_adjust(bottom=0.18) 
# # Save the combined plot
# filename = 'real_world/ble_combined_ti_ri.pdf'
# with PdfPages(filename) as pdf:
#     pdf.savefig(dpi=600, bbox_inches='tight')
# plt.close()


#################################
#             OLD               #
#################################

# # Plot violin plots with box plots for each condition and save them as PDF files
# for condition in conditions:
#     protocol = condition['protocol']
#     mode = condition['mode']
    
    
#     if mode:
#         subset = df[(df['protocol'] == protocol) & (df['mode'] == mode)]
#         title = f'{protocol.upper()} - {mode.replace("_", " ").capitalize()}'
#         filename = f'images_plot_/{protocol}_{mode}.pdf'
#     else:
#         subset = df[df['protocol'] == protocol]
#         title = f'{protocol.upper()}'
#         filename = f'images_plot_/{protocol}.pdf'
    
#     plt.figure(figsize=(12, 6))
#     # if condition
#     sns.violinplot(x='device_label', y='transmission_time', data=subset, inner='box', scale='width', palette=device_palette, cut=0)
#     # Adjust the plot to only show the left side
#     # plt.title(title)
#     plt.xlabel('Device')
#     if condition["mode"] == "randomization":
#         plt.ylabel('Randomization Interval')
#     else:
#         plt.ylabel('Transmission Interval')
#     plt.ylim(0, None)  # Ensure the y-axis starts at 0 to avoid negative values display
#     plt.tight_layout()
    
#     plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    
#     # Save plot to PDF
#     with PdfPages(filename) as pdf:
#         pdf.savefig(dpi=600, bbox_inches='tight')
#     plt.close()
