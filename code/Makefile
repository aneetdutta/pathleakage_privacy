# Define the Python interpreter
PYTHON = python3

# Define the default target
all: sumo data_gen gtsr smart plot

all_without_sumo: data_gen gtsr

gts: group tracking sanity

all_without_reconstruction: clean sumo data_gen gts

gtsr: group tracking sanity reconstruction

clean_db: 	
	@mongosh --eval "db.getSiblingDB('code').dropDatabase()"
	@echo "Dropped 'code' database"

sumo:
	@echo "Started Sumo"
	$(PYTHON) sumo/sumo_simulation.py
	@echo "Generated raw user data"

data_gen: clean_db user_data

user_data:
	time python3 sumo/generate_user_data.py
	echo "Generated user data"

	time python3 sumo/generate_sniffer_data.py
	echo "Generated sniffer data"

	@mongoimport --host localhost --port 27017 --db code --collection sniffed_data --type csv --file data/sniffed_data.csv --headerline
	@mongoimport --host localhost --port 27017 --db code --collection user_data --type csv --file data/user_data.csv --headerline

# Define a target to run each script separately
group:
	@echo "Aggregating group"
	time $(PYTHON) group/aggregation.py
	@echo "Running aggregation of sniffer timestep"
	time $(PYTHON) group/aggregate_sniffer_timesteps.py
	@echo "Sniffer timestep aggregation completed"
	@echo "Running grouping"
	time $(PYTHON) group/group_seq.py
	@echo "Grouping completed"

tracking:
	@echo "Running tracking"
	time $(PYTHON) tracking/tracking_multi.py
	@echo "Tracking completed"

smart:
	@echo "Running Smart Grouping"
	time $(PYTHON) group/group_smart_seq.py
	@echo "Grouping completed"
	@echo "Running Smart tracking"
	time $(PYTHON) tracking/tracking_smart.py
	@echo "Tracking completed"
	time $(PYTHON) reconstruction/reconstruction_baseline_smart.py
	@echo "Tracking completed"

sanity:
	@echo "Running sanity"
	time $(PYTHON) sanity/sanity.py
	@echo "Sanity completed"

reconstruction:
	time $(PYTHON) reconstruction/reconstruction_user_data.py
	@echo "Performed Reconstruction User Data"

	time $(PYTHON) reconstruction/reconstruction_baseline.py
	@echo "Performed Baseline Reconstruction"

	# $(PYTHON) reconstruction/reconstruction_baseline_random.py
	# @echo "Performed Baseline Reconstruction"

	time $(PYTHON) reconstruction/reconstruction_multi.py
	@echo "Performed Multi Reconstruction"

plot:
	time $(PYTHON) services/plot_reconstruction.py
	@echo "Performed Multi Reconstruction"


# Define a target to clean up any generated files (if needed)
clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf csv/*.csv
	rm -rf data/*.csv
	rm -rf logs/*.log
	rm -rf images/*.pdf

# .PHONY targets tell make these are not files
.PHONY: all run_scripts user_data group tracking sanity reconstruction clean data_gen sumo gtsr gts clean_db all_without_sumo plot smart