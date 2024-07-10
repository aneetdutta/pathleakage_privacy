import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from services.general import str_to_bool

DB_NAME = os.getenv("DB_NAME")
# ENABLE_SMART_TRACKING = str_to_bool(os.getenv("ENABLE_SMART_TRACKING"))
# ENABLE_BLUETOOTH = str_to_bool(os.getenv("ENABLE_BLUETOOTH"))
# ENABLE_LTE = str_to_bool(os.getenv("ENABLE_LTE"))
# ENABLE_WIFI = str_to_bool(os.getenv("ENABLE_WIFI"))

plt.figure(figsize=(10, 6))
#E69F00", "#56B4E9", "#009E73", "#0072B2", "#D55E00", "#CC79A7", "#F0E442
# Load the CSV files
# if ENABLE_WIFI:
baseline_wifi_df = pd.read_csv(f'csv/baseline_wifi_scenario1a4.csv')
baseline_wifi_scores = baseline_wifi_df['privacy_score'].values
baseline_wifi_scores_sorted = np.sort(baseline_wifi_scores)
baseline_wifi_users = np.arange(1, len(baseline_wifi_scores_sorted) + 1)
plt.plot(baseline_wifi_users, baseline_wifi_scores_sorted, label='Naive Baseline (Wifi)',alpha=0.7, linewidth=2, color="#2EC4B6")

# if ENABLE_LTE:
baseline_lte_df = pd.read_csv(f'csv/baseline_lte_scenario1a1.csv')
baseline_lte_scores = baseline_lte_df['privacy_score'].values
baseline_lte_scores_sorted = np.sort(baseline_lte_scores)
baseline_lte_users = np.arange(1, len(baseline_lte_scores_sorted) + 1)
plt.plot(baseline_lte_users, baseline_lte_scores_sorted, label='Naive Baseline (LTE)', alpha=0.7, linewidth=2, color="#FF9F1C")

# if ENABLE_BLUETOOTH:
baseline_ble_df = pd.read_csv(f'csv/baseline_ble_scenario1a1.csv')
baseline_ble_scores = baseline_ble_df['privacy_score'].values
baseline_ble_scores_sorted = np.sort(baseline_ble_scores)
baseline_ble_users = np.arange(1, len(baseline_ble_scores_sorted) + 1)
plt.plot(baseline_ble_users, baseline_ble_scores_sorted, label='Naive Baseline (Bluetooth)', alpha=0.7, linewidth=2, color="#94BFBE")


ble_wifi_df = pd.read_csv(f'csv/multi_protocol_scenario1a4.csv')
ble_wifi_scores = ble_wifi_df['privacy_score'].values
ble_wifi_scores_sorted = np.sort(ble_wifi_scores)
ble_wifi_users = np.arange(1, len(ble_wifi_scores_sorted) + 1)
plt.plot(ble_wifi_users, ble_wifi_scores_sorted, label='Multi-Protocol (WiFi, Bluetooth)',alpha=0.7, linewidth=2, color="#61304B")

# if ENABLE_LTE:
wifi_lte_df = pd.read_csv(f'csv/multi_protocol_scenario1a3.csv')
wifi_lte_scores = wifi_lte_df['privacy_score'].values
wifi_lte_scores_sorted = np.sort(wifi_lte_scores)
wifi_lte_users = np.arange(1, len(wifi_lte_scores_sorted) + 1)
plt.plot(wifi_lte_users, wifi_lte_scores_sorted, label='Multi-Protocol (LTE, WiFi)', alpha=0.7, linewidth=2, color="#857C8D")

# if ENABLE_BLUETOOTH:
lte_ble_df = pd.read_csv(f'csv/multi_protocol_scenario1a1.csv')
lte_ble_scores = lte_ble_df['privacy_score'].values
lte_ble_scores_sorted = np.sort(lte_ble_scores)
lte_ble_users = np.arange(1, len(lte_ble_scores_sorted) + 1)
plt.plot(lte_ble_users, lte_ble_scores_sorted, label='Multi-Protocol (LTE, Bluetooth)', alpha=0.7, linewidth=2, color="#5C0029")


multi_protocol_df = pd.read_csv(f'csv/multi_protocol_scenario1a2.csv')  
multi_protocol_scores = multi_protocol_df['privacy_score'].values
multi_protocol_scores_sorted = np.sort(multi_protocol_scores)
multi_protocol_users = np.arange(1, len(multi_protocol_scores_sorted) + 1)
plt.plot(multi_protocol_users, multi_protocol_scores_sorted, label='Multi-Protocol (LTE, WiFi, Bluetooth)', alpha=0.7, linewidth=2, color="#011627")

# plt.plot(multi_protocol_users_old, multi_protocol_scores_sorted_old, label='Multi-Protocol (18797)', alpha=0.7)

xticks = np.linspace(min(multi_protocol_users), max(multi_protocol_users), (math.floor(len(multi_protocol_users)/50)))
xticks = np.round(xticks).astype(int)
plt.xticks(xticks, fontsize=10)
plt.yticks(fontsize=20)
plt.xlabel('Number of Users', fontsize=20)
plt.ylabel('Privacy Leakage', fontsize=20)
# plt.title('Privacy Leakage for different tracking mechanisms',fontsize=14)
plt.legend(loc='lower right', fontsize=13)
plt.grid(True)
plt.savefig(f'images/privacy_leakage_q1.pdf', dpi=600)
# plt.show()
