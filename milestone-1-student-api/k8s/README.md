# Milestones 6-10 - Kubernetes, Helm, ArgoCD and Observability

## Overview
Three-node Kubernetes cluster with full observability stack.

## Cluster Architecture
| Node | Name | Label | Purpose |
|------|------|-------|---------|
| Node A | prod-cluster | type=application | REST API |
| Node B | prod-cluster-m02 | type=database | PostgreSQL |
| Node C | prod-cluster-m03 | type=dependent_services | Vault, ESO, ArgoCD, Observability |

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
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo add external-secrets https://charts.external-secrets.io
helm repo update
helm upgrade --install vault helm/vault --namespace vault --create-namespace
helm upgrade --install external-secrets external-secrets/external-secrets --namespace external-secrets --create-namespace --set installCRDs=true
kubectl exec -it vault-0 -n vault -- vault kv put secret/student-api db_password="postgres" secret_key="your-secret-key" db_url="postgresql://postgres:postgres@postgres-service.student-api.svc.cluster.local:5432/student_db"
kubectl create secret generic vault-token --from-literal=token=root -n student-api
helm upgrade --install secret-store helm/secret-store --namespace student-api --create-namespace
helm upgrade --install postgres helm/postgres --namespace student-api
helm upgrade --install student-api helm/student-api --namespace student-api

## Milestone 9 - GitOps with ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --server-side
kubectl apply -f argocd/projects/student-api-project.yaml
kubectl apply -f argocd/apps/secret-store-app.yaml
kubectl apply -f argocd/apps/postgres-app.yaml
kubectl apply -f argocd/apps/student-api-app.yaml
kubectl apply -f argocd/apps/observability-app.yaml

### Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
Open https://localhost:8080

## Milestone 10 - Observability Stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm dependency update helm/observability
helm upgrade --install observability helm/observability --namespace observability --create-namespace --timeout 10m

### Note for Minikube
After first install, fix Loki storage permissions on the node:
minikube ssh -p prod-cluster -n prod-cluster-m03 -- "sudo find /tmp/hostpath-provisioner/observability -type d -exec chmod 777 {} \;"
kubectl delete pod observability-loki-0 -n observability

### Access Grafana
minikube service observability-grafana -n observability -p prod-cluster --url
Username: admin
Password: admin123

### What's Monitored
- REST API endpoints (latency, uptime) via Blackbox Exporter
- ArgoCD server uptime via Blackbox Exporter
- HashiCorp Vault uptime via Blackbox Exporter
- PostgreSQL metrics via Prometheus Postgres Exporter
- Node metrics via Node Exporter
- Kubernetes metrics via kube-state-metrics
- Application logs via Promtail to Loki

### Verify in Grafana
1. Connections -> Data Sources: confirm Prometheus and Loki present
2. Explore -> Loki -> Code: query {app="student-api"} for application logs
3. Explore -> Prometheus: query probe_success{job="blackbox-argocd"} for uptime

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/healthcheck | Health check |
| GET | /api/v1/students | Get all students |
| POST | /api/v1/students | Create a student |
| GET | /api/v1/students/:id | Get student by ID |
| PUT | /api/v1/students/:id | Update student |
| DELETE | /api/v1/students/:id | Delete student |
