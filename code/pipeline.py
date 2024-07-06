import os
from concurrent.futures import ThreadPoolExecutor
import subprocess
env_instance = os.environ.copy()

def run_in_parallel(*tasks):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(task) for task in tasks]
        for future in futures:
            future.result()

def run_command(command, env=env_instance):
    """Run a command with optional environment variables."""
    result = subprocess.run(command, shell=True, env=env)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        
        
def sumo():
    """Run SUMO simulation."""
    print("Starting SUMO simulation...")
    run_command('python3 sumo/sumo_simulation.py')
    print("SUMO simulation finished.")

def generate_user_data():
    print("Running generate_user_data.py...")
    run_command('python3 sumo/generate_user_data.py')
    print("generate_user_data.py finished.")
    
def generate_sniffer_data():
    print("Running generate_sniffer_data.py...")
    run_command('python3 sumo/generate_sniffer_data.py')
    print("generate_sniffer_data.py finished.")
    
def import_sniffer_data_mongo():
    DB_NAME = os.getenv("DB_NAME")
    print("Importing sniffed data to MongoDB...")
    run_command(f'mongosh --host localhost --port 27017 --eval "use {DB_NAME}; db.sniffed_data.drop()"')
    run_command(f'mongoimport --host localhost --port 27017 --db {DB_NAME} --collection sniffed_data --type csv --file data/sniffed_data_{DB_NAME}.csv --headerline')
    print("sniffed data imported to MongoDB.")
    
def import_user_data_mongo():
    DB_NAME = os.getenv("DB_NAME")
    print("Importing user data to MongoDB...")
    run_command(f'mongosh --host localhost --port 27017 --eval "use {DB_NAME}; db.user_data.drop()"')
    run_command(f'mongoimport --host localhost --port 27017 --db {DB_NAME} --collection user_data --type csv --file data/user_data_{DB_NAME}.csv --headerline')
    print("user data imported to MongoDB.")
    
def import_data_mongo():
    import_sniffer_data_mongo()
    import_user_data_mongo()
    
def user_data():
    """Generate user data and import to MongoDB."""
    print("Starting user data generation...")
    generate_user_data()
    generate_sniffer_data()
    import_sniffer_data_mongo()
    import_user_data_mongo()
    print("User data generation and import finished.")

def aggregate():
    """Running aggregation."""
    print("Starting aggregation process...")
    
    print("Running aggregate_sniffer_timesteps.py...")
    run_command("python3 group/aggregate_sniffer_timesteps.py")
    print("aggregate_sniffer_timesteps.py finished.")
    
    print("Running aggregation.py...")
    run_command("python3 group/aggregation.py")
    print("aggregation.py finished.")
    
    print("Aggregation process finished.")

def aggregate_timesteps():
    print("Running aggregation.py...")
    run_command("python3 group/aggregation.py")
    print("aggregation.py finished.")

def group_multi():
    """Run grouping service."""
    print("Starting group_multi service...")
    run_command("python3 group/group_seq.py")
    print("group_multi service finished.")

def tracking_multi():
    """Run tracking service."""
    print("Starting tracking_multi service...")
    run_command('python3 tracking/tracking_multi.py')
    print("tracking_multi service finished.")

def group_smart():
    """Run grouping service."""
    print("Starting group_smart service...")
    run_command("python3 group/group_smart_seq.py")
    print("group_smart service finished.")

def tracking_smart():
    """Run tracking service."""
    print("Starting tracking_smart service...")
    run_command('python3 tracking/tracking_smart.py')
    print("tracking_smart service finished.")

    
def sanity():
    """Run sanity service."""
    print("Starting Group Checker service...")
    run_command('python3 sanity/group_checker.py')
    print("Group Checker finished.")
    print("Starting sanity service...")
    run_command('python3 sanity/sanity.py')
    print("sanity service finished.")

def reconstruction_baseline():
    run_command('python3 reconstruction/reconstruction_baseline.py')
    print("reconstruction_baseline.py finished.")
    
def reconstruction_baseline_smart():
    run_command('python3 reconstruction/reconstruction_baseline_smart.py')
    print("reconstruction_baseline_smart.py finished.")

def reconstruction_multi():
    run_command('python3 reconstruction/reconstruction_multi.py')
    print("reconstruction_multi.py finished.")

def reconstruction_user_data():
    print("Starting reconstruction service...")
    run_command('python3 reconstruction/reconstruction_user_data.py')
    print("reconstruction_user_data.py finished.")
    
def reconstruction_without_smart():
    """Run reconstruction service."""
    reconstruction_user_data()
    reconstruction_baseline()
    reconstruction_multi()
    print("Reconstruction service finished.")
    
def reconstruction():
    """Run reconstruction service."""
    reconstruction_user_data()
    reconstruction_baseline()
    # reconstruction_multi()
    run_in_parallel(reconstruction_baseline_smart, reconstruction_multi)
    print("Reconstruction service finished.")

def plot():
    """Run plotting service."""
    print("Starting plotting service...")
    run_command('python3 plot/plot_reconstruction.py')
    print("plotting service finished.")

def clean():
    """Clean up generated files."""
    run_command('rm -f *.pyc')
    run_command('rm -rf __pycache__')
    # run_command('rm -rf csv/*.csv')
    # run_command('rm -rf data/*.csv')
    run_command('rm -rf logs/*.log')
    # run_command('rm -rf images/*.pdf')

#task
def clean_db():
    DB_NAME = os.getenv("DB_NAME")
    """Clean the MongoDB database."""
    run_command(f'mongosh --eval "db.getSiblingDB(\'{DB_NAME}\').dropDatabase()"')

def after_aggregate_without_smart():
    multi()
    sanity()
    reconstruction_without_smart()
    plot()	
#task
def data_gen():
    """Generate data."""
    clean()
    sumo()
    clean_db()
    user_data()
    
def data_gen_without_sumo():
    """Generate data."""
    clean_db()
    user_data()

#task
def multi():
    """Run group, tracking, sanity, and reconstruction."""
    group_multi()
    tracking_multi()

def smart():
    """ Running Smart Service """
    group_smart()
    tracking_smart()
    # pass
    
def gtrp():
    run_in_parallel(multi, smart)
    sanity()
    reconstruction()
    plot()
    
#task
def all_tasks():
    """Run all tasks."""
    data_gen()
    aggregate()
    run_in_parallel(multi, smart)
    sanity()
    reconstruction()
    plot()

def all_tasks_without_smart_without_sumo():
    """Run all tasks."""
    clean_db()
    user_data()
    # data_gen()
    aggregate()
    multi()
    sanity()
    reconstruction_without_smart()
    plot()
    
def all_tasks_without_smart():
    """Run all tasks."""
    data_gen()
    aggregate()
    multi()
    sanity()
    reconstruction_without_smart()
    plot()
    
#task
def all_without_sumo():
    """Run all tasks except SUMO."""
    data_gen_without_sumo()
    aggregate()
    run_in_parallel(multi, smart)
    sanity()
    reconstruction()
    plot()

def tracking_until():
    """Run all tasks except SUMO."""
    tracking_multi()
    # sanity()
    reconstruction()
    # plot()
    
def limit_users_after_user_data():    
    print("Running limit_users.py...")
    run_command('python3 sumo/limit_users.py')
    print("limit_users.py finished.")
    
tasks = {
    "sumo": sumo,
    "user_data": user_data,
    "generate_user_data": generate_user_data,
    "generate_sniffer_data": generate_sniffer_data,
    "import_user_data_mongo": import_user_data_mongo,
    "import_sniffer_data_mongo": import_sniffer_data_mongo,
    "reconstruction_user_data": reconstruction_user_data,
    "reconstruction_without_smart": reconstruction_without_smart,
    "all_tasks_without_smart_without_sumo": all_tasks_without_smart_without_sumo,
    "group_multi": group_multi,
    "tracking_multi": tracking_multi,
    "group_smart": group_smart,
    "tracking_smart": tracking_smart,
    "tracking_until": tracking_until,
    "aggregate": aggregate,
    "sanity": sanity,
    "reconstruction": reconstruction,
    "reconstruction_baseline": reconstruction_baseline,
    "reconstruction_multi": reconstruction_multi,
    "plot": plot,
    "clean": clean,
    "clean_db": clean_db,
    "data_gen": data_gen,
    "multi": multi,
    "smart": smart,
    "gtrp": gtrp,
    "all_tasks": all_tasks,
    "all_without_sumo": all_without_sumo,
    "data_gen_without_sumo": data_gen_without_sumo,
    "all_tasks_without_smart": all_tasks_without_smart,
    "after_aggregate_without_smart": after_aggregate_without_smart,
    "import_data_mongo": import_data_mongo,
    "aggregate_timesteps": aggregate_timesteps,
    "limit_users_after_user_data": limit_users_after_user_data
}
