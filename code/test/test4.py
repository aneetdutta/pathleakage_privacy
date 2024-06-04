import concurrent.futures

def combine_values(dicts, keys):
    # Initialize a dictionary to hold combined sets for each key
    combined_dict = {key: set() for key in keys}
    
    # Combine values for each key from all dictionaries
    for d in dicts:
        for key in keys:
            combined_dict[key].update(d.get(key, []))
    
    return combined_dict

def create_exclusion_set(combined_set, element):
    return {item for item in combined_set if item != element}

def combine_and_exclude_all(dicts, keys):
    combined_dict = combine_values(dicts, keys)
    
    result_dict = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_element = {}
        
        for key in keys:
            combined_set = combined_dict[key]
            for element in combined_set:
                future = executor.submit(create_exclusion_set, combined_set, element)
                future_to_element[future] = element
        
        for future in concurrent.futures.as_completed(future_to_element):
            element = future_to_element[future]
            result_dict[element] = future.result()
    
    return result_dict

# Example usage
dicts = [
    {'LTE': [1, 2, 3], 'WIFI': [6, 7], 'BLUETOOTH': [13, 14]},
    {'LTE': [3, 4], 'WIFI': [8, 9], 'BLUETOOTH': [15, 16]},
    {'LTE': [5], 'WIFI': [10, 11, 12], 'BLUETOOTH': [20, 21]}
]

keys = ['LTE', 'WIFI', 'BLUETOOTH']

result_dict = combine_and_exclude_all(dicts, keys)
print("Result Dict:", result_dict)
