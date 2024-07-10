def find_all_possible_chains(dictionary):
    all_chains = []
    visited_keys = set()

    for start_key in dictionary:
        if start_key not in visited_keys:
            chain = []
            current_key = start_key
            
            while current_key is not None:
                visited_keys.add(current_key)
                chain.append(current_key)
                if current_key in dictionary:
                    next_key = dictionary[current_key]
                else:
                    break
                if next_key is None:
                    break
                
                if next_key in visited_keys:
                    # If we encounter a loop, we stop exploring this chain further
                    break
                
                if not next_key:
                    break
                
                current_key = next_key
            
            all_chains.append(chain)
    
    return all_chains

# Example usage:
my_dict = {
    'A': 'B',
    'B': 'L',
    'C': 'D',
    'D': 'E',
    'E': 'P',
    'L': 'G',
    'G': 'H',
    'H': 'I',
    'I': "O"  # End of chain, None indicates no further links
}

all_possible_chains = find_all_possible_chains(my_dict)
print(all_possible_chains)
# for chain in all_possible_chains:
#     print(chain)
