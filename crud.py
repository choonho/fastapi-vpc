from sqlalchemy.orm import Session
from models import VPC
from schemas import VPCCreate, VPCUpdate
from neutron_client import create_openstack_network

from fastapi import HTTPException

def create_vpc(db: Session, project_id: str, vpc: VPCCreate, x_auth_token):
    try:
        network_id = create_openstack_network(vpc.name, project_id, x_auth_token)
        db_vpc = VPC(project_id=project_id, vpc_id=network_id, name=vpc.name, cidr=vpc.cidr)
        db.add(db_vpc)
        db.commit()
        db.refresh(db_vpc)
        return db_vpc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def list_vpcs(db: Session, project_id: str):
    return db.query(VPC).filter(VPC.project_id == project_id).all()

def update_vpc(db: Session, vpc_id: str, vpc: VPCUpdate):
    db_vpc = db.query(VPC).filter(VPC.vpc_id == vpc_id).first()
    if db_vpc:
        db_vpc.name = vpc.name
        db.commit()
        db.refresh(db_vpc)
    return db_vpc

def delete_vpc(db: Session, vpc_id: str):
    db_vpc = db.query(VPC).filter(VPC.vpc_id == vpc_id).first()
    if db_vpc:
        db.delete(db_vpc)
        db.commit()
    return db_vpc
