FROM python:3.9
RUN apt-get update
COPY ./app .
COPY ./requirements.txt .
COPY ./scrauso.conf .

RUN pip install -r requirements.txt
CMD ["python", "main.py", "scrauso.conf"]