# Student CRUD REST API

A RESTful API built with Python and Flask to manage student records.
Built as part of the One2N SRE Bootcamp — Milestone 1, 2 and 3.

## Tech Stack

- Python 3.11
- Flask
- PostgreSQL
- Flask-SQLAlchemy
- Flask-Migrate
- Pytest
- Docker
- Docker Compose

## Prerequisites

- Python 3.11+
- PostgreSQL
- Git
- Docker
- Docker Compose
- make

## Local Setup (Without Docker)

1. Clone the repository

```
git clone https://github.com/prafful001/one2n-sre-bootcamp.git
cd one2n-sre-bootcamp/milestone-1-student-api
```

2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```
make install
```

4. Set up environment variables

```
cp .env.example .env
```

Edit .env with your database credentials.

5. Run database migrations

```
make migrate
```

6. Start the server

```
make run
```

Server runs at http://localhost:5000

## One-Click Local Setup (Docker Compose)

### Start Everything with One Command

```
make start-api
```

This will automatically:
1. Build the Docker image
2. Start PostgreSQL container
3. Run DB migrations
4. Start API container

Server runs at http://localhost:5000

### Order of Execution (Manual)

If you want to run step by step:

```
make start-db
make migrate
make docker-build
make start-api
```

### Stop Everything

```
make stop-db
```

## Make Targets

| Command | Description |
|---------|-------------|
| make install | Install dependencies |
| make run | Run API locally |
| make test | Run unit tests |
| make migrate | Run DB migrations |
| make docker-build | Build Docker image |
| make docker-run | Run API docker container |
| make start-db | Start DB container |
| make start-api | Start everything with one command |
| make stop-db | Stop all containers |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/healthcheck | Health check |
| POST | /api/v1/students | Add new student |
| GET | /api/v1/students | Get all students |
| GET | /api/v1/students/{id} | Get student by ID |
| PUT | /api/v1/students/{id} | Update student |
| DELETE | /api/v1/students/{id} | Delete student |

## Running Tests

```
make test
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection URL |
| FLASK_APP | Flask app module |
| FLASK_ENV | Environment |
| SECRET_KEY | App secret key |
| PORT | Port to run on |

## Docker

### Build Image

```
docker build -t student-api:1.0.0 .
```

### Run Container

```
docker run -p 5000:5000 -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/student_db -e FLASK_APP=app -e FLASK_ENV=development -e SECRET_KEY=your-secret-key student-api:1.0.0
```

### Image Details

- Base image: python:3.11-slim
- Multi-stage build to reduce image size
- Environment variables injected at runtime
- Never hardcoded in image
- Image versioning follows semver (1.0.0)