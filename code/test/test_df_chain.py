import pandas as pd

# Sample DataFrame
data = {
    'id': ['ABC', 'DEF'],
    'mapping': [['DEF'], ['FGH']],
    'start_timestep': [10, 20],
    'end_timestep': [20, 25]
}

df = pd.DataFrame(data)

def build_chain(current_id, df, visited):
    chain = []
    start_timestep = df.loc[df['id'] == current_id, 'start_timestep'].values[0]
    end_timestep = df.loc[df['id'] == current_id, 'end_timestep'].values[0]
    
    while current_id and current_id not in visited:
        visited.add(current_id)
        row = df[df['id'] == current_id]
        if not row.empty:
            mapping = row.iloc[0]['mapping']
            if mapping:
                next_id = mapping[0]
                if next_id in visited:
                    break
                chain.append(next_id)
                current_id = next_id
                end_timestep = df.loc[df['id'] == current_id, 'end_timestep'].values[0]
            else:
                break
        else:
            break
    
    return pd.Series([current_id, chain, start_timestep, end_timestep])

def create_chain_dataframe(df):
    all_chains = []
    visited = set()
    
    for _, row in df.iterrows():
        if row['id'] not in visited:
            chain_info = build_chain(row['id'], df, visited)
            all_chains.append(chain_info)
    
    chain_df = pd.DataFrame(all_chains, columns=['id', 'chain', 'start_timestep', 'end_timestep'])
    
    # Extract ids that are part of any chain
    ids_in_chains = set()
    for chain in chain_df['chain']:
        ids_in_chains.update(chain)

    # Filter out rows where id is part of any chain
    chain_df = chain_df[~chain_df['id'].isin(ids_in_chains)]
    
    return chain_df

chain_df = create_chain_dataframe(df)
print(chain_df)
