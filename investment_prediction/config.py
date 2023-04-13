import pymongo
import pandas as pd
import json 
from dataclasses import dataclass
import os


DATABASE_NAME="TimeSeries"

COLLECTION_NAME_br ="britannia"
COLLECTION_NAME_itc = 'itc'
COLLECTION_NAME_rel = 'reliance'
COLLECTION_NAME_tatam = 'tatamotors'
COLLECTION_NAME_tcs = 'tcs'

raw_file_path = os.path.join(os.getcwd(),"raw_dataset")
preprocessed_file_path = os.path.join(os.getcwd(),"pre_processed_dataset")


time_horizon = 1    # time horizon is the number of months, years, or decades you need to invest to achieve your financial goal.
no_of_features = 5    # number of features

@dataclass
class EnvironmentVariable:
    """
    In this class we are accessing the variables declared in .env file
    """
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_access_secret_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")

env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = ""