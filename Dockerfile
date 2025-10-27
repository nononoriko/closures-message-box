FROM python:3.10-slim

WORKDIR .

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main/main.py","--inf"]
