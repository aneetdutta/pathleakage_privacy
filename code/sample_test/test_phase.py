T0 = [
    {"LTE": ["L1"], "WiFi": ["W1"]},
    {"LTE": ["L1`"], "WiFi": ["W1"]},
]

T1 = [
    {"LTE": ["L1`"], "WiFi": ["W1"]},
    {"LTE": ["L2"], "WiFi": ["W2"]},
]

def find_new_mappings(T0, T1):
    new_mappings = {"LTE": {}, "WiFi": {}}
    
    # Function to extract all values for a given protocol
    def extract_values(protocol, T):
        return {item for d in T for item in d.get(protocol, [])}
    
    # Extract values
    T0_LTE_values = extract_values("LTE", T0)
    T1_LTE_values = extract_values("LTE", T1)
    
    T0_WiFi_values = extract_values("WiFi", T0)
    T1_WiFi_values = extract_values("WiFi", T1)
    
    # Find new values
    new_LTE_values = T1_LTE_values - T0_LTE_values
    new_WiFi_values = T1_WiFi_values - T0_WiFi_values
    
    # Create mappings for LTE
    for new_value in new_LTE_values:
        for item in T1:
            if new_value in item.get("LTE", []):
                for old_value in item.get("LTE", []):
                    if old_value in T0_LTE_values:
                        new_mappings["LTE"][old_value] = new_value
    
    # Create mappings for WiFi
    for new_value in new_WiFi_values:
        for item in T1:
            if new_value in item.get("WiFi", []):
                for old_value in item.get("WiFi", []):
                    if old_value in T0_WiFi_values:
                        new_mappings["WiFi"][old_value] = new_value
    
    return new_mappings

# Find and print the new mappings
new_mappings = find_new_mappings(T0, T1)
print(new_mappings)
