import pymongo
from pymongo import MongoClient

def copy_collections(source_uri, source_db_name, target_uri, target_db_name, collections):
    # Connect to the source MongoDB
    source_client = MongoClient(source_uri)
    
    source_db = source_client[source_db_name]
    print("connected")
    # Connect to the target MongoDB
    target_client = MongoClient(target_uri)
    target_db = target_client[target_db_name]
    
    for collection_name in collections:
        # Get the collection from the source database
        source_collection = source_db[collection_name]
        print(source_collection)
        
        # Get the collection from the target database
        target_collection = target_db[collection_name]
        
        # Copy all documents from the source collection to the target collection
        documents = list(source_collection.find())
        if documents.count() > 0:
            target_collection.insert_many(documents)
        
        print(f"Copied {source_collection.count_documents({})} documents from {source_db_name}.{collection_name} to {target_db_name}.{collection_name}")

# Configuration
source_uri = "mongodb://localhost:27017"
source_db_name = "scenario1a2"
target_uri = "mongodb://localhost:27017"
target_db_name = "scenario4a2"
collections = ["modified_inter_mappings", "reconstruction_baseline", "collection3"]  # Add your collection names here

# Run the copy function
copy_collections(source_uri, source_db_name, target_uri, target_db_name, collections)
