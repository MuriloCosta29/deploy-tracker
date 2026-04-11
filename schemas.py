# NOTE: Define the shape of data the client sends and receives. Uses Pydantic to validate request bodies before they reach the database.
#-------------------------------------------
from pydantic import BaseModel
from datetime import datetime

class ApplicationItem(BaseModel):  # This schema defines what the client sends.
    name: str
    url: str


class DeployItem(BaseModel):
    version: str
    status: bool
    application_id: int


class HealthCheck(BaseModel): # CORRECT ✅
    application_id: int
    status: bool
    response_time: float
    http_code: int
    created_at: datetime
