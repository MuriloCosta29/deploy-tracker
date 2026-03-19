# NOTE: Entry point of application. Creates the FastAPI and connects all routers.

from fastapi import FastAPI
from routes.applications import router as applications_router
from routes.deploys import router as deploys_router

# NOTE: `as` set a nickname for import

# -------------------------------------------------------------------------------
app = FastAPI()
app.include_router(applications_router)
app.include_router(deploys_router)
# -------------------------------------------------------------------------------


@app.get("/")
def health_check():
    return {"status": "The app in main.py is working"}
