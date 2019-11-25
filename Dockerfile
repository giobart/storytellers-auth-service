FROM python:3.6-alpine

RUN mkdir -p /usr/src/app

ADD . /usr/src/app
WORKDIR /usr/src/app

# different path...
ENV PYTHONPATH .
# ENV USERS_API "http://127.0.0.1:5001" uncomment this and place the right USERS_API url to test locally
# ENV SERVICE_DICOVERY ""

RUN pip install -r requirements.txt

EXPOSE 5005

CMD [ "python", "auth/app.py" ]
