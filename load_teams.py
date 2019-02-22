import mongo_connector
import json


db_client = mongo_connector.get_connection()
try:
    db = db_client.fifa
    team_collection = db['teams']

    with open('fifa.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    team_collection.insert(data)
finally:
    db_client.close()
