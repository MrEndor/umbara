# umbara

Umbara Project

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake-services.github.io)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
![workflow](https://github.com/MrEndor/umbara/actions/workflows/test.yml/badge.svg)

## Prerequisites

You will need:

- `python^3.11` (see `pyproject.toml` for full version)

## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`


## Quick start

Сheck your python version (should be 3.11)

1) Install poetry
```shell
pip install poetry
```
2) Choose poetry python version 3.11
```shell
poetry env use /full/path/to/python
```
3) Download all dependencies to mod dev
```shell
poetry install
```
If you only need dependencies for production, then
```shell
poetry install --only main
```

4) Before starting the project, you need to create an `.env` file in the directory `config` and fill 
it with the `.env.template` file in the same directory

5) Updating tables in a database
```shell
poetry run python manage.py migrate
```

6) Collect all statics in staticfiles
```shell
poetry run python manage.py collectstatic --noinput
```

7) Compile localization files
```shell
poetry run python manage.py compilemessages
```

8) Start django server
```shell
poetry run python manage.py runserver
```

### Optional
Create user for django admin\
`Attention`: This should be done after migrations
```shell
poetry run python manage.py createsuperuser
```

Running tests and coverage
```shell
poetry run pytest
```

Running Type Checker
```shell
poetry run mypy manage.py server
poetry run mypy tests
```

Running linter flake8
```shell
poetry run flake8 .
```

Compiling localization
```shell
poetry run python manage.py compilemessages
```
