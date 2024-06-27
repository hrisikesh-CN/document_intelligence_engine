import mimetypes
import os

from src.entity.artifact_entity import FileHandlerArtifact
from src.logger import get_logger


class ReadFiles:
    def __init__(self, file_handler_artifact: FileHandlerArtifact):
        self.file_handler_artifact = file_handler_artifact
        self.logger = get_logger(__name__)

    def check_file_type(self, file_path):
        # Define the allowed file types
        allowed_file_types = {
            'application/pdf': 'PDF',
            'application/vnd.ms-powerpoint': 'PPT',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'PPTX',
            'application/msword': 'DOC',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
            'image/png': 'PNG',
            'image/jpeg': 'JPG',
            'application/vnd.ms-excel': 'XLS',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'XLSX',
            'text/csv': 'CSV',
            'text/markdown': 'MD',
            'text/html': 'HTML'
        }

        # Get the MIME type of the file
        mime_type, _ = mimetypes.guess_type(file_path)

        # Check if the MIME type is in the allowed file types
        if mime_type in allowed_file_types:
            return allowed_file_types[mime_type]
        else:
            return None

    def get_file_names_and_types(self) -> list[dict]:
        file_details = []
        for file in os.listdir(self.file_handler_artifact.file_storage_dir):
            file_full_path = os.path.join(self.file_handler_artifact.file_storage_dir,
                                          file)
            if os.path.isfile(file_full_path):
                file_details.append({
                    'filename': file,
                    "full_path": file_full_path,
                    'file_type': self.check_file_type(file_full_path)
                })
        return file_details



