# Milestone 6 and 7 - Kubernetes Setup and Deployment

## Overview
Three-node Kubernetes cluster using Minikube for the Student REST API
production environment with HashiCorp Vault and External Secrets Operator.

## Cluster Architecture
| Node | Name | Label | Purpose |
|------|------|-------|---------|
| Node A | prod-cluster | type=application | REST API pods |
| Node B | prod-cluster-m02 | type=database | PostgreSQL database |
| Node C | prod-cluster-m03 | type=dependent_services | Vault, ESO |

## Prerequisites
- Minikube
- kubectl
- Helm
- Docker Desktop

## Milestone 6 - Cluster Setup

### Start the Cluster
minikube start --nodes 3 --driver docker --cpus 2 --memory 2048 --profile prod-cluster

### Label the Nodes
kubectl label node prod-cluster type=application
kubectl label node prod-cluster-m02 type=database
kubectl label node prod-cluster-m03 type=dependent_services

### Verify Nodes
kubectl get nodes -L type

### Or Run the Setup Script
bash k8s/setup-cluster.sh

## Milestone 7 - Deploy on Kubernetes

### Step 1: Install Vault
helm install vault hashicorp/vault --namespace vault --set server.nodeSelector.type=dependent_services --set injector.enabled=false --set server.dev.enabled=true

### Step 2: Install External Secrets Operator
helm install external-secrets external-secrets/external-secrets --namespace external-secrets --set nodeSelector.type=dependent_services --set installCRDs=true

### Step 3: Configure Vault
kubectl exec -it vault-0 -n vault -- vault kv put secret/student-api db_password="postgres" secret_key="your-secret-key" db_url="postgresql://postgres:postgres@postgres-service.student-api.svc.cluster.local:5432/student_db"
kubectl create secret generic vault-token --from-literal=token=root -n student-api

### Step 4: Deploy Manifests
kubectl apply -f k8s/database.yaml
kubectl apply -f k8s/external-secrets.yaml
kubectl apply -f k8s/secret-store.yaml
kubectl apply -f k8s/application.yaml

### Step 5: Verify Pods
kubectl get pods -n student-api
kubectl get pods -n vault
kubectl get pods -n external-secrets

### Step 6: Access the API
minikube service student-api-service -n student-api -p prod-cluster --url

## Files
| File | Description |
|------|-------------|
| setup-cluster.sh | Script to spin up cluster and label nodes |
| application.yaml | ConfigMap, ExternalSecret, Deployment, Service for API |
| database.yaml | ConfigMap, PVC, Deployment, Service for PostgreSQL |
| external-secrets.yaml | Namespace and ServiceAccount for ESO |
| secret-store.yaml | SecretStore connecting ESO to Vault |
| vault.yaml | Vault namespace |

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/healthcheck | Health check |
| GET | /api/v1/students | Get all students |
| POST | /api/v1/students | Create a student |
| GET | /api/v1/students/:id | Get student by ID |
| PUT | /api/v1/students/:id | Update student |
| DELETE | /api/v1/students/:id | Delete student |

## Secrets Management
- Secrets stored in HashiCorp Vault at path secret/student-api
- External Secrets Operator syncs secrets from Vault to Kubernetes
- SecretStore vault-backend connects ESO to Vault using token auth
- db-credentials secret automatically created in student-api namespace
