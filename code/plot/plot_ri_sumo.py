import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from services.general import str_to_bool
# Load the CSV file

multi_protocol_3a7df = pd.read_csv(f'csv/multi_protocol_scenario3a7.csv')
multi_protocol_3a7scores = multi_protocol_3a7df['privacy_score'].values
multi_protocol_3a7scores_sorted = np.sort(multi_protocol_3a7scores)
multi_protocol_3a7users = np.arange(1, len(multi_protocol_3a7scores_sorted) + 1)

multi_protocol_3a6df = pd.read_csv(f'csv/multi_protocol_scenario3a6.csv')
multi_protocol_3a6scores = multi_protocol_3a6df['privacy_score'].values
multi_protocol_3a6scores_sorted = np.sort(multi_protocol_3a6scores)
multi_protocol_3a6users = np.arange(1, len(multi_protocol_3a6scores_sorted) + 1)

multi_protocol_3a5df = pd.read_csv(f'csv/multi_protocol_scenario3a5.csv')
multi_protocol_3a5scores = multi_protocol_3a5df['privacy_score'].values
multi_protocol_3a5scores_sorted = np.sort(multi_protocol_3a5scores)
multi_protocol_3a5users = np.arange(1, len(multi_protocol_3a5scores_sorted) + 1)

multi_protocol_3a4df = pd.read_csv(f'csv/multi_protocol_scenario3a4.csv')
multi_protocol_3a4scores = multi_protocol_3a4df['privacy_score'].values
multi_protocol_3a4scores_sorted = np.sort(multi_protocol_3a4scores)
multi_protocol_3a4users = np.arange(1, len(multi_protocol_3a4scores_sorted) + 1)

multi_protocol_3a3df = pd.read_csv(f'csv/multi_protocol_scenario3a3.csv')
multi_protocol_3a3scores = multi_protocol_3a3df['privacy_score'].values
multi_protocol_3a3scores_sorted = np.sort(multi_protocol_3a3scores)
multi_protocol_3a3users = np.arange(1, len(multi_protocol_3a3scores_sorted) + 1)

# Plot the privacy scores
plt.figure(figsize=(10, 6))
plt.plot(multi_protocol_3a4users, multi_protocol_3a4scores_sorted, label='Multi-Protocol RI WIFI - 900-1800', alpha=0.7)
plt.plot(multi_protocol_3a7users, multi_protocol_3a7scores_sorted, label='Multi-Protocol RI WIFI - 600-900', alpha=0.7)
plt.plot(multi_protocol_3a6users, multi_protocol_3a6scores_sorted, label='Multi-Protocol RI WIFI - 300-600', alpha=0.7)
plt.plot(multi_protocol_3a5users, multi_protocol_3a5scores_sorted, label='Multi-Protocol RI WIFI - 120-300', alpha=0.7)
plt.plot(multi_protocol_3a3users, multi_protocol_3a3scores_sorted, label='Multi-Protocol RI WIFI - 0-60', alpha=0.7)

# plt.plot(multi_protocol_3a7users_old, multi_protocol_3a7scores_sorted_old, label='Multi-Protocol (18797)', alpha=0.7)

plt.xticks(np.arange(min(multi_protocol_3a7users), max(multi_protocol_3a7users)+1, math.floor(len(multi_protocol_3a7users)/10)), fontsize=10)
plt.yticks(fontsize=14)
plt.xlabel('Number of Users', fontsize=16)
plt.ylabel('Privacy Leakage', fontsize=14)
plt.title('Privacy Leakage (LTE - 900-1800 RI, LTE TI - 0-60, WIFI TI - 0-120, TIMESTEPS - 7200)',fontsize=14)
plt.legend(loc='lower right', fontsize=9)
plt.grid(True)
plt.savefig(f'images/privacy_leakage_RI.pdf', dpi=600)
# plt.show()
