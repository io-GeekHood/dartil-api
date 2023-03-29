from shared import *
import redis
import os
import logging



def get_state():
    result = REDIS_CONNECTION.get(STATE_KEYNAME)
    return int(result)

def set_state(number):
    keyname = os.getenv('REDIS_KEY', "dartil_0")
    success = REDIS_CONNECTION.set(STATE_KEYNAME,number)
    if success:
        logging.info(f"state on {keyname} set to {number}")



# checks if this file exist in minio
def minio_exist(bucket,filename):
    logging.info(f"searching for {filename} in {bucket}")
    try:
        objstat = MONGO_CONNECTION.stat_object(bucket,filename)
        minio_obj = objstat.object_name
        if filename == minio_obj:
            logging.info(f"{filename} found !")
            return True
        else:
            logging.info(f"{filename} not found!")
            return False
    except Exception as fail:
        logging.info(f"{filename} does not exist in bucket (valid insert)")
        return False

# checks if this document exist in mongo
def mongo_exist(database,collection,id):
    found = MONGO_CONNECTION[database][collection].count_documents({"_id":id},limit=1)
    if found:
        return True
    return False


# (insert given data into mongodb) check if exist : update if not : insert
def mongo_safe_insert(database,collection,data,replace=True):
    # logging.warning(f"check out data \n\n{data}\n\n")
    try:
        found = mongo_exist(database,collection,data['_id'])
        if found:
            return True
        else:
            MONGO_CONNECTION[database][collection].insert_one(data)
        return True
    except Exception as fail:
        logging.error(f"mongo insert/update for key {data['_id']} failed ! {fail}")
        return False
    
