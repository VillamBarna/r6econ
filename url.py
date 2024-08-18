# Open the file with URLs
with open('raw_urls.txt', 'r') as file:
    lines = file.readlines()

# Set to store unique item IDs (set automatically handles duplicates)
unique_item_ids = set()

# Loop through each line in the file
for line in lines:
    # Split the URL at 'itemId=' and take the part after it
    if 'itemId=' in line:
        item_id = line.split('itemId=')[1].strip()
        # Remove any trailing characters (like newlines or spaces)
        item_id = item_id.split('&')[0]  # In case there are additional parameters after itemId
        # Add to the set (duplicate entries will be ignored)
        unique_item_ids.add(item_id)

# Convert set to a sorted list (optional: sort to maintain order)
unique_item_ids = sorted(list(unique_item_ids))

# Write the unique item IDs to a new file
with open('unique_item_ids.txt', 'w') as output_file:
    for item_id in unique_item_ids:
        output_file.write(item_id + '\n')

# Print out the unique IDs (optional)
for item_id in unique_item_ids:
    print(item_id)