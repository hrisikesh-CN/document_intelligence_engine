import os, sys 

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import FileHandlerArtifact
from src.logger import get_logger
from src.exception import CustomException


class DataTransformation:
    def __init__(self,
                 file_handler_artifact: FileHandlerArtifact,
                 data_transformation_config: DataTransformationConfig):
        
        self.data_transformation_config = data_transformation_config
        self.file_handler_artifact = file_handler_artifact
        
        
    def transform_data(self):
        try:
            #read the data from the file handler artifact
            file_store_dir = self.file_handler_artifact.file_storage_dir
            #transform the data 
            for file_name in os.listdir(file_store_dir):
                file_full_path = os.path.join(file_store_dir,
                                              file_name)
                
                if os.path.exists(file_full_path):
                    pass
                    #read the data
                
            
            pass
        except Exception as e:
            raise CustomException(e, sys)
        
        