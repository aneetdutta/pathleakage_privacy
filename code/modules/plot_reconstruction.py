import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from modules.general import str_to_bool

SCENARIO_NAME = os.getenv("SCENARIO_NAME")
# ENABLE_SMART_TRACKING = str_to_bool(os.getenv("ENABLE_SMART_TRACKING"))
ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH"))
ENABLE_LTE = str_to_bool(os.getenv("ENABLE_LTE"))
ENABLE_WIFI = str_to_bool(os.getenv("ENABLE_WIFI"))

plt.figure(figsize=(10, 6))
#E69F00", "#56B4E9", "#009E73", "#0072B2", "#D55E00", "#CC79A7", "#F0E442
# Load the CSV files
if ENABLE_WIFI:
    baseline_wifi_df = pd.read_csv(f'output/data/{SCENARIO_NAME}/baseline_wifi_{SCENARIO_NAME}.csv')
    baseline_wifi_scores = baseline_wifi_df['privacy_score'].values
    baseline_wifi_scores_sorted = np.sort(baseline_wifi_scores)
    baseline_wifi_users = np.arange(1, len(baseline_wifi_scores_sorted) + 1)
    plt.plot(baseline_wifi_users, baseline_wifi_scores_sorted, label='Naive Baseline (Wifi)',alpha=0.7, linewidth=2, color="#E69F00")

if ENABLE_LTE:
    baseline_lte_df = pd.read_csv(f'output/data/{SCENARIO_NAME}/baseline_lte_{SCENARIO_NAME}.csv')
    baseline_lte_scores = baseline_lte_df['privacy_score'].values
    baseline_lte_scores_sorted = np.sort(baseline_lte_scores)
    baseline_lte_users = np.arange(1, len(baseline_lte_scores_sorted) + 1)
    plt.plot(baseline_lte_users, baseline_lte_scores_sorted, label='Naive Baseline (LTE)', alpha=0.7, linewidth=2, color="#56B4E9")

if ENABLE_BLUETOOTH:
    baseline_ble_df = pd.read_csv(f'output/data/{SCENARIO_NAME}/baseline_ble_{SCENARIO_NAME}.csv')
    baseline_ble_scores = baseline_ble_df['privacy_score'].values
    baseline_ble_scores_sorted = np.sort(baseline_ble_scores)
    baseline_ble_users = np.arange(1, len(baseline_ble_scores_sorted) + 1)
    plt.plot(baseline_ble_users, baseline_ble_scores_sorted, label='Naive Baseline (Bluetooth)', alpha=0.7, linewidth=2, color="#009E73")

if ENABLE_WIFI:
    baseline_smart_wifi_df = pd.read_csv(f'output/data/{SCENARIO_NAME}/single_wifi_{SCENARIO_NAME}.csv')
    baseline_smart_wifi_scores = baseline_smart_wifi_df['privacy_score'].values
    baseline_smart_wifi_scores_sorted = np.sort(baseline_smart_wifi_scores)
    baseline_smart_wifi_users = np.arange(1, len(baseline_smart_wifi_scores_sorted) + 1)
    plt.plot(baseline_smart_wifi_users, baseline_smart_wifi_scores_sorted, label='Single Protocol (Wifi)', alpha=0.7, linewidth=2, color="#0072B2")
if ENABLE_LTE:
    baseline_smart_lte_df = pd.read_csv(f'output/data/{SCENARIO_NAME}/single_lte_{SCENARIO_NAME}.csv')
    baseline_smart_lte_scores = baseline_smart_lte_df['privacy_score'].values
    baseline_smart_lte_scores_sorted = np.sort(baseline_smart_lte_scores)
    baseline_smart_lte_users = np.arange(1, len(baseline_smart_lte_scores_sorted) + 1)
    plt.plot(baseline_smart_lte_users, baseline_smart_lte_scores_sorted, label='Single Protocol (LTE)', alpha=0.7, linewidth=2, color="#D55E00")

if ENABLE_BLUETOOTH:
    baseline_smart_ble_df = pd.read_csv(f'output/data/{SCENARIO_NAME}/single_ble_{SCENARIO_NAME}.csv')
    baseline_smart_ble_scores = baseline_smart_ble_df['privacy_score'].values
    baseline_smart_ble_scores_sorted = np.sort(baseline_smart_ble_scores)
    baseline_smart_ble_users = np.arange(1, len(baseline_smart_ble_scores_sorted) + 1)
    plt.plot(baseline_smart_ble_users, baseline_smart_ble_scores_sorted, label='Single Protocol (Bluetooth)', alpha=0.7, linewidth=2, color="#CC79A7")



multi_protocol_df = pd.read_csv(f'output/data/{SCENARIO_NAME}/multi_protocol_{SCENARIO_NAME}.csv')  
multi_protocol_scores = multi_protocol_df['privacy_score'].values
multi_protocol_scores_sorted = np.sort(multi_protocol_scores)
scores_less_than_one = multi_protocol_scores_sorted[multi_protocol_scores_sorted < 1.0]

# Print the scores and their count
print(f"Scores less than 1.0: {scores_less_than_one}")
print(f"Count of scores less than 1.0: {len(scores_less_than_one)}")

multi_protocol_users = np.arange(1, len(multi_protocol_scores_sorted) + 1)

if ENABLE_WIFI and ENABLE_BLUETOOTH and not ENABLE_LTE:
    multi_label = 'Multi-Protocol (LTE, Bluetooth)'
elif ENABLE_BLUETOOTH and ENABLE_LTE and not ENABLE_WIFI:
    multi_label = 'Multi-Protocol (LTE, Bluetooth)'
elif ENABLE_LTE and ENABLE_WIFI and not ENABLE_BLUETOOTH:
    multi_label = 'Multi-Protocol (LTE, WiFi)'
elif ENABLE_LTE and ENABLE_WIFI and ENABLE_BLUETOOTH:
    multi_label = 'Multi-Protocol (LTE, WiFi, Bluetooth)'
else:
    multi_label = None
plt.plot(multi_protocol_users, multi_protocol_scores_sorted, label=multi_label, alpha=0.7, linewidth=2, color="#000000")

# plt.plot(multi_protocol_users_old, multi_protocol_scores_sorted_old, label='Multi-Protocol (18797)', alpha=0.7)

# plt.xticks(np.linspace(min(multi_protocol_users), max(multi_protocol_users)), fontsize=10)
plt.yticks(np.linspace(0, 1, 10), fontsize=10)

# plt.yticks(fontsize=20)
plt.xlabel('Number of Users', fontsize=20)
plt.ylabel('Privacy Leakage', fontsize=20)
# plt.title('Privacy Leakage for different tracking mechanisms',fontsize=14)
plt.legend(loc='lower right', fontsize=13)
plt.grid(True)
plt.savefig(f'output/images/privacy_leakage_{SCENARIO_NAME}.pdf', dpi=600)
# plt.show()
