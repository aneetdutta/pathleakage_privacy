from pymongo import MongoClient
from bson.son import SON

class MongoDB:

    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.get_database("code")
        # self.collection = self.db[collection_name]
        self.timesteps = []

    def set_collection(self, collection_name):
        self.collection = self.db[collection_name]
        
    def get_all_timesteps(self):
        self.timesteps = self.collection.find().distinct("timestep")
        return self.timesteps

    def aggregate_save(self):
        pipeline = [
                {
                    "$addFields": {
                        "dist_S_U": {
                            "$sqrt": {
                                "$add": [
                                    {
                                        "$pow": [
                                            {
                                                "$subtract": [
                                                    {"$toDouble": {"$arrayElemAt": ["$sniffer_location", 0]}},
                                                    {"$toDouble": {"$arrayElemAt": ["$location", 0]}},
                                                ]
                                            },
                                            2,
                                        ]
                                    },
                                    {
                                        "$pow": [
                                            {
                                                "$subtract": [
                                                    {"$toDouble": {"$arrayElemAt": ["$sniffer_location", 1]}},
                                                    {"$toDouble": {"$arrayElemAt": ["$location", 1]}},
                                                ]
                                            },
                                            2,
                                        ]
                                    },
                                ]
                            }
                        }
                    }
                },
                {
                    '$group': {
                        '_id': {
                            'timestep': '$timestep',
                            'sniffer_id': '$sniffer_id'
                        },
                        'data': {
                            '$push': {
                                "protocol": "$protocol",
                                "lte_id": "$lte_id",
                                "WiFi_id": "$WiFi_id",
                                "bluetooth_id": "$bluetooth_id",
                                "dist_S_U": "$dist_S_U",
                                "location": "$location",
                            }
                        }
                    }
                },
                {
                    '$group': {
                        '_id': '$_id.timestep',
                        'sniffer_data': {
                            '$push': {
                                'k': { '$toString': '$_id.sniffer_id' },
                                'v': '$data'
                            }
                        }
                    }
                },
                {
                    '$project': {
                        '_id': 0,
                        'timestep': '$_id',
                        'sniffer_data': {
                            '$arrayToObject': '$sniffer_data'
                        }
                    }
                }
            ]
        
        return self.collection.aggregate(pipeline)

    def aggregate_timestep(self):
        pipeline = [
            {
                '$group': {
                    '_id': '$timestep',
                    "lte_ids": {"$addToSet": "$lte_id"},
                    "bluetooth_ids": {"$addToSet": "$bluetooth_id"},
                    "wifi_ids": {"$addToSet": "$WiFi_id"}
                }
            },
            {
                '$project': {
                    'timestep': '$_id',
                    '_id': 0,
                    'lte_ids': 1,
                    'bluetooth_ids': 1,
                    'wifi_ids': 1,
                    "ids": {
                        "$setUnion": ["$lte_ids", "$bluetooth_ids", "$wifi_ids"]
                    }
                }
            },
            {
                "$sort": { "timestep": 1 }  # Sort by timestep in ascending order
            }
        ]

        return self.collection.aggregate(pipeline)


    def aggregate_users(self):
        pipeline = [
            {
                '$group': {
                    '_id': '$user_id',
                    "lte_ids": {"$addToSet": "$lte_id"},
                    "bluetooth_ids": {"$addToSet": "$bluetooth_id"},
                    "wifi_ids": {"$addToSet": "$WiFi_id"}
                }
            },
            {
                '$project': {
                    'user_id': '$_id',
                    '_id': 0,
                    'lte_ids': 1,
                    'bluetooth_ids': 1,
                    'wifi_ids': 1,
                    "ids": {
                        "$setUnion": ["$lte_ids", "$bluetooth_ids", "$wifi_ids"]
                    }
                }
            },
            {
                "$sort": { "user_id": 1 }  # Sort by timestep in ascending order
            }
        ]
        return self.collection.aggregate(pipeline)
        
    def batch_insert(self, collection, documents, batch_size=100):
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            collection.insert_many(batch)