FROM python:3.9
COPY ./app .
COPY ./requirements.txt .
COPY ./scrauso.conf .

RUN pip install -r requirements.txt
CMD ["python", "-u", "main.py", "scrauso.conf"]