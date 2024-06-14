def remove_subsets(chains):
    chains_copy = sorted(chains, key=len, reverse=True)
    subsets_removed = []
    for chain in chains_copy:
        if not any(set(chain).issubset(set(other)) for other in subsets_removed):
            subsets_removed.append(chain)
    return subsets_removed

def build_chain_for_key(current_key, current_chain, visited, data, all_chains):
    if current_key in visited:
        return

    visited.add(current_key)
    current_chain.append(current_key)

    next_key = data.get(current_key)
    if next_key:
        build_chain_for_key(next_key, current_chain.copy(), visited.copy(), data, all_chains)
    else:
        all_chains.append(current_chain.copy())

def find_chain_for_key(data, start_key):
    all_chains = []
    build_chain_for_key(start_key, [], set(), data, all_chains)
    return remove_subsets(all_chains)

# Example dictionary
data = {
    "V2Z8JBJ33V6Y": "PJ8E8O8VF5C9",
    "L1": "L1`",
    "L1`": "L1``",
    "L2": "L1``",
    "L3": "L3`",
    "8A5AHRKOPP1N": "8JBDCGM4CL9N",
    "ILDGVFY62LCN": "7C2053GOQIZY",
    "6R83Q6PMQU1I": "A9I20M1JV92O",
    "KB6PROCLE8O6": "YM8VWWS6DLB2",
    "761FG1XCK4XC": "F5ZBZVSQ7JCS",
    "NUVFZPICOZRR": "ED1U46SM6S08",
    "0G8S9S7HZ99H": "Z0Y0SA0HZG0A",
    "B4ZV9BEPECV2": "7A3GGTOC8JT3",
    "asd": "V2Z8JBJ33V6Y",
    "OMXR9449EBRA": "DWO5ZK4I8DC7",
}

# Find chains for a specific key
key_to_find = "V2Z8JBJ33V6Y"
chains = find_chain_for_key(data, key_to_find)
print(chains)
