from flask import Flask, request
from src.cloud_storage.aws_storage import S3Uploader

# Flask app to use the S3Uploader
app = Flask(__name__)

@app.route("/")
def test():
    return {"message": "Hello World!"}

@app.route('/upload/<company_name>', methods=['POST'])
def upload(company_name):
    files = request.files.getlist('file')  # Get list of files from the request
    if not files:
        return {"error": "No files provided"}, 400

    # Initialize the S3Uploader
    s3_uploader = S3Uploader(
        bucketname=company_name
    )
    upload_responses = s3_uploader.upload_files(files)
    return {"results": upload_responses}

if __name__ == "__main__":
    app.run(port=5000)