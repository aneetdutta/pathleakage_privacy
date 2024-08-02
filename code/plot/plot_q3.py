import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Define marker interval
marker_interval = 50

plt.figure(figsize=(10, 6))


ti_30_df = pd.read_csv(f'csv/multi_protocol_scenario7a1.csv')  
ti_30_scores = ti_30_df['privacy_score'].values
ti_30_scores_sorted = np.sort(ti_30_scores)
ti_30_users = np.arange(1, len(ti_30_scores_sorted) + 1)
count_users_privacy_1 = ti_30_df[ti_30_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = ti_30_df[ti_30_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = ti_30_df[ti_30_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = ti_30_df[ti_30_df['privacy_score'] >= 0.8].shape[0]

plt.plot(ti_30_users, ti_30_scores_sorted, label='LTE, BLE - Transmission Interval:(0-30)', alpha=0.7, linewidth=3, color="#000000", marker='o', markevery=marker_interval)


ti_60_df = pd.read_csv(f'csv/multi_protocol_scenario1a1.csv')
ti_60_scores = ti_60_df['privacy_score'].values
ti_60_scores_sorted = np.sort(ti_60_scores)
ti_60_users = np.arange(1, len(ti_60_scores_sorted) + 1)
count_users_privacy_1 = ti_60_df[ti_60_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = ti_60_df[ti_60_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = ti_60_df[ti_60_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = ti_60_df[ti_60_df['privacy_score'] >= 0.8].shape[0]
print(f"Total number of users for LTE-BLE with privacy_score == 1.0: {count_users_privacy_1}")
print(f"Total number of users for LTE-BLE with privacy_score >= 0.95: {count_users_privacy_2}")
print(f"Total number of users for LTE-BLE with privacy_score >= 0.9: {count_users_privacy_3}")
print(f"Total number of users for LTE-BLE with privacy_score >= 0.8: {count_users_privacy_4}")
plt.plot(ti_60_users, ti_60_scores_sorted, label='LTE, BLE - Transmission Interval:(0-60)', alpha=0.7, linewidth=3, color="#bf5b17", marker='p', markevery=marker_interval)



ti_120_df = pd.read_csv(f'csv/multi_protocol_scenario7a2.csv')
ti_120_scores = ti_120_df['privacy_score'].values
ti_120_scores_sorted = np.sort(ti_120_scores)
ti_120_users = np.arange(1, len(ti_120_scores_sorted) + 1)
count_users_privacy_1 = ti_120_df[ti_120_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = ti_120_df[ti_120_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = ti_120_df[ti_120_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = ti_120_df[ti_120_df['privacy_score'] >= 0.8].shape[0]
print(f"Total number of users for LTE-BLE with privacy_score == 1.0: {count_users_privacy_1}")
print(f"Total number of users for LTE-BLE with privacy_score >= 0.95: {count_users_privacy_2}")
print(f"Total number of users for LTE-BLE with privacy_score >= 0.9: {count_users_privacy_3}")
print(f"Total number of users for LTE-BLE with privacy_score >= 0.8: {count_users_privacy_4}")
plt.plot(ti_120_users, ti_120_scores_sorted, label='LTE, BLE - Transmission Interval:(60-120)', alpha=0.7, linewidth=3, color="#e7298a", marker='<', markevery=marker_interval)


# plt.margins(0)
# plt.autoscale(enable=True, axis='both', tight=True)

xticks = np.linspace(min(ti_30_users), max(ti_30_users), math.floor(len(ti_30_users)/50))
xticks = np.round(xticks).astype(int)
plt.xticks(xticks, fontsize=22)
plt.yticks(fontsize=22)
plt.xlabel('Number of Users', fontsize=22)
plt.ylabel('Privacy Leakage', fontsize=22)
plt.legend(loc='lower right', fontsize=15)
plt.grid(True)
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.savefig(f'images/privacy_leakage_q3.pdf', dpi=600, bbox_inches='tight')
plt.show()
