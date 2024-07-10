import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Define marker interval
marker_interval = 50

plt.figure(figsize=(10, 6))


# full_multilateration_df = pd.read_csv(f'csv/multi_protocol_scenario5b2.csv')
# full_multilateration_scores = full_multilateration_df['privacy_score'].values
# full_multilateration_scores_sorted = np.sort(full_multilateration_scores)
# full_multilateration_users = np.arange(1, len(full_multilateration_scores_sorted) + 1)
# count_users_privacy_1 = full_multilateration_df[full_multilateration_df['privacy_score'] == 1.0].shape[0]
# count_users_privacy_2 = full_multilateration_df[full_multilateration_df['privacy_score'] >= 0.95].shape[0]
# count_users_privacy_3 = full_multilateration_df[full_multilateration_df['privacy_score'] >= 0.9].shape[0]
# count_users_privacy_4 = full_multilateration_df[full_multilateration_df['privacy_score'] >= 0.8].shape[0]
# # print(f"Total number of users for BLE-WIFI with privacy_score == 1.0: {count_users_privacy_1}")
# # print(f"Total number of users for BLE-WIFI with privacy_score >= 0.95: {count_users_privacy_2}")
# # print(f"Total number of users for BLE-WIFI with privacy_score >= 0.9: {count_users_privacy_3}")
# # print(f"Total number of users for BLE-WIFI with privacy_score >= 0.8: {count_users_privacy_4}")
# plt.plot(full_multilateration_users, full_multilateration_scores_sorted, label='Full Coverage with Multilateration', alpha=0.7, linewidth=3, color="#bf5b17", marker='<', markevery=marker_interval)

partial_nomultilateration_df = pd.read_csv(f'csv/multi_protocol_scenario5c2.csv')
partial_nomultilateration_scores = partial_nomultilateration_df['privacy_score'].values
partial_nomultilateration_scores_sorted = np.sort(partial_nomultilateration_scores)
partial_nomultilateration_users = np.arange(1, len(partial_nomultilateration_scores_sorted) + 1)
count_users_privacy_1 = partial_nomultilateration_df[partial_nomultilateration_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = partial_nomultilateration_df[partial_nomultilateration_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = partial_nomultilateration_df[partial_nomultilateration_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = partial_nomultilateration_df[partial_nomultilateration_df['privacy_score'] >= 0.8].shape[0]
# print(f"Total number of users for LTE-WIFI with privacy_score == 1.0: {count_users_privacy_1}")
# print(f"Total number of users for LTE-WIFI with privacy_score >= 0.95: {count_users_privacy_2}")
# print(f"Total number of users for LTE-WIFI with privacy_score >= 0.9: {count_users_privacy_3}")
# print(f"Total number of users for LTE-WIFI with privacy_score >= 0.8: {count_users_privacy_4}")
plt.plot(partial_nomultilateration_users, partial_nomultilateration_scores_sorted, label='Partial Coverage with No Multilateration', alpha=0.7, linewidth=3, color="#a6d854", marker='>', markevery=marker_interval)

partial_multilateration_df = pd.read_csv(f'csv/multi_protocol_scenario5d2.csv')
partial_multilateration_scores = partial_multilateration_df['privacy_score'].values
partial_multilateration_scores_sorted = np.sort(partial_multilateration_scores)
partial_multilateration_users = np.arange(1, len(partial_multilateration_scores_sorted) + 1)
count_users_privacy_1 = partial_multilateration_df[partial_multilateration_df['privacy_score'] == 1.0].shape[0]
count_users_privacy_2 = partial_multilateration_df[partial_multilateration_df['privacy_score'] >= 0.95].shape[0]
count_users_privacy_3 = partial_multilateration_df[partial_multilateration_df['privacy_score'] >= 0.9].shape[0]
count_users_privacy_4 = partial_multilateration_df[partial_multilateration_df['privacy_score'] >= 0.8].shape[0]
# print(f"Total number of users for LTE-BLE with privacy_score == 1.0: {count_users_privacy_1}")
# print(f"Total number of users for LTE-BLE with privacy_score >= 0.95: {count_users_privacy_2}")
# print(f"Total number of users for LTE-BLE with privacy_score >= 0.9: {count_users_privacy_3}")
# print(f"Total number of users for LTE-BLE with privacy_score >= 0.8: {count_users_privacy_4}")
plt.plot(partial_multilateration_users, partial_multilateration_scores_sorted, label='Partial Coverage with Multilateration', alpha=0.7, linewidth=3, color="#e7298a", marker='p', markevery=marker_interval)

# plt.margins(0)
# plt.autoscale(enable=True, axis='both', tight=True)

xticks = np.linspace(min(partial_multilateration_users), max(partial_multilateration_users), math.floor(len(partial_multilateration_users)/5))
xticks = np.round(xticks).astype(int)
plt.xticks(xticks, fontsize=22)
plt.yticks(fontsize=22)
plt.xlabel('Number of Users', fontsize=22)
plt.ylabel('Privacy Leakage', fontsize=22)
plt.legend(loc='lower right', fontsize=15)
plt.grid(True)
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.savefig(f'images/privacy_leakage_q4b.pdf', dpi=600, bbox_inches='tight')
plt.show()
