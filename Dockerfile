FROM python:3.10.0-alpine

COPY ./ ./app

WORKDIR ./app

RUN pip install -r requirements.txt

CMD ["python", "./src/bot.py"]