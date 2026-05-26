Set-Content -Path C:\Users\KIIT\one2n-sre-bootcamp\milestone-1-student-api\k8s\README.md -Encoding UTF8 -Value @"
# Milestone 6 - Kubernetes Cluster Setup

## Overview
Three-node Kubernetes cluster using Minikube for the Student REST API production environment.

## Cluster Architecture
| Node | Name | Label | Purpose |
|------|------|-------|---------|
| Node A | prod-cluster | type=application | REST API pods |
| Node B | prod-cluster-m02 | type=database | PostgreSQL database |
| Node C | prod-cluster-m03 | type=dependent_services | Observability, Vault etc. |

## Prerequisites
- Minikube
- kubectl
- Docker Desktop

## Setup

### Start the Cluster
```bash
minikube start --nodes 3 --driver docker --cpus 2 --memory 2048 --profile prod-cluster
```

### Label the Nodes
```bash
kubectl label node prod-cluster type=application
kubectl label node prod-cluster-m02 type=database
kubectl label node prod-cluster-m03 type=dependent_services
```

### Verify Nodes
```bash
kubectl get nodes -L type
```

### Or Run the Setup Script
```bash
bash k8s/setup-cluster.sh
```

## Deploy the Application

### Apply Kubernetes Manifests
```bash
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml
```

### Verify Pods are Running
```bash
kubectl get pods
```

### Access the API
```bash
minikube service student-api-service -p prod-cluster --url
```

## Files
| File | Description |
|------|-------------|
| setup-cluster.sh | Script to spin up cluster and label nodes |
| secret.yaml | Database and app secrets |
| configmap.yaml | Application configuration |
| db-deployment.yaml | PostgreSQL deployment and service |
| api-deployment.yaml | Student API deployment (2 replicas) |
| api-service.yaml | NodePort service for external access |

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/students | Get all students |
| POST | /api/v1/students | Create a student |
| GET | /api/v1/students/:id | Get student by ID |
| PUT | /api/v1/students/:id | Update student |
| DELETE | /api/v1/students/:id | Delete student |
"@