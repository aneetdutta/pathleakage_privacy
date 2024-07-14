import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Define marker interval
marker_interval = 50

plt.figure(figsize=(10, 6))

# Load the CSV files
baseline_wifi_df = pd.read_csv(f'csv/multi_protocol_scenario5c2_partial.csv')
baseline_wifi_scores = baseline_wifi_df['privacy_score'].values
baseline_wifi_scores_sorted = np.sort(baseline_wifi_scores)
baseline_wifi_users = np.arange(1, len(baseline_wifi_scores_sorted) + 1)
plt.plot(baseline_wifi_users, baseline_wifi_scores_sorted, label='LTE Only Coverage (No Multilateration)', linestyle='-', alpha=0.7, linewidth=3, color="#66c2a5", marker='o', markevery=marker_interval)

baseline_ble_df = pd.read_csv(f'csv/multi_protocol_scenario5d2_partial.csv')
baseline_ble_scores = baseline_ble_df['privacy_score'].values
baseline_ble_scores_sorted = np.sort(baseline_ble_scores)
baseline_ble_users = np.arange(1, len(baseline_ble_scores_sorted) + 1)
plt.plot(baseline_ble_users, baseline_ble_scores_sorted, label='LTE Only Coverage (Multilateration)', linestyle='-', alpha=0.7, linewidth=3, color="#8da0cb", marker='s', markevery=marker_interval)

baseline_lte_df = pd.read_csv(f'csv/multi_protocol_scenario5b2.csv')
baseline_lte_scores = baseline_lte_df['privacy_score'].values
baseline_lte_scores_sorted = np.sort(baseline_lte_scores)
baseline_lte_users = np.arange(1, len(baseline_lte_scores_sorted) + 1)
plt.plot(baseline_lte_users, baseline_lte_scores_sorted, label='Full Coverage (Multilateration)', linestyle='-', alpha=0.7, linewidth=3, color="#fdc086", marker='v', markevery=marker_interval)

multi_protocol_df = pd.read_csv(f'csv/multi_protocol_scenario1a2.csv')  
multi_protocol_scores = multi_protocol_df['privacy_score'].values
multi_protocol_scores_sorted = np.sort(multi_protocol_scores)
multi_protocol_users = np.arange(1, len(multi_protocol_scores_sorted) + 1)
plt.plot(multi_protocol_users, multi_protocol_scores_sorted, label='Full Coverage (No Multilateration)', alpha=0.7, linewidth=3, color="#000000", marker='*', markevery=marker_interval)

# plt.margins(0)
# plt.autoscale(enable=True, axis='both', tight=True)

xticks = np.linspace(min(multi_protocol_users), max(multi_protocol_users), math.floor(len(multi_protocol_users)/50))
xticks = np.round(xticks).astype(int)
plt.xticks(xticks, fontsize=22)
plt.yticks(fontsize=22)
plt.xlabel('Number of Users', fontsize=22)
plt.ylabel('Privacy Leakage', fontsize=22)
plt.legend(loc='lower right', fontsize=15)
plt.grid(True)
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.savefig(f'images/privacy_leakage_q4c.pdf', dpi=600, bbox_inches='tight')
plt.show()
