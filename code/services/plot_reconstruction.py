import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Load the CSV files
baseline_wifi_df = pd.read_csv('csv/baseline_wifi.csv')
baseline_lte_df = pd.read_csv('csv/baseline_lte.csv')
# baseline_random_wifi_df = pd.read_csv('csv/baseline_random_wifi.csv')
# baseline_random_lte_df = pd.read_csv('csv/baseline_random_lte.csv')
multi_protocol_df = pd.read_csv('csv/multi_protocol.csv')
# multi_protocol_old_df = pd.read_csv('csv/multi_protocol_old.csv')

# Extract the privacy scores
baseline_wifi_scores = baseline_wifi_df['privacy_score'].values
baseline_lte_scores = baseline_lte_df['privacy_score'].values
# baseline_random_wifi_scores = baseline_random_wifi_df['privacy_score'].values
# baseline_random_lte_scores = baseline_random_lte_df['privacy_score'].values
multi_protocol_scores = multi_protocol_df['privacy_score'].values
# multi_protocol_scores_old = multi_protocol_old_df['privacy_score'].values

# Sort the scores for consistent comparison
baseline_wifi_scores_sorted = np.sort(baseline_wifi_scores)
baseline_lte_scores_sorted = np.sort(baseline_lte_scores)
# baseline_random_wifi_scores_sorted = np.sort(baseline_random_wifi_scores)
# baseline_random_lte_scores_sorted = np.sort(baseline_random_lte_scores)
multi_protocol_scores_sorted = np.sort(multi_protocol_scores)
# multi_protocol_scores_sorted_old = np.sort(multi_protocol_scores_old)


# Compute the cumulative number of users
baseline_wifi_users = np.arange(1, len(baseline_wifi_scores_sorted) + 1)
baseline_lte_users = np.arange(1, len(baseline_lte_scores_sorted) + 1)
# baseline_random_wifi_users = np.arange(1, len(baseline_random_wifi_scores_sorted) + 1)
# baseline_random_lte_users = np.arange(1, len(baseline_random_lte_scores_sorted) + 1)
multi_protocol_users = np.arange(1, len(multi_protocol_scores_sorted) + 1)
# multi_protocol_users_old = np.arange(1, len(multi_protocol_scores_sorted_old) + 1)


# Plot the privacy scores
plt.figure(figsize=(10, 6))
plt.plot(baseline_wifi_users, baseline_wifi_scores_sorted, label='Naive Baseline (Wifi)',alpha=0.7)
plt.plot(baseline_lte_users, baseline_lte_scores_sorted, label='Naive Baseline (LTE)', alpha=0.7)
# plt.plot(baseline_random_wifi_users, baseline_random_wifi_scores_sorted, label='Baseline+Localization(Wifi)', alpha=0.7)
# plt.plot(baseline_random_lte_users, baseline_random_lte_scores_sorted, label='Baseline+Localization(LTE)', alpha=0.7)
plt.plot(multi_protocol_users, multi_protocol_scores_sorted, label='Multi-Protocol', alpha=0.7)
# plt.plot(multi_protocol_users_old, multi_protocol_scores_sorted_old, label='Multi-Protocol (Old)', alpha=0.7)

plt.xticks(np.arange(min(multi_protocol_users), max(multi_protocol_users)+1, math.floor(len(multi_protocol_users)/16)), fontsize=10)
plt.yticks(fontsize=14)
plt.xlabel('Number of Users', fontsize=16)
plt.ylabel('Privacy Leakage', fontsize=14)
plt.title('Privacy Leakage for different tracking mechanisms',fontsize=14)
plt.legend(loc='lower right', fontsize=9)
plt.grid(True)
plt.savefig('images/privacy_leakage_1.pdf', dpi=600)
# plt.show()
