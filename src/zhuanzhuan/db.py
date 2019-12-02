import pymongo
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


def connect_database():
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    MONGODB_HOST = os.getenv('MONGODB_HOST')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT'))

    client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT,
                                 username=MONGODB_USERNAME, password=MONGODB_PASSWORD, authSource=MONGODB_DATABASE)
    return client.get_database(MONGODB_DATABASE)
