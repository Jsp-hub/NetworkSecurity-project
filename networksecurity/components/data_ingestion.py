'''this file is responsible for what steps will be performed in data ingestion task'''

'''tasks performed in data ingestion:
1)data will be read from MongoDB
2)creating feature store(raw.csv)
3)split into train and test
4)save train.csv and test.csv into ingested folder '''

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#configurations of the Data Ingestion steps
from networksecurity.entity.config_entity import DataIngestionConfig

import os
import sys
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

from networksecurity.entity.artifact_entity import DataIngestionArtifact  # added for initiate_data_ingestion(self) function

'''reading data from MongoDB'''
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    '''function to get the dataframe from mongoDB'''
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name   # from config_entity it will be read from hardcoded values from constant and will use here
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI) 
            collection = self.mongo_client[database_name][collection_name]   #this might be changed as per push_data.py if error encounterd otherwise fine
            
            df=pd.DataFrame(list(collection.find()))
            '''when data is read from mongoDB, extra column _id is added, so remove it'''
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"], axis =1)
            
            df.replace({"na":np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    

    '''saving the data collected from MongoDB in Feature store as csv file'''
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path  #this filepath is there in constants so csv will be saved in that location as phisingData.csv - this will be handled by config_entity.py file
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test data as a csv into file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

     
    '''combining all steps'''
    def initiate_data_ingestion(self):
          
        try:
            dataframe = self.export_collection_as_dataframe()    # 1st step
            dataframe = self.export_data_into_feature_store(dataframe)  #2nd step
            self.split_data_as_train_test(dataframe)      #3rd step
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

'''after this data ingestion the main output is our test.csv ad train.csv which we will use further'''
'''so, make a file artifact_entity.py where the output of each component(ingestion, validation, training, eval) is to be saved'''