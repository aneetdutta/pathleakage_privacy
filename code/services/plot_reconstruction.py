import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

DB_NAME = os.getenv("DB_NAME")

# Load the CSV files
baseline_wifi_df = pd.read_csv(f'csv/baseline_wifi_{DB_NAME}.csv')
baseline_lte_df = pd.read_csv(f'csv/baseline_lte_{DB_NAME}.csv')
# baseline_smart_wifi_df = pd.read_csv(f'csv/baseline_smart_wifi_{DB_NAME}.csv')
# baseline_smart_lte_df = pd.read_csv(f'csv/baseline_smart_lte_{DB_NAME}.csv')
multi_protocol_df = pd.read_csv(f'csv/multi_protocol_{DB_NAME}.csv')
multi_protocol_old_df = pd.read_csv('csv/multi_protocol_project_18797.csv')

# Extract the privacy scores
baseline_wifi_scores = baseline_wifi_df['privacy_score'].values
baseline_lte_scores = baseline_lte_df['privacy_score'].values
# baseline_smart_wifi_scores = baseline_smart_wifi_df['privacy_score'].values
# baseline_smart_lte_scores = baseline_smart_lte_df['privacy_score'].values
multi_protocol_scores = multi_protocol_df['privacy_score'].values
multi_protocol_scores_old = multi_protocol_old_df['privacy_score'].values

# Sort the scores for consistent comparison
baseline_wifi_scores_sorted = np.sort(baseline_wifi_scores)
baseline_lte_scores_sorted = np.sort(baseline_lte_scores)
# baseline_smart_wifi_scores_sorted = np.sort(baseline_smart_wifi_scores)
# baseline_smart_lte_scores_sorted = np.sort(baseline_smart_lte_scores)
multi_protocol_scores_sorted = np.sort(multi_protocol_scores)
multi_protocol_scores_sorted_old = np.sort(multi_protocol_scores_old)


# Compute the cumulative number of users
baseline_wifi_users = np.arange(1, len(baseline_wifi_scores_sorted) + 1)
baseline_lte_users = np.arange(1, len(baseline_lte_scores_sorted) + 1)
# baseline_smart_wifi_users = np.arange(1, len(baseline_smart_wifi_scores_sorted) + 1)
# baseline_smart_lte_users = np.arange(1, len(baseline_smart_lte_scores_sorted) + 1)
multi_protocol_users = np.arange(1, len(multi_protocol_scores_sorted) + 1)
multi_protocol_users_old = np.arange(1, len(multi_protocol_scores_sorted_old) + 1)


# Plot the privacy scores
plt.figure(figsize=(10, 6))
plt.plot(baseline_wifi_users, baseline_wifi_scores_sorted, label='Naive Baseline (Wifi)',alpha=0.7)
plt.plot(baseline_lte_users, baseline_lte_scores_sorted, label='Naive Baseline (LTE)', alpha=0.7)
# plt.plot(baseline_smart_wifi_users, baseline_smart_wifi_scores_sorted, label='Baseline+Localization(Wifi)', alpha=0.7)
# plt.plot(baseline_smart_lte_users, baseline_smart_lte_scores_sorted, label='Baseline+Localization(LTE)', alpha=0.7)
plt.plot(multi_protocol_users, multi_protocol_scores_sorted, label='Multi-Protocol', alpha=0.7)
plt.plot(multi_protocol_users_old, multi_protocol_scores_sorted_old, label='Multi-Protocol (18797)', alpha=0.7)

plt.xticks(np.arange(min(multi_protocol_users), max(multi_protocol_users)+1, math.floor(len(multi_protocol_users)/10)), fontsize=10)
plt.yticks(fontsize=14)
plt.xlabel('Number of Users', fontsize=16)
plt.ylabel('Privacy Leakage', fontsize=14)
plt.title('Privacy Leakage for different tracking mechanisms',fontsize=14)
plt.legend(loc='lower right', fontsize=9)
plt.grid(True)
plt.savefig(f'images/privacy_leakage_{DB_NAME}.pdf', dpi=600)
# plt.show()
