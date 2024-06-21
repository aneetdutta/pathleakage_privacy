import os
from concurrent.futures import ThreadPoolExecutor



def run_in_parallel(*tasks):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(task) for task in tasks]
        for future in futures:
            future.result()

#task
def sumo():
    """Run SUMO simulation."""
    os.system('python3 sumo/sumo_simulation.py')

#task
def user_data():
    DB_NAME = os.getenv("DB_NAME")
    """Generate user data and import to MongoDB."""
    print(os.getenv("IDENTIFIER_LENGTH"))
    os.system('python3 sumo/generate_user_data.py')
    os.system('python3 sumo/generate_sniffer_data.py')
    os.system(f'mongoimport --host localhost --port 27017 --db {DB_NAME} --collection sniffed_data --type csv --file data/sniffed_data_{DB_NAME}.csv --headerline')
    os.system(f'mongoimport --host localhost --port 27017 --db {DB_NAME} --collection user_data --type csv --file data/user_data_{DB_NAME}.csv --headerline')

#task
def group():
    """Run grouping service."""
    os.system('python3 services/group_service.py')

#task
def tracking():
    """Run tracking service."""
    os.system('python3 services/tracking_service.py')

#task
def sanity():
    """Run sanity service."""
    os.system('python3 services/sanity_service.py')

#task
def reconstruction():
    """Run reconstruction service."""
    os.system('python3 reconstruction/reconstruction_baseline.py')
    os.system('python3 reconstruction/reconstruction_baseline_smart.py')
    os.system('python3 reconstruction/reconstruction_multi.py')

#task
def plot():
    """Run plotting service."""
    os.system('python3 services/plot_reconstruction.py')

#task
def clean():
    """Clean up generated files."""
    os.system('rm -f *.pyc')
    os.system('rm -rf __pycache__')
    os.system('rm -rf csv/*.csv')
    os.system('rm -rf data/*.csv')
    os.system('rm -rf logs/*.log')
    os.system('rm -rf images/*.pdf')

#task
def clean_db():
    """Clean the MongoDB database."""
    os.system('mongosh --eval "db.getSiblingDB(\'code\').dropDatabase()"')

#task
def data_gen():
    """Generate data."""
    clean()
    sumo()
    clean_db()
    user_data()

#task
def gtsr():
    """Run group, tracking, sanity, and reconstruction."""
    group()
    tracking()
    sanity()
    reconstruction()

#task
def all_tasks():
    """Run all tasks."""
    sumo()
    data_gen()
    run_in_parallel(gtsr, plot)

#task
def all_without_sumo():
    """Run all tasks except SUMO."""
    data_gen()
    run_in_parallel(gtsr, plot)
    
    
tasks = {
    "sumo": sumo,
    "user_data": user_data,
    "group": group,
    "tracking": tracking,
    "sanity": sanity,
    "reconstruction": reconstruction,
    "plot": plot,
    "clean": clean,
    "clean_db": clean_db,
    "data_gen": data_gen,
    "gtsr": gtsr,
    "all_tasks": all_tasks,
    "all_without_sumo": all_without_sumo
}