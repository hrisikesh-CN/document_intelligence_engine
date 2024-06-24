FROM python:3.10.6-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
# Expose the port that Streamlit will run on
EXPOSE 5000

CMD [ "python3","app.py" ]