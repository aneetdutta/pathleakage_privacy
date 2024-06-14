data = {
    "L1": ["L1`"],
    "L1`": ["L1``", "L1", "L1```"],
    "L1```": ["L1``", "L1````"],
    "L2": [],
    "L3": ["L3`"],
    "L4": ["L4`"],
    "L4`": ["L4``"]
}

def remove_subsets_and_merge(data):
    result = []
    for key, value in data.items():
        chain = [key] + value
        chain_set = set(chain)
        # Check if the chain is a subset of any existing chain or if it intersects with any existing chain
        subset = next((existing for existing in result if chain_set.issubset(set(existing))), None)
        intersection = next((existing for existing in result if chain_set.intersection(set(existing))), None)
        if subset:
            continue  # Skip if the chain is a subset of an existing chain
        elif intersection:
            # Merge the chains and remove the old ones
            result = [list(set(existing + chain)) if existing == intersection else existing for existing in result]
        else:
            result.append(chain)
    return result

converted_data = remove_subsets_and_merge(data)


def get_list_containing_value(merged_data, value):
    for chain in merged_data:
        if value in chain:
            return chain
    return None

value = "L4"
result = get_list_containing_value(converted_data, value)
print(result)


# print(converted_data)
