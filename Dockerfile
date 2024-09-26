FROM python:3.9.20-slim
WORKDIR /app
COPY . .

RUN pip install python-dotenv

CMD ["python3", "main.py"]