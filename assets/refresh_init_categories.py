import time
import requests
import re
import json
import logging
logging.basicConfig(level=logging.DEBUG, format='(%(asctime)-9s) %(message)s')


def put_collections_in_mongo(mongo_cli):
    body = [
    {
        "id": "1067813990035357696",
        "parameters": None
    },
    {
        "id": "1067816789812969472",
        "parameters": None
    },
    {
        "id": "1067817281960017920",
        "parameters": None
    },
    {
        "id": "1067817548143132672",
        "parameters": None
    },
    {
        "id": "1067818167914463232",
        "parameters": None
    }
    ]
    target = "https://mobile.dartil.com/App/GeneralData/Collection/mobile-result"
    result,success = requests.post(target,json=body)
    buffer = []
    for base_category in result["data"]:
        if len(base_category["data"]) > 0:
            collection_buffer = {}
            for collection_info in base_category["data"]:
                collection_buffer[collection_info["name"]] = collection_info["id"]
        tree = {"_id":base_category["id"],"category_group_name":base_category["title"],"collections":collection_buffer}
        mongo_cli["dartil-main"]["collections"].insert_one(tree)


