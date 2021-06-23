FROM python:3.9
RUN apt-get update && apt-get install nano sqlite3
COPY ./app .
COPY ./requirements.txt .
COPY ./scrauso.conf .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-u", "main.py", "scrauso.conf"]