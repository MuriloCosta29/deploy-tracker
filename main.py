# NOTE: Entry point of application. Creates the FastAPI and connects all routers.
# NOTE: `as` set a nickname for import
# -----------------------------------------------------------------------

import time
from fastapi import FastAPI, Request
from routes.applications import router as applications_router
from routes.deploys import router as deploys_router
from routes.health_checks import router as health_checks_router
from database import Base, engine
from prometheus_client import make_asgi_app
from metrics import REQUEST_COUNT, REQUEST_LATENCY

# -----------------------------------------------------------------------
# middleware (code that runs before and after every request).
# -----------------------------------------------------------------------

app = FastAPI()
app.include_router(applications_router)
app.include_router(deploys_router)
app.include_router(health_checks_router)
metrics_app = make_asgi_app()

# -----------------------------------------------------------------------


@app.middleware("http")
async def track_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    method = request.method
    status_code_str = str(response.status_code)
    endpoint = request.url.path
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code_str).inc()
    REQUEST_LATENCY.labels(
        method=method, endpoint=endpoint, status=status_code_str
    ).observe(process_time)
    return response


# ------------------------------------------------------------------------

Base.metadata.create_all(
    bind=engine
)  # Creates the table in the database (not file! File is the SQLite. Now is database, only.)

# ------------------------------------------------------------------------


@app.get("/")
def health_check():
    return {"status": "The app in main.py is working"}


app.mount("/metrics", metrics_app)
