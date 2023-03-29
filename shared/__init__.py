import os
import sys
import redis
from pymongo import MongoClient
from minio import Minio
import logging
logging.basicConfig(level=logging.DEBUG, format='(%(asctime)-9s) %(message)s')
# data storage connection
try:
    # mongodb://hds:PvU3oaGvwqocVQu7wa3rdplvnHS2ZOJJ@172.27.226.72:27017
    # mongodb://hit_admin:*5up3r53CUR3D@127.0.0.1:27017
    MONGO_HOST = os.getenv('MONGODB_URI', "mongodb://hit_admin:*5up3r53CUR3D@127.0.0.1:27017")
    logging.info(f"connecting to mongo on :{MONGO_HOST}")
    DATABASE = os.getenv('MONGO_DATABASE', 'dartil-main')
    COLLECTION = "products"
    MONGO_CONNECTION = MongoClient(MONGO_HOST)
except:
    MONGO_HOST = os.getenv('MONGODB_URI', "mongodb://hit_admin:*5up3r53CUR3D@127.0.0.1:27017")
    logging.error(f"failed to initiate mongodb connector module on {MONGO_HOST}")
    sys.exit(1)

# memmory storage connection
try:
    host = os.getenv('REDIS_HOST', "127.0.0.1")
    port = os.getenv('REDIS_PORT', "6379")
    logging.info(f"connecting to redis on :{host}:{port}")
    REDIS_CONNECTION = redis.Redis(host=host, port=int(port), db=0, decode_responses=True)
    STATE_KEYNAME = os.getenv('STATE_KEYNAME', "dartil_0")
    exist = REDIS_CONNECTION.exists(STATE_KEYNAME)
    if not exist:
        REDIS_CONNECTION.set(STATE_KEYNAME,0)
except:
    host = os.getenv('REDIS_HOST', "127.0.0.1")
    port = os.getenv('REDIS_PORT', "6379")
    logging.error(f"failed to initiate redis connector module {host}:{port}")
    sys.exit(1)


# object storage connection
try:
    S3Host = os.environ.get('S3_HOST', 'http://localhost:9000/')
    MinioHost = os.environ.get('AWS_HOST', 'localhost:9000')
    MinioUser = os.environ.get('AWS_ACCESS', 'minioadmin')
    MinioPass = os.environ.get('AWS_SECRET', 'sghllkfij,dhvrndld')
    BUCKET = os.environ.get('BUCKET_NAME',"test")
    logging.info(f"connecting to minio on :{MinioHost}")
    MINIO_CONNECTION = Minio(
                MinioHost,
                access_key=MinioUser,
                secret_key=MinioPass,
                secure=False
            )
except:
    MinioHost = os.environ.get('AWS_HOST', 'localhost:9000')
    logging.error(f"failed to initiate minio connector module on {MinioHost} ( {MinioUser} | {MinioPass} )")
    sys.exit(1)



# public configurations
LOCALIZED = os.environ.get('LOCALIZED', 'True')
PROXY_PROVIDER = os.environ.get('PROXY_PROVIDER', '172.27.226.11')
TOLLERANCE = os.environ.get('TOLLERANCE', '5')
SLEEPING = os.environ.get('SLEEPING', '3')
