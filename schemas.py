# NOTE: Define the shape of data the client sends and receives. Uses Pydantic to validate request bodies before they reach the database.
from pydantic import BaseModel


class ApplicationItem(BaseModel):  # This schema defines what the client sends.
    name: str
    url: str


class DeployItem(BaseModel):
    version: str
    status: bool
    application_id: int
