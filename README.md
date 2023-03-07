# power_systems_data_api_demonstrator

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m power_systems_data_api_demonstrator
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "power_systems_data_api_demonstrator"
power_systems_data_api_demonstrator
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variabels should start with "POWER_SYSTEMS_DATA_API_DEMONSTRATOR_" prefix.

For example if you see in your "power_systems_data_api_demonstrator/settings.py" a variable named like
`random_parameter`, you should provide the "POWER_SYSTEMS_DATA_API_DEMONSTRATOR_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `power_systems_data_api_demonstrator.settings.Settings.Config`.

An exmaple of .env file:
```bash
POWER_SYSTEMS_DATA_API_DEMONSTRATOR_RELOAD="True"
POWER_SYSTEMS_DATA_API_DEMONSTRATOR_PORT="8000"
POWER_SYSTEMS_DATA_API_DEMONSTRATOR_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possibe bugs);


You can read more about pre-commit here: https://pre-commit.com/


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml --project-directory . down
```

For running tests on your local machine.


2. Run the pytest.
```bash
pytest -vv .
```

### Seeded Data

The data has been seeded by pulling from a variety of public sources. The data was extracted using python in notebooks that can be accessed using the following command. :

```
poetry run jupyter notebook data/
```

However these scripts require API keys so you will need to set the following variables:

```
# for ELEXON
export BMRS_API_KEY=ABC

# for EIA
export EIA_API_KEY=DEF
```

To seed this data you need to run the following command:
```
poetry run python power_systems_data_api_demonstrator/etl/seed.py
```
