# Deploy Tracker
Deploy monitoring dashboard with observability.

An application that logs and monitors application deployments. Once an app is deployed, Deploy Tracker collects metrics, displays the status, shows logs, and triggers alerts if downtime occurs.

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- Celery / ARQ
- Prometheus
- Grafana
- Docker Compose
- GitHub Actions
- Nginx

## Roadmap

- [ ] Week 1: FastAPI + PostgreSQL (API core + database)
- [ ] Week 2: Redis (caching layer)
- [ ] Week 3: Celery/ARQ (async workers + health checks)
- [ ] Week 4: Prometheus (metrics collection)
- [ ] Week 5: Grafana (monitoring dashboards)
- [ ] Week 6: GitHub Actions (CI/CD pipeline)
- [ ] Week 7: Nginx (reverse proxy) + Docker Compose (full orchestration)
- [ ] Week 8: README polish, tests, final refinements
