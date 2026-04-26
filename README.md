# Deploy Tracker
Deploy monitoring dashboard with observability.

An application that logs and monitors application deployments. Once an app is deployed, Deploy Tracker collects metrics, displays the status, shows logs, and triggers alerts if downtime occurs.

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- Celery
- Prometheus
- Grafana
- Docker Compose
- GitHub Actions
- Nginx

## Roadmap

- [x] Week 1: FastAPI + PostgreSQL (API core + database)
- [x] Week 2: Redis (caching layer)
- [x] Week 3: Celery/ARQ (async workers + health checks)
- [x] Week 4: Prometheus (metrics collection)
- [x] Week 5: Grafana (monitoring dashboards)
- [x] Week 6: GitHub Actions (CI/CD pipeline)
- [x] Week 7: Nginx (reverse proxy) + Docker Compose (full orchestration)
- [ ] Week 8: README polish, tests, final refinements

## Architecture
![Architecture Diagram](docs/architecture.png)

## Monitoring Dashboard
![Grafana Dashboard](docs/grafana-dashboard.png)

## How to Run

### Prerequisites
- Docker
- Docker Compose

### Setup
1. Clone the repository  
`git clone https://github.com/MuriloCosta29/deploy-tracker.git` 

2. Enter in folder  
`cd deploy-tracker`  

3. Start all services  
`docker compose up --build`  

4. Access the services  

- **API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)
- **Nginx:** http://localhost


5. Create an application to monitor  
- Open Swagger at http://localhost:8000/docs
- POST /applications with a name and URL (e.g., https://google.com)
- Health checks will run automatically every 30 seconds

6. Stop all services  
`docker compose down`
