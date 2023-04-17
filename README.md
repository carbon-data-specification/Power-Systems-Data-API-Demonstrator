# Power Systems Data API Demonstrator

This demonstrator is available [here](ttps://carbon-data-specification.onrender.com).

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
docker-compose  up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml`.

## Project structure

```bash
$ tree "power_systems_data_api_demonstrator"
power_systems_data_api_demonstrator
├── __main__.py
├── settings.py
├── src
│   ├── api
│   │   ├── docs
│   │   ├── grid_node
│   │   └── router.py
│   ├── application.py
│   ├── lib
│   │   ├── db
│   └── lifetime.py
└── tests
    ├── conftest.py
    └── test_****.py
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "POWER*SYSTEMS_DATA_API_DEMONSTRATOR*" prefix.

For example if you see in your "power_systems_data_api_demonstrator/settings.py" a variable named like
`random_parameter`, you should provide the "POWER_SYSTEMS_DATA_API_DEMONSTRATOR_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `power_systems_data_api_demonstrator.settings.Settings.Config`.

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

An example of .env file:

```bash
POWER_SYSTEMS_DATA_API_DEMONSTRATOR_PORT="8000"
```

If you want to use this env file, you will need to run docker in the following way:

```bash
docker-compose --env-file .env up
```

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

- black (formats your code);
- mypy (validates types);
- isort (sorts imports in all files);
- flake8 (spots possibe bugs);

You can read more about pre-commit here: https://pre-commit.com/

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f docker-compose.yml --project-directory . down
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
docker-compose exec api python power_systems_data_api_demonstrator/seed/seed.py
```
