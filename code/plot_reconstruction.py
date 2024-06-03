import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV files
baseline_df = pd.read_csv('baseline.csv')
multi_protocol_df = pd.read_csv('multi_protocol.csv')

# Extract the privacy scores
baseline_scores = baseline_df['privacy_score'].values
multi_protocol_scores = multi_protocol_df['privacy_score'].values

# Sort the scores for consistent comparison
baseline_scores_sorted = np.sort(baseline_scores)
multi_protocol_scores_sorted = np.sort(multi_protocol_scores)

# Compute the cumulative number of users
baseline_users = np.arange(1, len(baseline_scores_sorted) + 1)
multi_protocol_users = np.arange(1, len(multi_protocol_scores_sorted) + 1)

# Plot the privacy scores
plt.figure(figsize=(10, 6))
plt.plot(baseline_users, baseline_scores_sorted, label='Baseline', marker='o')
plt.plot(multi_protocol_users, multi_protocol_scores_sorted, label='Multi-Protocol', marker='x')
plt.xticks(np.arange(min(multi_protocol_users), max(multi_protocol_users)+1, 3.0), fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Number of Users', fontsize=16)
plt.ylabel('Privacy Leakage', fontsize=14)
plt.title('Privacy Leakage for Baseline and Multi-Protocol',fontsize=14)
plt.legend(loc='lower right', fontsize="18")
plt.grid(True)
plt.savefig('privacy_leakage.pdf', dpi=600)
plt.show()
