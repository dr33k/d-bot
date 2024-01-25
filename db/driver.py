import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
kb = client['knowledge_base']
