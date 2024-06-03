import pandas as pd

# Create the sample DataFrame
data = {
    '_id': ['7PKDJ98GDK7L', 'U1B2PC59J23O', 'RGF8AZ43F2EO', 'UXI5RYB8U29B', 'WRXGG14INFKB'],
    'start_timestep': [18001.25, 18001.25, 18022.50, 18037.00, 18049.50],
    'last_timestep': [18015.75, 18022.25, 18036.75, 18049.25, 18061.75]
}

df = pd.DataFrame(data)

# Find the minimum value of start_timestep
min_start_timestep = df['start_timestep'].min()

# Filter the DataFrame to include only rows with the minimum start_timestep
result = df[df['start_timestep'] == min_start_timestep]

print(len(result))
