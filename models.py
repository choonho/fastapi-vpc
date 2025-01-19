from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VPC(Base):
    __tablename__ = "vpcs"
    vpc_id = Column(String(36), primary_key=True, index=True, nullable=False)
    project_id = Column(String, index=True)
    name = Column(String, nullable=False)
    cidr = Column(String, nullable=False)
    status = Column(String, default="ACTIVE")

