# mind_matter

TechCare Coaching's Cohort 12/2024

```
project_root/
├── app/
│ ├── __init__.py # App factory and initialization
│ ├── routes/
│ │ ├── __init__.py # Import all API routes
│ │ ├── users.py # User-related API routes
│ │ ├── items.py # Item-related API routes
│ ├── models.py # Database models
│ ├── services.py # Business logic
│ ├── extensions.py # Flask extensions (e.g., SQLAlchemy, Migrate)
│ ├── config.py # App configurations
├── migrations/ # Database migration scripts
├── tests/
│ ├── conftest.py # Pytest setup
│ ├── test_routes.py # Tests for API endpoints
├── requirements/
| |── dev.txt # Development dependencies
| |── prod.txt # Production dependencies
├── .env # Environment variables
├── run.py # Entry point to run the app
```

## Docker Quickstart

This app can be run completely using `Docker` and `docker compose`. **Using Docker is recommended, as it guarantees the application is run using compatible versions of Python and Node**.

Step 1: Please copy .env.exmaple to .env in the same folder before build docker

Step 2: Build Docker

```bash
docker compose build
```

If build image with tag, please add argument

```bash
docker build -t <<image_name>> --build-arg INSTALL_PYTHON_VERSION=3.12.8 .
```

Step 3: Run Docker service
There are three main services:

To run the development version of the app

```bash
docker compose up flask-dev
```

To run the production version of the app

```bash
docker compose up flask-prod
```

The list of `environment:` variables in the `docker compose.yml` file takes precedence over any variables specified in `.env`.

To run any commands using the `Flask CLI`

```bash
docker compose run --rm manage <<COMMAND>>
```

Therefore, to initialize a database you would run
Only init if there is no migrations/versions. Migrate when there is changes in model, and upgrade to create db and tables

```bash
docker compose run --rm manage db init
docker compose run --rm manage db migrate
docker compose run --rm manage db upgrade
```

To seed the database do --user <number> --recipes <number>

```bash
docker compose run --rm manage seed --users 10
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
```

## Shell

To open the interactive shell, run

```bash
docker compose run --rm manage shell

```

By default, you will have access to the flask `app`.

## Running Tests/Linter

To run all tests, run

```bash
docker compose run --rm manage test
```

To run the linter, run

```bash
docker compose run --rm manage lint
```

The `lint` command will attempt to fix any linting/style errors in the code. If you only want to know if the code will pass CI and do not wish for the linter to make changes, add the `--check` argument.

## Migrations

Whenever a database migration needs to be made. Run the following commands

```bash
docker compose run --rm manage db migrate
```

This will generate a new migration script. Then run

```bash
docker compose run --rm manage db upgrade
```

To apply the migration.

For a full migration command reference, run `docker compose run --rm manage db --help`.

If you will deploy your application remotely (e.g on Heroku) you should add the `migrations` folder to version control.
You can do this after `flask db migrate` by running the following commands

```bash
git add migrations/*
git commit -m "Add migrations"
```

Make sure folder `migrations/versions` is not empty.

To access running project localhost:5000
access swagger at localhost:5000/apidocs

## Relevance Docs

Flasgger: https://github.com/flasgger/flasgger?tab=readme-ov-file#using-marshmallow-schemas
Marshmallow: https://flask-marshmallow.readthedocs.io/en/latest/ https://marshmallow-sqlalchemy.readthedocs.io/en/latest/

Flask Migrate: https://flask-migrate.readthedocs.io/en/latest/

Precommit CI: https://pre-commit.ci/
