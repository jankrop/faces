# syntax=docker/dockerfile:1

FROM python:3.9
EXPOSE 80
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]
