# django-media-guard

Serve private media through a Django application.

## Requirements

* Python >= 3.6
* Django >= 1.11, < 2.2

## Installation

```bash
  pip install --upgade pip
  pipenv install --dev
```

To be able to upload to pypi you need a .pypirc file, this can live in your home directory.
Example:
```
[distutils]
index-servers =
    sfd

[sfd]
repository: https://pypi.test.squirrel.rodeo/
username: [********]
password: [********]
```

## Usage

### To deploy to omni pypi
* Install twine
```bash
pip install twine
```
* Create a distribution
```bash
python setup.py sdist
```
* Use twine to push to omni pypi
```bash
twine upload -r sfd dist/*
```

## Development

```bash
pipenv install --dev
pre-commit install --hook-type pre-commit
pre-commit install --hook-type pre-push

pipenv shell
```

You can run the example application using the `manage.py` in the repo root.
