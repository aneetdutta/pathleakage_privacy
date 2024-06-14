echo "Started script"

python3 sumo/sumo_simulation.py
echo "Generated raw user data"

python3 sumo/generate_user_data.py
echo "Generated user data"

python3 sumo/generate_sniffer_data.py
echo "Generated sniffer data"