def remove_subsets(chains):
    chains_copy = sorted(chains, key=len, reverse=True)
    subsets_removed = []
    for chain in chains_copy:
        if not any(chain.issubset(other) for other in subsets_removed):
            subsets_removed.append(chain)
    return subsets_removed

def build_all_chains(current_key, current_chain, visited, data, all_chains):
    if current_key in visited:
        return

    visited.add(current_key)
    current_chain.add(current_key)

    if current_key in data:
        build_all_chains(data[current_key], current_chain.copy(), visited.copy(), data, all_chains)
    else:
        all_chains.append(current_chain.copy())

def find_all_chains(data):
    all_chains = []

    for key in data:
        build_all_chains(key, set(), set(), data, all_chains)
    
    return remove_subsets(all_chains)

# Example dictionary
data = {
    "L1": "L1`",
    "L1`": "L1``",
    "L2": "L1``",
    "L3": "L4",
    "L1``": "L1```"
}

chains = find_all_chains(data)
print(chains)
