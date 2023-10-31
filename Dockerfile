FROM python:3.11

WORKDIR /app

copy requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "Mobius.py"]
