# Milestone 5 - Deploy REST API on Bare Metal (Vagrant)

## Overview
Deploys the Student REST API and its dependent services on a Vagrant VM
using Docker Compose and Nginx as a load balancer.

## Architecture
- 2 API containers
- 1 PostgreSQL container
- 1 Nginx container (load balancer on port 8080)

## Prerequisites
- Vagrant
- VirtualBox
- Docker Desktop

## Setup

### Start the Vagrant Box
vagrant up

### SSH into the VM
vagrant ssh

### Deploy Everything
cd /opt/app
make deploy

### Stop Everything
make stop

## Nginx Load Balancing
- Nginx listens on port 8080
- Forwards requests to api1:5000 and api2:5000
- Round-robin load balancing between 2 API containers

## Make Targets
| Command | Description |
|---------|-------------|
| make deploy | Start all containers |
| make stop | Stop all containers |
| make restart | Restart all containers |
| make logs | View container logs |
| make clean | Remove all containers and images |

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/healthcheck | Health check |
| GET | /api/v1/students | Get all students |
| POST | /api/v1/students | Create a student |
| GET | /api/v1/students/:id | Get student by ID |
| PUT | /api/v1/students/:id | Update student |
| DELETE | /api/v1/students/:id | Delete student |

## Access the API
http://localhost:8080/api/v1/students
