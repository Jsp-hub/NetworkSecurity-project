from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig

from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer


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


        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifacts)  #the order of passing the argument must be same as in ModelTrainer
        logging.info("Initiating model training")
        model_trainer_artifacts = model_trainer.initiate_model_trainer()
        logging.info("Model Training Completed")
        #print(model_trainer_artifacts)   # path won't be printed in terminal so remove it



    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
