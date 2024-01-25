import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
test_kb = client['test_knowledge_base']