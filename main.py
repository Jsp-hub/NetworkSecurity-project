from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig

from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation


'''testing of Data Ingestion Pipeline'''
if __name__ == "__main__":
    try:
        trainingpipelineconfig= TrainingPipelineConfig()   #because this is required for DataIngestionConfig()

        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig)      #because this is required for DataIngestion()
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("intiating the data ingestion")
        dataingestionartifacts= data_ingestion.initiate_data_ingestion()   #called function
        logging.info("data ingestion completed")
        print(dataingestionartifacts)


        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifacts, data_validation_config)
        logging.info("Initiating data validation")
        data_validation_artifacts = data_validation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_artifacts)

        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifacts, data_transformation_config)
        logging.info("Initiating data ingestion")
        data_transformation_artifacts = data_transformation.initiate_data_transformation()
        logging.info("data transformation completed")
        print(data_transformation_artifacts)


    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
