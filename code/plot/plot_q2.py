import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Define marker interval
marker_interval = 50

plt.figure(figsize=(10, 6))

# Load the CSV files
baseline_wifi_df = pd.read_csv(f'csv/baseline_wifi_scenario1a4.csv')
baseline_wifi_scores = baseline_wifi_df['privacy_score'].values
baseline_wifi_scores_sorted = np.sort(baseline_wifi_scores)
baseline_wifi_users = np.arange(1, len(baseline_wifi_scores_sorted) + 1)
plt.plot(baseline_wifi_users, baseline_wifi_scores_sorted, label='Naive Baseline (WiFi)', linestyle=':', alpha=0.7, linewidth=3, color="#66c2a5", marker='o', markevery=marker_interval)


baseline_loc_wifi_df = pd.read_csv(f'csv/baseline_smart_wifi_scenario4a2.csv')
baseline_loc_wifi_scores = baseline_loc_wifi_df['privacy_score'].values
baseline_loc_wifi_scores_sorted = np.sort(baseline_loc_wifi_scores)
baseline_loc_wifi_users = np.arange(1, len(baseline_loc_wifi_scores_sorted) + 1)
count_users_privacy_1 = baseline_loc_wifi_df[baseline_loc_wifi_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = baseline_loc_wifi_df[baseline_loc_wifi_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = baseline_loc_wifi_df[baseline_loc_wifi_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = baseline_loc_wifi_df[baseline_loc_wifi_df['privacy_score'] >= 0.8].shape[0]
# print(f"Total number of users for BLE-WIFI with privacy_score == 1.0: {count_users_privacy_1}")
# print(f"Total number of users for BLE-WIFI with privacy_score >= 0.95: {count_users_privacy_2}")
# print(f"Total number of users for BLE-WIFI with privacy_score >= 0.9: {count_users_privacy_3}")
# print(f"Total number of users for BLE-WIFI with privacy_score >= 0.8: {count_users_privacy_4}")
plt.plot(baseline_loc_wifi_users, baseline_loc_wifi_scores_sorted, label='Baseline - Localization (WiFi)', alpha=0.7, linewidth=3, color="#bf5b17", marker='<', markevery=marker_interval)

baseline_ble_df = pd.read_csv(f'csv/baseline_ble_scenario1a1.csv')
baseline_ble_scores = baseline_ble_df['privacy_score'].values
baseline_ble_scores_sorted = np.sort(baseline_ble_scores)
baseline_ble_users = np.arange(1, len(baseline_ble_scores_sorted) + 1)
plt.plot(baseline_ble_users, baseline_ble_scores_sorted, label='Naive Baseline (Bluetooth)', linestyle=':', alpha=0.7, linewidth=3, color="#8da0cb", marker='s', markevery=marker_interval)

baseline_loc_ble_df = pd.read_csv(f'csv/baseline_smart_ble_scenario4a2.csv')
baseline_loc_ble_scores = baseline_loc_ble_df['privacy_score'].values
baseline_loc_ble_scores_sorted = np.sort(baseline_loc_ble_scores)
baseline_loc_ble_users = np.arange(1, len(baseline_loc_ble_scores_sorted) + 1)
count_users_privacy_1 = baseline_loc_ble_df[baseline_loc_ble_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = baseline_loc_ble_df[baseline_loc_ble_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = baseline_loc_ble_df[baseline_loc_ble_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = baseline_loc_ble_df[baseline_loc_ble_df['privacy_score'] >= 0.8].shape[0]
# print(f"Total number of users for LTE-WIFI with privacy_score == 1.0: {count_users_privacy_1}")
# print(f"Total number of users for LTE-WIFI with privacy_score >= 0.95: {count_users_privacy_2}")
# print(f"Total number of users for LTE-WIFI with privacy_score >= 0.9: {count_users_privacy_3}")
# print(f"Total number of users for LTE-WIFI with privacy_score >= 0.8: {count_users_privacy_4}")
plt.plot(baseline_loc_ble_users, baseline_loc_ble_scores_sorted, label='Baseline - Localization (Bluetooth)', alpha=0.7, linewidth=3, color="#a6d854", marker='>', markevery=marker_interval)

baseline_lte_df = pd.read_csv(f'csv/baseline_lte_scenario1a1.csv')
baseline_lte_scores = baseline_lte_df['privacy_score'].values
baseline_lte_scores_sorted = np.sort(baseline_lte_scores)
baseline_lte_users = np.arange(1, len(baseline_lte_scores_sorted) + 1)
plt.plot(baseline_lte_users, baseline_lte_scores_sorted, label='Naive Baseline (LTE)', linestyle=':', alpha=0.7, linewidth=3, color="#fdc086", marker='v', markevery=marker_interval)


baseline_loc_lte_df = pd.read_csv(f'csv/baseline_smart_lte_scenario4a2.csv')
baseline_loc_lte_scores = baseline_loc_lte_df['privacy_score'].values
baseline_loc_lte_scores_sorted = np.sort(baseline_loc_lte_scores)
baseline_loc_lte_users = np.arange(1, len(baseline_loc_lte_scores_sorted) + 1)
count_users_privacy_1 = baseline_loc_lte_df[baseline_loc_lte_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = baseline_loc_lte_df[baseline_loc_lte_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = baseline_loc_lte_df[baseline_loc_lte_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = baseline_loc_lte_df[baseline_loc_lte_df['privacy_score'] >= 0.8].shape[0]
# print(f"Total number of users for LTE-BLE with privacy_score == 1.0: {count_users_privacy_1}")
# print(f"Total number of users for LTE-BLE with privacy_score >= 0.95: {count_users_privacy_2}")
# print(f"Total number of users for LTE-BLE with privacy_score >= 0.9: {count_users_privacy_3}")
# print(f"Total number of users for LTE-BLE with privacy_score >= 0.8: {count_users_privacy_4}")
plt.plot(baseline_loc_lte_users, baseline_loc_lte_scores_sorted, label='Baseline - Localization (LTE)', alpha=0.7, linewidth=3, color="#e7298a", marker='p', markevery=marker_interval)

multi_protocol_df = pd.read_csv(f'csv/multi_protocol_scenario1a2.csv')  
multi_protocol_scores = multi_protocol_df['privacy_score'].values
multi_protocol_scores_sorted = np.sort(multi_protocol_scores)
multi_protocol_users = np.arange(1, len(multi_protocol_scores_sorted) + 1)
count_users_privacy_1 = multi_protocol_df[multi_protocol_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = multi_protocol_df[multi_protocol_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = multi_protocol_df[multi_protocol_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = multi_protocol_df[multi_protocol_df['privacy_score'] >= 0.8].shape[0]
print(f"Total number of users for LTE-WIFI-BLE with privacy_score == 1.0: {count_users_privacy_1}")
print(f"Total number of users for LTE-WIFI-BLE with privacy_score >= 0.95: {count_users_privacy_2}")
print(f"Total number of users for LTE-WIFI-BLE with privacy_score >= 0.9: {count_users_privacy_3}")
print(f"Total number of users for LTE-WIFI-BLE with privacy_score >= 0.8: {count_users_privacy_4}")


plt.plot(multi_protocol_users, multi_protocol_scores_sorted, label='Multi-Protocol (LTE, WiFi, Bluetooth)', alpha=0.7, linewidth=3, color="#000000", marker='*', markevery=marker_interval)

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
plt.savefig(f'images/privacy_leakage_q2.pdf', dpi=600, bbox_inches='tight')
plt.show()
