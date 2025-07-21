from dataclasses import dataclass

'''output of the DataIngestion task'''
@dataclass
class DataIngestionArtifact:
    trained_file_path: str      #this are two output of data ingestion component
    test_file_path: str

