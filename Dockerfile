FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "./main.py"]