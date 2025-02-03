from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency: DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/v2/vpcs", response_model=schemas.VPCResponse)
def create_vpc(vpc: schemas.VPCCreate, db: Session = Depends(get_db), x_auth_token: str = Header(None)):
    # parameter 에서 X-Auth-Token 을 자동으로 추출해 준다.
    if not x_auth_token:
        raise HTTPException(status_code=401, detail="X-Auth-Token is missing")
    # x_auth_token을 전달한다.
    return crud.create_vpc(db, vpc, x_auth_token)

@app.get("/v2/vpcs", response_model=schemas.VPCListResponse)
def list_vpc(project_id: str, db: Session = Depends(get_db)):
    db_vpc = crud.list_vpcs(db, project_id)
    if db_vpc is None:
        raise HTTPException(status_code=404, detail="VPC not found")
    return {"vpcs": db_vpc}

@app.get("/v2/vpcs/{vpc_id}", response_model=schemas.VPCResponse)
def read_vpc(vpc_id: str, db: Session = Depends(get_db)):
    db_vpc = crud.get_vpc(db, vpc_id)
    if db_vpc is None:
        raise HTTPException(status_code=404, detail="VPC not found")
    return db_vpc

@app.put("/v2/vpcs/{vpc_id}", response_model=schemas.VPCResponse)
def update_vpc(vpc_id: str, vpc: schemas.VPCUpdate, db: Session = Depends(get_db)):
    db_vpc = crud.update_vpc(db, vpc_id, vpc)
    if db_vpc is None:
        raise HTTPException(status_code=404, detail="VPC not found")
    return db_vpc

@app.delete("/v2/vpcs/{vpc_id}")
def delete_vpc(vpc_id: str, db: Session = Depends(get_db)):
    db_vpc = crud.delete_vpc(db, vpc_id)
    if db_vpc is None:
        raise HTTPException(status_code=404, detail="VPC not found")
    return {"status": "DELETED"}
