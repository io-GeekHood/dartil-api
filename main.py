from shared import *
import time
import json
import io
from shared.helper import *
from assets.refresh_init_categories import put_collections_in_mongo
import logging
from shared.connectors import *
def renew_dartil_collections(client:MongoClient):
    put_collections_in_mongo(client)



def get_products_dartil(client:MongoClient):
    collection = client[DATABASE]["collections"]
    passed = get_state()
    for doc in collection.aggregate([{"$skip":passed}]):
        for category in doc["collections"]:
            for page in range(1,150):
                time.sleep(int(SLEEPING))
                category_id = category["parent_id"]
                facet_request = {
                    "productFilter": {
                        "baseFilter": {
                        "categories": [
                            category_id
                        ]
                        },
                        "categories": [
                            category_id
                        ],
                        "price": {},
                        "booleanProductFilters": [],
                        "vendors": [],
                        "productRate": {},
                        "brands": [],
                        "attributes": []
                    },
                    "pageNumber": page,
                    "facets": 1203
                }
                target = "https://gateway.dartil.com/Web/GeneralData/Collection/products-facets"
                result,success = simple_post(target,body=facet_request)
                if success:
                    if "data" in result.keys() and len(result["data"]["products"]) > 0:
                        for product in result["data"]["products"]:
                            try:
                                product["_id"] = product["id"]
                                del product["id"]
                                catalog_endpoint = f"https://gateway.dartil.com/Web/Catalog/product/{product['_id']}"
                                catalogs,success = simple_get(catalog_endpoint)
                                if success:
                                    try:
                                        logging.info(f"appending product catalog to result !")
                                        catalog = catalogs["data"]
                                        media = [f"https://cdn.dartil.com/{url['path']}" for url in catalog["uniqueProducts"][0]['mediaList']]
                                    except Exception as fail:
                                        logging.warning(f"could not fetch catalog data for product: {catalog_endpoint}")
                                        catalog = {}
                                        media = []
                                else:
                                    logging.warning(f"could not fetch catalog data for product: {catalog_endpoint}")
                                    catalog = {}
                                    media = []
                                product["catalog"]= catalog
                                mongo_safe_insert(DATABASE,COLLECTION,product)
                                logging.info(f"inserted new document with len #{len(product)} ")
                                if len(media) > 0:
                                    get_page_media_dartil(product["_id"],media)
                            except Exception as fail:
                                logging.warning(f"mongo data insertion failiure for json object ({product['name']}) | {fail}")
                    else:
                        logging.info(f"{category['title']} ran out of products on page #{page} (pagination break...)")
                        break

def get_page_media_dartil(prid,urls:list=[]):
    for idx,image in enumerate(urls):
        filename = f"{prid}_{idx}.jpg"
        exist = minio_exist(BUCKET,filename)
        if exist:
            continue
        byte_response,success = simple_get(url=image,content_type='byte')
        if success:
            try:
                buffer = bytearray(byte_response)
                byte_len = len(buffer)
                value_as_a_stream = io.BytesIO(buffer)
            except Exception as fail:
                logging.error(f"failed to digest media response content into byte-stream ! {fail}")
            try:
                
                MINIO_CONNECTION.put_object(bucket_name=BUCKET,object_name=filename,length=byte_len,data=value_as_a_stream)
                logging.info(f"image {filename} lenght #{byte_len} uploaded with success !")
            except Exception as fail:
                logging.error(f"failed to save image bytes in minio bucket {fail}")


if __name__ == '__main__':
    client = MongoClient(MONGO_HOST)
    get_products_dartil(client)

