# sps-python-microservices

Microservices solution built with Python

This is a microservices solution which is a simple Flask app that serves a Blog API. It is built with the following technologies:

- [Python](https://www.python.org/) - The programming language used
- [Flask](http://flask.pocoo.org/) - The web framework used

## Prerequisites

- Python 3.6 or higher

## Installing

- Clone the repository

### Local

- Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

- Set the environment variables.

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=1
```

- Run the app

```bash
flask run
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
