# NOTE: Entry point of application. Creates the FastAPI and connects all routers.
# NOTE: `as` set a nickname for import
# ------------------------------------------------------------------------

from fastapi import FastAPI
from routes.applications import router as applications_router
from routes.deploys import router as deploys_router
from routes.health_checks import router as health_checks_router
from database import Base, engine

# ------------------------------------------------------------------------

app = FastAPI()
app.include_router(applications_router)
app.include_router(deploys_router)
app.include_router(health_checks_router)

# ------------------------------------------------------------------------

Base.metadata.create_all(
    bind=engine
)  # Creates the table in the database (not file! File is the SQLite. Now is database, only.)

# ------------------------------------------------------------------------


@app.get("/")
def health_check():
    return {"status": "The app in main.py is working"}
