echo "Started script"
mongosh --eval "db.getSiblingDB('code').dropDatabase()"
echo "Dropped 'code' database"
python3 sumo/sumo_simulation.py
echo "Generated raw user data"

python3 sumo/generate_user_data.py
echo "Generated user data"

python3 sumo/generate_sniffer_data.py
echo "Generated sniffer data"

mongoimport --host localhost --port 27017 --db code --collection sniffed_data --type csv --file data/sniffed_data.csv --headerline
mongoimport --host localhost --port 27017 --db code --collection user_data --type csv --file data/user_data.csv --headerline

python3 group/aggregation.py

python3 group/aggregate_sniffer_timesteps.py

python3 group/group_parallel.py

python3 tracking/tracking.py

echo "Performing smart tracking algorithm"
python3 tracking/tracking_single.py
echo "Performed Tracking operation"

python3 sanity/sanity.py
echo "Performed Sanity check"

python3 reconstruction/reconstruction_user_data.py
echo "Performed Baseline Reconstruction"

python3 reconstruction/reconstruction_baseline.py
echo "Performed Baseline Reconstruction"

# python3 reconstruction_baseline_random.py
# echo "Performed Baseline Reconstruction"

python3 reconstruction/reconstruction_multi.py
echo "Performed Multi Reconstruction"

python3 services/plot_reconstruction.py
echo "Performed Multi Reconstruction"