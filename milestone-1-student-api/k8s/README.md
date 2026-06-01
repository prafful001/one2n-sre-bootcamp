# Milestone 6, 7 and 8 - Kubernetes Setup, Deployment and Helm Charts

## Overview
Three-node Kubernetes cluster using Minikube for the Student REST API
production environment with HashiCorp Vault and External Secrets Operator.
From Milestone 8 onwards, Helm charts are used for all deployments.

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
minikube start --nodes 3 --driver docker --cpus 2 --memory 2048 --profile prod-cluster
kubectl label node prod-cluster type=application
kubectl label node prod-cluster-m02 type=database
kubectl label node prod-cluster-m03 type=dependent_services

## Milestone 7 - Deploy using K8s Manifests
kubectl apply -f k8s/database.yaml
kubectl apply -f k8s/external-secrets.yaml
kubectl apply -f k8s/secret-store.yaml
kubectl apply -f k8s/application.yaml

## Milestone 8 - Deploy using Helm Charts

### Step 1: Add Helm Repos
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

### Step 2: Install Vault
helm upgrade --install vault helm/vault --namespace vault --create-namespace

### Step 3: Install External Secrets Operator
helm upgrade --install external-secrets external-secrets/external-secrets --namespace external-secrets --create-namespace --set installCRDs=true --set nodeSelector.type=dependent_services

### Step 4: Configure Vault
kubectl exec -it vault-0 -n vault -- vault kv put secret/student-api db_password="postgres" secret_key="your-secret-key" db_url="postgresql://postgres:postgres@postgres-service.student-api.svc.cluster.local:5432/student_db"
kubectl create secret generic vault-token --from-literal=token=root -n student-api

### Step 5: Install Secret Store
helm upgrade --install secret-store helm/secret-store --namespace student-api --create-namespace

### Step 6: Install PostgreSQL
helm upgrade --install postgres helm/postgres --namespace student-api

### Step 7: Install Student API
helm upgrade --install student-api helm/student-api --namespace student-api

### Step 8: Verify Everything
helm list -A
kubectl get pods -n student-api
kubectl get pods -n vault
kubectl get pods -n external-secrets

### Step 9: Access the API
minikube service student-api-service -n student-api -p prod-cluster --url

## Helm Charts Structure
| Chart | Description |
|-------|-------------|
| helm/student-api | REST API deployment, service, configmap, externalsecret |
| helm/postgres | PostgreSQL deployment, service, PVC |
| helm/vault | Wrapper chart for HashiCorp Vault |
| helm/external-secrets | Wrapper chart for External Secrets Operator |
| helm/secret-store | SecretStore and vault-token secret |

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/healthcheck | Health check |
| GET | /api/v1/students | Get all students |
| POST | /api/v1/students | Create a student |
| GET | /api/v1/students/:id | Get student by ID |
| PUT | /api/v1/students/:id | Update student |
| DELETE | /api/v1/students/:id | Delete student |
