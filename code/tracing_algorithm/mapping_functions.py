import os, sys
sys.path.append(os.getcwd())
import numpy as np

SCENARIO_NAME = os.getenv("SCENARIO_NAME")
MAX_MOBILITY_FACTOR = float(os.getenv('MAX_MOBILITY_FACTOR'))
MAX_TRANSMIT_TIME=60

def compute_localization_error(protocols):
    # protocols is a Categorical series
    unique_cats = protocols.cat.categories
    errors = np.zeros(len(unique_cats), dtype=np.int8)
    # Assign errors by category
    for i, cat in enumerate(unique_cats):
        if cat == 'Bluetooth':
            errors[i] = 1
        elif cat == 'WiFi':
            errors[i] = 5
        else:
            errors[i] = 10
    return errors


def check_compatibility_vectorized(subset1, subset2, protocol_errors):
    arr1_x = subset1['sl_x'].values
    arr1_y = subset1['sl_y'].values
    arr1_t = subset1['timestep'].values
    arr1_d = subset1['dist_S_U'].values
    arr1_p = subset1['protocol'].cat.codes.values
    arr1_sniffer = subset1['sniffer_id'].values

    # --- 2) Extract arrays from subset2
    arr2_x = subset2['sl_x'].values
    arr2_y = subset2['sl_y'].values
    arr2_t = subset2['timestep'].values
    arr2_d = subset2['dist_S_U'].values
    arr2_p = subset2['protocol'].cat.codes.values
    arr2_sniffer = subset2['sniffer_id'].values
    
    r1 = arr1_d + protocol_errors[arr1_p]
    r2 = arr2_d + protocol_errors[arr2_p]

    dx = arr1_x[:, None] - arr2_x[None, :]
    dy = arr1_y[:, None] - arr2_y[None, :]
    d_xy = np.sqrt(dx**2 + dy**2)

    R = r1[:, None] + r2[None, :]
    min_distance = d_xy - R
    min_distance[min_distance < 0] = 0
    
    delta_t = np.abs(arr1_t[:, None] - arr2_t[None, :])
    compatible_matrix = (min_distance <= (delta_t * MAX_MOBILITY_FACTOR))

    # --- 8) Return True only if *all* pairs pass
    return compatible_matrix.all() 

# Function to check interval overlap
def intervals_overlap_intra(max1, min2):
    if max1 < min2:
        if (min2 - max1) <= MAX_TRANSMIT_TIME:
            return True
        # ((min2-max1)<=60)
    else:
        return False
    
def intervals_overlap_inter(min1, max1, min2, max2):
    return not (max1+MAX_TRANSMIT_TIME < min2 or max2+MAX_TRANSMIT_TIME < min1)