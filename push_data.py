'''this is the ETL pipeline that extract data from local machine, transform it into json and load it to MongoDB'''

import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException
        
    def cv_to_json(self, file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)  #reset the dataframe index to 0
            #converting data into mongoDB fromat
            records = list(json.loads(data.T.to_json()).values())
            return records       # records must be returned otherwise empty list exception will be raised

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self,records, database, collection):   #database, collection are attributes of mongodb
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)   #connect to your mongoDB
            self.database = self.mongo_client[database]
            self.collection = collection
            self.records=records
            self.collection= self.database[self.collection]        #from this recored will be inserted in specific collection under specified database on mongoDB
            self.collection.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        


if __name__ == '__main__':
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "Jeel's_DB"
    COLLECTION = "NetworkData"
    #creating object of NetworkDataExtract class
    networkobj= NetworkDataExtract()
    records=networkobj.cv_to_json(file_path=FILE_PATH)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE, COLLECTION)  # returns no. of record because the function returns no of record after inserting records in database
    print(f"Inserted {no_of_records} records in your MongoDB")


