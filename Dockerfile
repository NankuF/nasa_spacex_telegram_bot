FROM python:alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "apod_auto_posting.py"]