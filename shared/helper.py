from shared import *
from minio import Minio
import requests
from pymongo import MongoClient
from bson import ObjectId

# (get a random proxy port from redis to create proxy) check if ran local is true : return empty {} else : return {...proxy}
def get_random_proxy():
    proxy_map = {}
    keyname = "proxies"
    if not bool(eval(LOCALIZED)):
        try:
            port = REDIS_CONNECTION.srandmember(keyname)
            if port:
                logging.debug(f"random port on get {port}")
                proxy_uri = f"http://proxyman:Proxyisawesome1@{PROXY_PROVIDER}:{port}"
                logging.info(f"** < using proxy {proxy_uri} > **")
                proxy_map = {
                    "http": proxy_uri,
                    "https": proxy_uri
                }
            else:
                logging.error(f"failed to get random proxy port from redis!")
        except Exception as fail:
            logging.error(f"failed to get random proxy port from redis!{fail}")
    else:
        logging.info(f"** < requesting with static ip > **")
    return proxy_map

# (get request on given target) check if content_type is image return (byte) else : return (json)
def simple_get(url,content_type:str='json'):
    tries = 0
    while True:
        tries += 1
        if tries > int(TOLLERANCE):
            return {},False
        chosen_proxy = get_random_proxy()
        try:
            logging.info(f"GET: {url}")
            response = requests.get(url,proxies=chosen_proxy,timeout=6)
            if response.status_code == 200:
                logging.info(f"fetched content with status {response.status_code} (success)")
                if content_type == 'byte':
                    return response.content,True
                elif content_type == 'json':
                    try:
                        json_response = response.json()
                        return json_response,True
                    except:
                        logging.error(f"failed to parse content to json format!")
                elif content_type == 'text':
                    text_response = response.text
                    return text_response,True

        except Exception as fail:
            logging.error(f"failed to get content from :\n{url} (retrying {tries}/{TOLLERANCE}) {fail}")

# (get request on given target) check if content_type is image return (byte) else : return (json)
def simple_post(url,body,content_type:str='json'):
    tries = 0
    while True:
        tries += 1
        if tries > int(TOLLERANCE):
            return {},False
        chosen_proxy = get_random_proxy()
        try:
            logging.info(f"GET: {url}")
            response = requests.post(url,json=body,proxies=chosen_proxy,timeout=8)
            if response.status_code == 200:
                logging.info(f"fetched content with status {response.status_code} (success)")
                if content_type == 'byte':
                    return response.content,True
                elif content_type == 'json':
                    try:
                        json_response = response.json()
                        return json_response,True
                    except:
                        logging.error(f"failed to parse content to json format!")
                elif content_type == 'text':
                    text_response = response.text
                    return text_response,True

        except Exception as fail:
            logging.error(f"failed to get content from :\n{url} (retrying {tries}/{TOLLERANCE}) {fail}")



