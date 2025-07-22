# Elektroniczny Rejestr Członków 2 (Backend)

Tech stack: Python, Poetry, FastAPI, SQLModel, Alembic, Docker.

## Development

The project uses [Poetry](https://python-poetry.org) for dependency management.
It's best to [install it using the official installer](https://python-poetry.org/docs/#installing-with-the-official-installer).

Once Poetry is installed, `git clone` and `cd` into this repository.
Run `poetry install`. This will create a virtual environment in `.venv`
and install the project with its dependencies.

### VS Code Setup

Install the following extensions:
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  and [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
  (you probably have them already)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)

The provided `.vscode/settings.json` file tells VS Code to use the Black formatter for Python files
and enables formatting on save. Unless you have a good reason, keep those two settings.

Extensions also worth installing:
- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
  (if you ever need to edit `pyproject.toml`)

### Other editors

You're on your own. Try and get your IDE to use the Black formatter though.

### Running the Project

To avoid having to run a PostgreSQL instance yourself, use the provided Docker Compose configuration.
If you haven't already, [install Docker](https://docker.com).

To run the project (rebuilding the backend container) use:
```
docker compose up --build
```
This will start showing logs from both the backend and postgres containers. Ctrl-C to stop.

You can also run in detached mode:
```
docker compose up --build -d

# To view logs (Ctrl-C to stop following)
docker compose logs -f

# To shut down
docker compose down
```

In either case, the backend service will be exposed to `http://localhost:8000` and
the postgres database will be exposed on port 9876.

### Database Migrations

The project uses [Alembic](https://alembic.sqlalchemy.org) for managing database migrations.
Due to the Poetry setup, whenever Alembic docs refer to the `alembic` command instead
you should use `poetry run alembic`. This makes sure the command is run in the project's
virtual environment and that the `alembic` command will even be found.

For all the details, refer to Alembic documentation.
Specifically, the basics of creating and applying migrations are described
[here](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

**Note:** Most Alembic commands will fail if the compose stack is not running, as
the database won't be reachable. Make sure to run `docker compose up --build -d` first.
(Or `docker compose up --build` in another terminal.)
