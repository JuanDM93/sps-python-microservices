# sps-python-microservices

Microservices solution built with Python

This is a microservices solution which is a simple Flask app that serves a Blog API. It is built with the following technologies:

- [Python](https://www.python.org/) - The programming language used
- [Flask](http://flask.pocoo.org/) - The web framework used
- [MongoDB](https://www.mongodb.com/) - The database used
- [Docker](https://www.docker.com/) - The containerization platform used

## Prerequisites

- Python 3.6 or higher
- MongoDB (optional)
- Docker (optional)

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
```

- For the DATABASE you can use a config.py file in the */instance* folder, follow the example in config-example.py provided at */docs*. Or you can set the MONGODB_URI environment variable.

```bash
export MONGODB_URI=mongodb://localhost:27017/flaskr
```

(if you are not using MongoDB locally you can use a remote MongoDB Atlas instance instead at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas))

- Run the app

```bash
flask run
```

### Dockerized

- Build the image

```bash
docker build -t flaskr .
```

- Run the container

```bash
docker run -p <port>:5000 -e "MONGODB_URI: <mongodb_uri>" flaskr
```

- Or use docker-compose

```bash
docker-compose up
```

## Resources

Resources are the main components of the application. All of them are accessible through the API endpoint.

### Index

The Index endpoint is the main endpoint of the application. It displays the API welcome message.

- GET / - Get the API welcome message

### API description endpoint

The documentation is available at the */spec* endpoint.

- GET /spec - Get the Swagger documentation (JSON)

### Healthcheck

The Healthcheck endpoint is a simple endpoint that returns the health of the API.

- GET /api/health - Get the health of the application

### Authentication

The Authentication endpoint is used to authenticate the user and get a token.

- POST /api/auth/register - Register a new user
- POST /api/auth/login - Login an existing user

### Blogs

The Blog endpoint is used to manage the blogs.

- Blog Model (BSON)
  - id: ObjectId
  - title: String
  - content: String

- GET /api/blogs - Get all the blogs
- POST /api/blogs - Create a new blog
- GET /api/blogs/{id} - Get a blog
- PUT /api/blogs/{id} - Update a blog
- DELETE /api/blogs/{id} - Delete a blog

## Acknowledgments

- Pokemon API - [https://pokeapi.co/](https://pokeapi.co/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
