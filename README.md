# one2n SRE Bootcamp — Student CRUD REST API

A RESTful API built with Python and Flask to manage student records.
Built as part of the One2N SRE Bootcamp — Milestones 1 through 11.

---

## Tech Stack

- Python 3.11
- Flask
- PostgreSQL
- Flask-SQLAlchemy
- Flask-Migrate
- Pytest
- Docker
- Docker Compose
- Vagrant + VirtualBox
- Nginx
- Kubernetes
- Helm
- ArgoCD
- HashiCorp Vault
- External Secrets Operator
- Prometheus
- Grafana
- Loki + Promtail
- Blackbox Exporter
- Postgres Exporter
- GitHub Actions (self-hosted runner)

---

## Prerequisites

- Python 3.11+
- PostgreSQL
- Git
- Docker
- Docker Compose
- make
- kubectl
- Helm 3+
- Vagrant + VirtualBox (Milestone 5)
- A running Kubernetes cluster (Milestones 6+)
- ArgoCD CLI (Milestone 9)

---

## Milestone 1 — REST API

**Folder:** `milestone-1-rest-api/`

A RESTful CRUD API to manage student records using Python 3.11, Flask, and PostgreSQL with Alembic-based migrations and a Pytest test suite.

### Local Setup (Without Docker)

1. Clone the repository

```
git clone https://github.com/prafful001/one2n-sre-bootcamp.git
cd one2n-sre-bootcamp/milestone-1-rest-api
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

Edit `.env` with your database credentials.

5. Run database migrations

```
make migrate
```

6. Start the server

```
make run
```

Server runs at http://localhost:5000

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/healthcheck | Health check |
| POST | /api/v1/students | Add new student |
| GET | /api/v1/students | Get all students |
| GET | /api/v1/students/{id} | Get student by ID |
| PUT | /api/v1/students/{id} | Update student |
| DELETE | /api/v1/students/{id} | Delete student |

### Running Tests

```
make test
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection URL |
| FLASK_APP | Flask app module |
| FLASK_ENV | Environment (development/production) |
| SECRET_KEY | App secret key |
| PORT | Port to run on |

### Make Targets

| Command | Description |
|---------|-------------|
| make install | Install Python dependencies |
| make run | Run API locally without Docker |
| make test | Run Pytest test suite |
| make migrate | Run Alembic DB migrations |

---

## Milestone 2 — Containerise REST API

**Folder:** `milestone-2-containerise/`

Containerised the Flask API using a multi-stage Docker build to produce a minimal, production-ready image.

### Build Image

```
docker build -t student-api:1.0.0 .
```

### Run Container

```
docker run -p 5000:5000 -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/student_db -e FLASK_APP=app -e FLASK_ENV=development -e SECRET_KEY=your-secret-key student-api:1.0.0
```

### Tag and Push to Docker Hub

```
docker tag student-api:1.0.0 <your-dockerhub-username>/student-api:1.0.0
docker push <your-dockerhub-username>/student-api:1.0.0
```

### Image Details

- Base image: `python:3.11-slim`
- Multi-stage build to reduce final image size
- Only production dependencies in final image
- Environment variables injected at runtime
- Never hardcoded in image
- Image versioning follows semver (`1.0.0`)

### .dockerignore

The following are excluded from the Docker build context:

- `venv/`
- `__pycache__/`
- `.env`
- `.pytest_cache/`
- `*.pyc`

---

## Milestone 3 — One-Click Local Setup

**Folder:** `milestone-3-local-dev-setup/`

Complete local development environment using Docker Compose. Spins up the API and PostgreSQL with a single command and runs migrations automatically.

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

### Make Targets

| Command | Description |
|---------|-------------|
| make install | Install dependencies |
| make run | Run API locally |
| make test | Run unit tests |
| make migrate | Run DB migrations |
| make docker-build | Build Docker image |
| make docker-run | Run API Docker container |
| make start-db | Start PostgreSQL container |
| make start-api | Start everything with one command |
| make stop-db | Stop all containers |

### Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| api | 5000 | Flask REST API |
| db | 5432 | PostgreSQL database |

---

## Milestone 4 — CI Pipeline

**Folder:** `milestone-4-ci-pipeline/`

Automated CI pipeline using GitHub Actions with a self-hosted runner. Triggered on every push and pull request to `main`.

### Pipeline Triggers

```
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

### Pipeline Steps

1. Checkout code
2. Set up Python 3.11
3. Install dependencies (`make install`)
4. Run linting with flake8 and isort
5. Run tests with pytest (`make test`)
6. Build Docker image
7. Push image to Docker Hub (on push to main only)

### Self-Hosted Runner Setup

1. Go to GitHub repo Settings → Actions → Runners
2. Click **New self-hosted runner**
3. Follow the setup instructions for your OS
4. Start the runner:

```
./run.sh
```

### Run Linting Locally

```
flake8 .
isort --check-only .
```

Fix isort issues automatically:

```
isort .
```

---

## Milestone 5 — Bare Metal Deployment

**Folder:** `milestone-5-bare-metal-deploy/`

Deploy the Student API on a Linux VM provisioned with Vagrant, using Nginx as a reverse proxy and Docker Compose to run the services inside the VM.

### Start the VM

```
vagrant up
```

### SSH into the VM

```
vagrant ssh
```

### Run Setup Script (inside VM)

```
bash setup.sh
```

This will automatically:
1. Install Docker and Docker Compose on the VM
2. Copy application files to the VM
3. Start PostgreSQL and API containers via Docker Compose
4. Configure and start Nginx as a reverse proxy

### Check VM Status

```
vagrant status
```

### Stop the VM

```
vagrant halt
```

### Destroy the VM

```
vagrant destroy
```

### Nginx Configuration

Nginx config is at `nginx/nginx.conf`:

- Listens on port `80`
- Forwards all traffic to the API on port `5000`
- Sets correct proxy headers

### Access the API

Once the VM is running and setup is complete:

```
http://<VM-IP>/api/v1/healthcheck
```

---

## Milestone 6 — Kubernetes Cluster Setup

**Folder:** `milestone-6-k8s-cluster/`

Set up a local Kubernetes cluster ready for application deployments.

### Bootstrap the Cluster

```
bash cluster.sh
```

This will:
1. Initialise the Kubernetes control plane
2. Apply CNI networking plugin
3. Set up namespaces
4. Configure kubectl context

### Verify the Cluster

```
kubectl get nodes
```

```
kubectl get namespaces
```

```
kubectl cluster-info
```

### Create Application Namespace

```
kubectl create namespace student-api
```

### Set Default Namespace

```
kubectl config set-context --current --namespace=student-api
```

---

## Milestone 7 — Deploy REST API on Kubernetes

**Folder:** `milestone-7-k8s-deploy/`

Deploy the Student API and PostgreSQL on Kubernetes using raw manifests. Includes HashiCorp Vault for secrets management and External Secrets Operator to sync secrets into the cluster.

### Apply All Manifests

```
kubectl apply -f k8s/
```

### Apply in Order (Manual)

```
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/database.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/vault.yaml
kubectl apply -f k8s/secret-store.yaml
kubectl apply -f k8s/external-secrets.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml
```

### Check Deployment Status

```
kubectl get pods -n student-api
kubectl get services -n student-api
kubectl get configmaps -n student-api
kubectl get externalsecrets -n student-api
```

### View API Logs

```
kubectl logs -f deployment/student-api -n student-api
```

### Port Forward to Access API Locally

```
kubectl port-forward svc/student-api 5000:5000 -n student-api
```

API available at http://localhost:5000

### Manifests

| File | Description |
|------|-------------|
| api-deployment.yaml | Flask API Deployment |
| api-service.yaml | Flask API Service |
| db-deployment.yaml | PostgreSQL Deployment |
| database.yaml | PostgreSQL Service and PVC |
| configmap.yaml | App environment config |
| secret.yaml | Kubernetes Secret |
| external-secrets.yaml | ExternalSecret resource |
| secret-store.yaml | Vault SecretStore |
| vault.yaml | Vault configuration |
| application.yaml | ArgoCD Application manifest |
| setup-cluster.sh | Cluster setup helper script |

---

## Milestone 8 — Helm Charts

**Folder:** `milestone-8-helm-charts/`

All Kubernetes resources packaged as Helm charts for reusable, parameterised, and versioned deployments.

### Install All Charts

```
helm install vault ./vault -n student-api
helm install external-secrets ./external-secrets -n student-api
helm install secret-store ./secret-store -n student-api
helm install postgres ./postgres -n student-api
helm install student-api ./student-api -n student-api
```

### Upgrade a Chart

```
helm upgrade student-api ./student-api -n student-api
```

### Uninstall a Chart

```
helm uninstall student-api -n student-api
```

### List Installed Releases

```
helm list -n student-api
```

### Render Templates Without Installing (Dry Run)

```
helm template student-api ./student-api
```

### Override Values at Install Time

```
helm install student-api ./student-api \
  --set image.tag=2.0.0 \
  --set service.port=8080 \
  -n student-api
```

### Charts

| Chart | Description |
|-------|-------------|
| student-api | Flask API Deployment, Service, ConfigMap, ExternalSecret |
| postgres | PostgreSQL Deployment, Service, PersistentVolumeClaim |
| vault | HashiCorp Vault (upstream chart with custom values) |
| external-secrets | External Secrets Operator |
| secret-store | Vault SecretStore and Vault token Secret |

### Vault Policy

Vault policy for the student-api is defined in `policy.hcl`. Apply it with:

```
vault policy write student-api policy.hcl
```

---

## Milestone 9 — ArgoCD (GitOps)

**Folder:** `milestone-9-argocd/`

GitOps-based continuous deployment using ArgoCD. All application state is declared in Git and ArgoCD syncs it automatically to the cluster. No manual kubectl apply needed after setup.

### Install ArgoCD

```
kubectl apply -f install/argocd-install.yaml
```

### Wait for ArgoCD to be Ready

```
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=120s
```

### Access ArgoCD UI

```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open https://localhost:8080

### Get Initial Admin Password

```
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

### Login via CLI

```
argocd login localhost:8080
```

### Apply ArgoCD Project

```
kubectl apply -f projects/student-api-project.yaml
```

### Apply All Applications

```
kubectl apply -f apps/
```

### Sync an Application Manually

```
argocd app sync student-api
```

### Check Application Status

```
argocd app list
argocd app get student-api
```

### Applications

| File | Description |
|------|-------------|
| apps/student-api-app.yaml | Deploys Student API via Helm chart |
| apps/postgres-app.yaml | Deploys PostgreSQL via Helm chart |
| apps/secret-store-app.yaml | Deploys Vault SecretStore via Helm chart |
| apps/observability-app.yaml | Deploys observability stack via Helm chart |

### How GitOps Works Here

1. Code or config is pushed to this Git repository
2. ArgoCD detects the change (polls every 3 minutes or via webhook)
3. ArgoCD compares the live cluster state with the desired state in Git
4. If there is a diff, ArgoCD syncs the cluster to match Git
5. No manual deployments needed

---

## Milestone 10 — Observability Stack

**Folder:** `milestone-10-observability/`

Full observability stack deployed as a single Helm umbrella chart. Covers metrics collection, log aggregation, endpoint probing, and visualisation.

### Update Chart Dependencies

```
helm dependency update ./helm
```

### Install Observability Stack

```
helm install observability ./helm -n monitoring --create-namespace
```

### Upgrade

```
helm upgrade observability ./helm -n monitoring
```

### Uninstall

```
helm uninstall observability -n monitoring
```

### Access Grafana

```
kubectl port-forward svc/observability-grafana 3000:3000 -n monitoring
```

Open http://localhost:3000

Default credentials:
- Username: `admin`
- Password: `prom-operator`

### Access Prometheus

```
kubectl port-forward svc/observability-kube-prometheus-prometheus 9090:9090 -n monitoring
```

Open http://localhost:9090

### Access Alertmanager

```
kubectl port-forward svc/observability-kube-prometheus-alertmanager 9093:9093 -n monitoring
```

Open http://localhost:9093

### Check All Pods

```
kubectl get pods -n monitoring
```

### Components

| Component | Description |
|-----------|-------------|
| kube-prometheus-stack | Prometheus, Grafana, Alertmanager, node-exporter, kube-state-metrics |
| Loki | Log aggregation backend |
| Promtail | Log shipping DaemonSet running on every node |
| Blackbox Exporter | HTTP and TCP endpoint probing |
| Prometheus Postgres Exporter | PostgreSQL metrics for Prometheus |

### Chart Dependencies

| Chart | Version | Repository |
|-------|---------|------------|
| kube-prometheus-stack | 61.3.2 | prometheus-community |
| loki | 6.6.2 | grafana |
| promtail | 6.16.4 | grafana |
| prometheus-blackbox-exporter | 9.0.0 | prometheus-community |
| prometheus-postgres-exporter | 6.3.0 | prometheus-community |

---

## Milestone 11 — Grafana Dashboards and Alerts

**Folder:** `milestone-11-dashboards-alerts/`

Grafana dashboards provisioned as Kubernetes ConfigMaps. They are version-controlled in Git and automatically loaded by the Grafana sidecar — no manual dashboard imports needed.

### Apply All Dashboards

```
kubectl apply -f dashboards/ -n monitoring
```

### Verify Dashboards are Loaded

```
kubectl get configmaps -n monitoring | grep dashboard
```

### Check Grafana Sidecar Logs (if dashboards not appearing)

```
kubectl logs -f deployment/observability-grafana -c grafana-sc-dashboard -n monitoring
```

### Port Forward to View in Browser

```
kubectl port-forward svc/observability-grafana 3000:3000 -n monitoring
```

Open http://localhost:3000 and go to **Dashboards** in the left sidebar.

### Dashboards

| File | Panels Included |
|------|----------------|
| dashboard-node-exporter.yaml | CPU usage, memory usage, disk I/O, network traffic per node |
| dashboard-kube-state-metrics.yaml | Deployment replicas, Pod restarts, ReplicaSet health |
| dashboard-postgres.yaml | Active connections, query duration, cache hit ratio, transactions |
| dashboard-loki-logs.yaml | Log volume over time, error rate, log stream explorer |
| dashboard-blackbox.yaml | HTTP probe success rate, SSL certificate expiry, response latency |

### How Dashboard Provisioning Works

1. Each file is a Kubernetes ConfigMap containing the full Grafana dashboard JSON
2. ConfigMaps are labelled with `grafana_dashboard: "1"`
3. The Grafana sidecar container watches for ConfigMaps with this label across all namespaces
4. When a ConfigMap is created or updated, the sidecar picks it up and loads the dashboard into Grafana automatically
5. No Grafana restart is needed

---

## Progress

| Milestone | Description | Status |
|-----------|-------------|--------|
| 1 | REST API | ✅ Complete |
| 2 | Containerise REST API | ✅ Complete |
| 3 | One-click local setup | ✅ Complete |
| 4 | CI Pipeline | ✅ Complete |
| 5 | Bare metal deployment | ✅ Complete |
| 6 | Kubernetes cluster setup | ✅ Complete |
| 7 | Deploy on Kubernetes | ✅ Complete |
| 8 | Helm charts | ✅ Complete |
| 9 | ArgoCD | ✅ Complete |
| 10 | Observability stack | ✅ Complete |
| 11 | Dashboards and Alerts | ✅ Complete |
