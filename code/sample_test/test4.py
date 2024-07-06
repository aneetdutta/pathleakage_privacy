def combine_and_exclude_all(dicts, result_dict=None):
    # Fetch all unique keys from the provided dictionaries
    keys = {key for d in dicts for key in d.keys()}
    
    # Initialize a dictionary to hold combined sets for each key
    combined_dict = {key: set() for key in keys}
    
    # Combine values for each key from all dictionaries
    for d in dicts:
        for key in keys:
            values = d.get(key, [])
            combined_dict[key].update(values)
    
    # Initialize result_dict if not provided
    if result_dict is None:
        result_dict = {}
    else:
        # Ensure existing result_dict values are sets
        for key in result_dict:
            result_dict[key] = set(result_dict[key])
    
    # Create the final dictionary with each element as key and the set without that element as value
    for key, combined_set in combined_dict.items():
        for element in combined_set:
            if element not in result_dict:
                result_dict[element] = combined_set - {element}
            else:
                result_dict[element].update(combined_set - {element})
    
    # Convert sets back to lists for the final result
    return {key: list(value) for key, value in result_dict.items()}
# # Example usage:
# dicts = [
#     {'a': [1, 2], 'b': [3, 4]},
#     {'a': [2, 3], 'b': [4, 5]},
# ]
# keys = ['a', 'b']

# result = combine_and_exclude_all(dicts, keys)
# print(result)


# Example usage
dicts = [
    {'LTE': [1, 2, 3], 'WIFI': [6, 7], 'BLUETOOTH': [13, 14]},
    {'LTE': [3, 4], 'WIFI': [8, 9], 'BLUETOOTH': [15, 16]},
    {'LTE': [5], 'WIFI': [10, 11, 12], 'BLUETOOTH': [20, 21]}
]

# keys = ['LTE', 'WIFI', 'BLUETOOTH']

# Initial result_dict (can be empty or pre-filled)
initial_result_dict = {
    1: [3, 4, 5]
}

result_dict = combine_and_exclude_all(dicts, result_dict=initial_result_dict)
print("Result Dict:", result_dict)
