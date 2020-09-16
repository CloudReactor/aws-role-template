# Alpine base image can lead to long compilation times and errors.
# https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.8.5-buster

LABEL maintainer="jeff@cloudreactor.io"

WORKDIR /usr/app

RUN pip install --no-input --no-cache-dir --upgrade pip==20.2.3
RUN pip install --no-input --no-cache-dir pip-tools==5.1.2

COPY generator/requirements.in .

RUN pip-compile --allow-unsafe --generate-hashes requirements.in \
  --output-file requirements.txt

# install dependencies
# https://stackoverflow.com/questions/45594707/what-is-pips-no-cache-dir-good-for
RUN pip install --no-input --no-cache-dir -r requirements.txt

# Output directly to the terminal to prevent logs from being lost
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1

# Don't write *.pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Enable the fault handler for segfaults
# https://docs.python.org/3/library/faulthandler.html
ENV PYTHONFAULTHANDLER 1

ENV PYTHONPATH /usr/app/generator

COPY generator ./generator
COPY src ./src

# TODO
#ARG ENV_FILE_PATH=deploy/files/.env.dev

# copy deployment environment settings
#COPY ${ENV_FILE_PATH} .env

ENTRYPOINT ["python", "generator/make_template.py"]
