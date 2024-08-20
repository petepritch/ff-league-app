FROM python:3.9

WORKDIR /fantasy-football-bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./bot ./bot

CMD ["python", "./bot/main.py"]