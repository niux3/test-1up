FROM python:3.9
WORKDIR /code
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY ./Pipfile /code/Pipfile
RUN pipenv install
COPY ./app /code/app
CMD ["pipenv", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
