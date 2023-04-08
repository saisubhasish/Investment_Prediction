from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    dataset1_file_path:str
    dataset2_file_path:str
    dataset3_file_path:str
    dataset4_file_path:str
    dataset5_file_path:str
    

@dataclass
class DataValidationArtifact:
    train_file_path:str 
    test_file_path:str
    report_file_path:str