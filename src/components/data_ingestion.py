from typing import Union, List
import os, sys
from src.cloud_storage.aws_storage import S3Handler
from src.utils import extract_s3_info
from src.entity.config_entity import FileHandlerConfig
from src.entity.artifact_entity import FileHandlerArtifact
from src.logger import get_logger
from src.exception import CustomException
class DataIngestion:
    def __init__(self,
                 file_handler_config: FileHandlerConfig):
        self.logger = get_logger(__name__)
        self.file_handler_config = file_handler_config



    def download_data_from_s3(self,
                              urls: List[str]):
        try:
            #download files from s3
            
            for url in urls:
                bucket_name, object_key = extract_s3_info(url)
                local_file_storage_path = os.path.join(
                    self.file_handler_config.file_storage_dir,
                    bucket_name, #company name
                    object_key
                )
                
                if not os.path.exists(local_file_storage_path):
                    os.makedirs(os.path.dirname(local_file_storage_path), exist_ok=True)
                
                
                S3Handler.download_file_from_s3(
                    bucket_name=bucket_name,
                    object_key=object_key,
                    local_file_path=local_file_storage_path
                    )
                
                self.logger.info(f"Data download complete for bucket %s" % bucket_name)
                
            return FileHandlerArtifact(
                                        file_storage_dir=os.path.join(
                                        self.file_handler_config.file_storage_dir,
                                        bucket_name)
                                        )


        except Exception as e:
            raise CustomException(e, sys)


