# NOTE: All endpoints related to the /deploys resource.
# GET /deploys - List all
# GET /deploys/{id} - get one
# POST /deploys - create
# PATCH /deploys/{id} - edit
# DELETE /deploys/{id} - delete

# --------------------------------------------------------------------------------------------

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Deploy
from database import get_session
from schemas import DeployItem

# --------------------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------------------


@router.get("/deploys")
def list_deploys(db: Session = Depends(get_session)):
    deploys = db.query(Deploy).all()
    return deploys


# --------------------------------------------------------------------------------------------


@router.get("/deploys/{id}")
def one_deploy(id: int, db: Session = Depends(get_session)):
    deploy_by_id = db.query(Deploy).filter(Deploy.id == id).first()
    return deploy_by_id


# --------------------------------------------------------------------------------------------


@router.post("/deploys")
def create_deploy(deploy_data: DeployItem, db: Session = Depends(get_session)):
    new_deploy = Deploy(
        version=deploy_data.version,
        status=deploy_data.status,
        application_id=deploy_data.application_id,
    )
    db.add(new_deploy)
    db.commit()
    db.refresh(new_deploy)
    return new_deploy


# --------------------------------------------------------------------------------------------


@router.delete("/deploys/{id}")
def delete_deploy(id: int, db: Session = Depends(get_session)):
    del_deploy = db.query(Deploy).filter(Deploy.id == id).first()
    db.delete(del_deploy)
    db.commit()
    return del_deploy


# --------------------------------------------------------------------------------------------


# WARNING: Revise this!!!
@router.patch("/deploys/{id}")
def change_deploy(id: int, deploy_data: DeployItem, db: Session = Depends(get_session)):
    changing_deploy = db.query(Deploy).filter(Deploy.id == id).first()
    changing_deploy.version = deploy_data.version
    changing_deploy.status = deploy_data.status
    changing_deploy.application_id = deploy_data.application_id
    db.commit()
    db.refresh(changing_deploy)
    return changing_deploy
