# -*- coding: utf-8 -*-
import logging
import pymongo
from datetime import datetime
from cookiespool.config import *
from scrapy_redis.defaults import REDIS_CLS


def set_redis_server():
    redis_server = REDIS_CLS(host = REDIS_HOST, port = REDIS_PORT)
    return redis_server

def set_mongo_server(dbname = MONGODB_DBNAME):
        conn = pymongo.MongoClient(host = MONGODB_HOST, port = MONGODB_PORT)
        return conn[dbname]

def set_logger(log_name, log_path):
    logger = logging.getLogger(log_name)
    logger.setLevel(LOG_LEVEL)
    fh = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

