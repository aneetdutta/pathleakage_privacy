import pandas as pd

# Define the TIMESTEPS value
TIMESTEPS = 18100.0  # This should be your specific TIMESTEPS value

# Define the chain_list
chain_list = ['K27IA5S5PI5E', 'NZOYUHB8SEBB', '8MQIB2ECXNDD']

# Define the DataFrame
data = {
    '_id': ['K27IA5S5PI5E', '8MQIB2ECXNDD', 'NZOYUHB8SEBB'],
    'start_timestep': [18022.25, 18072.25, 18089.75],
    'last_timestep': [18089.5, 18100.0, 18100.0],
    'duration': [67.25, 27.75, 10.25],
    'user_id': ['pedestrian_1-3_5363', 'pedestrian_2-1_4638', 'pedestrian_1-3_5363'],
    'ideal_duration': [77.75, 27.75, 77.75],
    'protocol': ['wifi', 'wifi', 'wifi']
}

df = pd.DataFrame(data)

# Get the count of elements in chain_list with last_timestep equal to TIMESTEPS
count_timesteps = sum(df[df['_id'].isin(chain_list)]['last_timestep'] == TIMESTEPS)

# Remove elements from the end until only one element with last_timestep equal to TIMESTEPS remains
for id in reversed(chain_list):
    if count_timesteps > 1 and df[df['_id'] == id]['last_timestep'].values[0] == TIMESTEPS:
        chain_list.remove(id)
        count_timesteps -= 1

# Print the updated chain_list
print("Updated chain_list:", chain_list)
