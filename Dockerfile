FROM python:3.6-alpine

RUN mkdir -p /usr/src/app

ADD . /usr/src/app
WORKDIR /usr/src/app

# different path...
ENV PYTHONPATH .
ENV USERS_API_URL "http://127.0.0.1/stocazzo"
ENV SERVICE_DICOVERY ""

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "auth/app.py" ]