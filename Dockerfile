FROM python:3.14.5-alpine3.22

WORKDIR /etl
COPY requirements.txt requirements.txt  
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . . 
CMD ["python3", "src/main.py"]
