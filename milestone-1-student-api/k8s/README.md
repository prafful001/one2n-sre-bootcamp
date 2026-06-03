# Milestone 6, 7, 8 and 9 - Kubernetes Setup, Helm Charts and ArgoCD

## Overview
Three-node Kubernetes cluster using Minikube for the Student REST API
production environment with HashiCorp Vault, External Secrets Operator,
Helm Charts and ArgoCD for GitOps-based deployments.

## Cluster Architecture
| Node | Name | Label | Purpose |
|------|------|-------|---------|
| Node A | prod-cluster | type=application | REST API pods |
| Node B | prod-cluster-m02 | type=database | PostgreSQL database |
| Node C | prod-cluster-m03 | type=dependent_services | Vault, ESO, ArgoCD |

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

## Milestone 9 - GitOps with ArgoCD

### Step 1: Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --server-side
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/crds/applicationset-crd.yaml --server-side

### Step 2: Wait for ArgoCD pods to be ready
kubectl get pods -n argocd

### Step 3: Set nodeSelector for ArgoCD pods on Node C
kubectl patch deployment argocd-server -n argocd --type merge --patch-file node-selector-patch.json
kubectl patch deployment argocd-repo-server -n argocd --type merge --patch-file node-selector-patch.json
kubectl patch deployment argocd-dex-server -n argocd --type merge --patch-file node-selector-patch.json
kubectl patch deployment argocd-applicationset-controller -n argocd --type merge --patch-file node-selector-patch.json
kubectl patch deployment argocd-notifications-controller -n argocd --type merge --patch-file node-selector-patch.json
kubectl patch deployment argocd-redis -n argocd --type merge --patch-file node-selector-patch.json
kubectl patch statefulset argocd-application-controller -n argocd --type merge --patch-file node-selector-patch.json

### Step 4: Get ArgoCD Admin Password
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d

### Step 5: Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
Open https://localhost:8080
Username: admin
Password: from Step 4

### Step 6: Apply ArgoCD Manifests Declaratively
kubectl apply -f argocd/projects/student-api-project.yaml
kubectl apply -f argocd/apps/secret-store-app.yaml
kubectl apply -f argocd/apps/postgres-app.yaml
kubectl apply -f argocd/apps/student-api-app.yaml

### Step 7: Verify ArgoCD Apps
kubectl get applications -n argocd

## ArgoCD Directory Structure
argocd/
- install/argocd-install.yaml     ArgoCD namespace and config
- projects/student-api-project.yaml  ArgoCD AppProject
- apps/student-api-app.yaml       ArgoCD Application for API
- apps/postgres-app.yaml          ArgoCD Application for PostgreSQL
- apps/secret-store-app.yaml      ArgoCD Application for SecretStore

## How GitOps Works
1. Developer pushes code to GitHub
2. GitHub Actions runs tests, builds Docker image with git SHA tag
3. GitHub Actions updates image tag in helm/student-api/values.yaml
4. GitHub Actions commits and pushes the updated values.yaml
5. ArgoCD detects the change in GitHub
6. ArgoCD auto-syncs and deploys new version to Kubernetes

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
