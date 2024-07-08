import os, sys 
from src.entity.config_entity import FileHandlerConfig
from src.components.data_ingestion import DataIngestion
from src.logger import get_logger
from src.exception import CustomException


class QAPipeline:
    def __init__(self) -> None:
        pass
    
    def start_data_ingestion(self, urls: list[str]):
        """This method is initiates the data ingestion process and
        returns the file handler artifact with the file storage dir path.

    
        Returns:
            FileHandlerArtifact: path of the file storage directory
        """
        try:
            data_ingestion = DataIngestion(FileHandlerConfig())
            file_handler_artifact = data_ingestion.download_data_from_s3(urls)
            return file_handler_artifact 
        except Exception as e:
            raise CustomException(e, sys)
        
        