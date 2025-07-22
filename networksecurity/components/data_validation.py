from networksecurity.entity.artifact_entity import DataIngestionArtifact   #input of data validation task = output of data ingestion artifacts
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import os, sys
#for data drift
from scipy.stats import ks_2samp
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.utils.main_utils.utils import write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_numerical_columns_present(self) -> bool:
        try:
            expected_numerical_columns = self._schema_config['numerical_columns']
            train_df = DataValidation.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = DataValidation.read_data(self.data_ingestion_artifact.test_file_path)

            train_numerical_cols = train_df.select_dtypes(include=['number']).columns.tolist()
            test_numerical_cols = test_df.select_dtypes(include=['number']).columns.tolist()

            missing_in_train = [col for col in expected_numerical_columns if col not in train_numerical_cols]
            missing_in_test = [col for col in expected_numerical_columns if col not in test_numerical_cols]

            if missing_in_train or missing_in_test:
                logging.warning(f"Missing numerical columns in train: {missing_in_train}")
                logging.warning(f"Missing numerical columns in test: {missing_in_test}")
                return False

            return True

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold = 0.05) -> bool:
        try:
            status = True         #assuming no drift initially
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1, d2)
                if threshold<=is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False

                report.update({column:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
        
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        


        
    def initiate_data_validation(self)->DataValidationArtifact:         #this is the final function where all the above methods are initialised for data validation task
        '''Step -1 : reading the data'''
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)       
            test_dataframe=DataValidation.read_data(test_file_path)

            '''Step -2 : validate number of columns '''

            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
                
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n" 
                

            '''Step - 3: validate numerical columns'''  
            status = self.validate_numerical_columns_present()
            if not status:
                error_message = f"Numerical columns missing or mismatched in train or test dataset.\n"
                

            '''Step - 4: checking data drift'''
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)