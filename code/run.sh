mongosh --eval "db.getSiblingDB('code').dropDatabase()"
echo "Dropped 'code' database"

python3 raw_user_data.py
echo "Generated raw user data"

echo "Generating sniffer data"
python3 raw_sniffer_data.py
echo "Generated raw sniffer data"

# python3 sumo_simulation.py
mongoimport --host localhost --port 27017 --db code --collection sniffed_data --type json --file sniffed_data.json --jsonArray
echo "Imported sniffed data into MongoDB"

mongoimport --host localhost --port 27017 --db code --collection user_data --type json --file user_data.json --jsonArray
echo "Imported user data into MongoDB"

python3 aggregation.py
echo "Performed aggregation operations"

python3 group.py
echo "Performed grouping operations"

python3 group_checker.py
echo "Checked group data"

python3 user_id.py
echo "Performed user ID operations"

python3 tracking.py
echo "Performed Tracking operation"

python3 sanity.py
echo "Performed Sanity check"