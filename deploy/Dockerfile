FROM python:3.9.6-slim-buster


RUN pip install poetry==1.2.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/
WORKDIR /app

# Installing requirements
RUN poetry install

# Copying actual application
COPY . /app/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "power_systems_data_api_demonstrator"]
