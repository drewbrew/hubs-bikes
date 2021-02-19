FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools wheel pipenv

# Adds our application code to the image
COPY . /code
WORKDIR /code

RUN pipenv install

EXPOSE 8000

# Run the production server
CMD pipenv run newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - bikes.wsgi:application
