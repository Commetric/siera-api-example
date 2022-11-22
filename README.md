# siera-api-example

This example demonstrates how to process articles (texts) using the Siera API. 

### To install:

This example uses Python 3.9 and pipenv

1. Clone this repo:

```
$ git clone https://github.com/Commetric/siera-api-example.git
```

2. Install Python packages ( in a virtual environment ):

```
$ pipenv install
```

3. Set environment variables in .env (initially copy .env.template to .env)

### To run:

```
$ pipenv run python process_articles.py
```

### Next steps:

The get_articles method is just a placeholder and should be replaced, normally with code that selects articles from a database.
