FROM python:3.10-alpine
LABEL maintainer="contactugodaniels@gmail.com"

# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# # Only update packages
# RUN apt-get update

# Set working directory
WORKDIR /backend

# copy requirements files
COPY ./requirements.txt /backend/requirements.txt

# install requirements
RUN python -m venv /py && \
    /py/bin/pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

# Copy codebase
COPY . /backend/

USER django-user
