FROM python:3.9
RUN apt-get update
RUN apt-get install nano sqlite3
COPY ./app .
COPY ./requirements.txt .
COPY ./scrauso.conf .

RUN pip install -r requirements.txt
CMD ["python", "main.py", "scrauso.conf"]