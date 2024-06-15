# Define the Python interpreter
PYTHON = python3

# Define the default target
all: run_scripts

gts: group tracking sanity

gtsr: group tracking sanity reconstruction

clean_db: 	
	@mongosh --eval "db.getSiblingDB('code').dropDatabase()"
	@echo "Dropped 'code' database"

sumo:
	@echo "Started Sumo"
	$(PYTHON) sumo/sumo_simulation.py
	@echo "Generated raw user data"

user_data: clean_db
	python3 sumo/generate_user_data.py
	echo "Generated user data"

	python3 sumo/generate_sniffer_data.py
	echo "Generated sniffer data"

	@mongoimport --host localhost --port 27017 --db code --collection sniffed_data --type csv --file data/sniffed_data.csv --headerline
	@mongoimport --host localhost --port 27017 --db code --collection user_data --type csv --file data/user_data.csv --headerline

# Define a target to run each script separately
group:
	@echo "Aggregating group"
	$(PYTHON) group/aggregation.py
	@echo "Running aggregation of sniffer timestep"
	$(PYTHON) group/aggregate_sniffer_timesteps.py
	@echo "Sniffer timestep aggregation completed"
	@echo "Running grouping"
	$(PYTHON) group/group_parallel.py
	@echo "Grouping completed"

tracking:
	@echo "Running tracking"
	$(PYTHON) tracking/tracking.py
	@echo "Tracking completed"

sanity:
	@echo "Running sanity"
	$(PYTHON) sanity/sanity.py
	@echo "Sanity completed"

reconstruction:
	$(PYTHON) reconstruction/reconstruction_user_data.py
	@echo "Performed Reconstruction User Data"

	$(PYTHON) reconstruction/reconstruction_baseline.py
	@echo "Performed Baseline Reconstruction"

	# $(PYTHON) reconstruction/reconstruction_baseline_random.py
	# @echo "Performed Baseline Reconstruction"

	$(PYTHON) reconstruction/reconstruction_multi.py
	@echo "Performed Multi Reconstruction"

	$(PYTHON) services/plot_reconstruction.py
	@echo "Performed Multi Reconstruction"

# Define a target to clean up any generated files (if needed)
clean:
	rm -f *.pyc
	rm -rf __pycache__

# .PHONY targets tell make these are not files
.PHONY: all run_scripts user_data group tracking sanity reconstruction clean