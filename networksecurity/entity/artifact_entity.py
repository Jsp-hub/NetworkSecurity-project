from dataclasses import dataclass

'''output of the DataIngestion task'''
@dataclass
class DataIngestionArtifact:
    trained_file_path: str      #this are two output of data ingestion component
    test_file_path: str

@dataclass
class DataValidationArtifact:      # outputs of data validation task
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str