from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

'''testing of Data Ingestion Pipeline'''
if __name__ == "__main__":
    try:
        trainingpipelineconfig= TrainingPipelineConfig()   #because this is required for DataIngestionConfig()
        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig)      #because this is required for DataIngestion()
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("intiating the data ingestion")
        dataingestionartifacts= data_ingestion.initiate_data_ingestion()   #called function
        print(dataingestionartifacts)


    except Exception as e:
        raise NetworkSecurityException(e, sys)