# siera-api-example

This example demonstrates how to process articles (texts) using the Siera API.

### To install:

For this example we recommend using Python 3.9 and pipenv

1. Clone this repo:

```
$ git clone https://github.com/Commetric/siera-api-example.git
```

2. Install Python packages:

In a virtual environment using pipenv:

```
$ pipenv install
```

OR using pip directly:

```
$ pip install -r requirements.txt
```

3. Set environment variables in .env (initially copy .env.template into .env)

### To run:

In a virtual environment using pipenv:

```
$ pipenv run python process_articles.py
```

OR directly:

```
$ python process_articles.py
```

### Next steps:

The get_articles method is just a placeholder and should be replaced, normally with code that selects articles from a database.
