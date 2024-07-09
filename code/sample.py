import csv

# Input and output file paths
input_file = 'data/sniffed_data_scenario1a4.csv'
output_file = 'data/sniffed_data_scenario1a4_f.csv'

# Open input and output files
with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write headers to output file
    writer.writeheader()
    
    # Iterate through rows in input file
    for row in reader:
        # Check if protocol is not 'wifi', then write the row
        if row['protocol'] != 'LTE':
            writer.writerow(row)

print("Rows with protocol=wifi removed successfully.")
