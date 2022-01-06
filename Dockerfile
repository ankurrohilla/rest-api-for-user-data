# pull the official base image
FROM python:3.9-slim-buster
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev
COPY requirements.txt /app/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy project
COPY . /app

COPY start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


