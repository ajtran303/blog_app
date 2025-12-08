# TDD Python Flask Blog App

Test-driven development of a Python Flask blog app with pytest and pydantic

## Setup (Mac OS)

Start a virtual environment
```bash
python -p venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Initialize the database
```bash
python blog/init_db.py
```

Start the server in one terminal
```bash
FLASK_APP=blog/app.py python -m flask run
```

Run the tests in another terminal
```bash
python -m pytest tests
```

## TODO
- Automate setup and breakdown of database when testing so that the init_db script isn't needed

- Run Flask app as subprocess during test so that two terminals aren't needed to run tests
