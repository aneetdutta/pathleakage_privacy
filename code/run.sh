mongosh --eval "db.getSiblingDB('code').dropDatabase()"
python3 sumo_simulation.py
mongoimport --host localhost --port 27017 --db code --collection sniffed_data --type json --file sniffed_data.json --jsonArray
mongoimport --host localhost --port 27017 --db code --collection user_data --type json --file user_data.json --jsonArray
python3 aggregation.py
python3 group.py
python3 group_checker.py
python3 user_id.py
python3 tracking.py
python3 sanity.py