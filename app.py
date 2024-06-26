from flask import Flask, request
from flask_cors import CORS, cross_origin
from src.pipeline.qa_pipeline import QAPipeline
from src.cloud_storage.aws_storage import S3Handler

# Flask app to use the S3Uploader
app = Flask(__name__)

@cross_origin
@app.route("/")
def test():
    return {"message": "Hello World!"}

@cross_origin
@app.route('/upload/<company_name>', methods=['POST'])
def upload(company_name):
    files = request.files.getlist('file')  # Get list of files from the request
    if not files:
        return {"error": "No files provided"}, 400

    # Initialize the S3Uploader
    s3_uploader = S3Handler(
        bucketname=company_name
    )
    upload_responses = s3_uploader.upload_files(files)
    return {"results": upload_responses}


@cross_origin
@app.route('/chat', methods=['POST'])
def chat():
    
    data = request.get_json()
    question = data['question']
    urls = data['urls']  

    # Ensure urls is a list
    if not isinstance(urls, list):
        urls = [urls]  # Convert single URL to a list
        
            
    #download files
    qa_pipeline = QAPipeline()
    file_handler_artifact = qa_pipeline.start_data_ingestion(urls)
    return {"restlt":file_handler_artifact.file_storage_dir,
            "question":question}
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)