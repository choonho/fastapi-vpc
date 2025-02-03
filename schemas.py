import ipaddress
from typing import List
from pydantic import BaseModel, validator

class VPCBase(BaseModel):
    name: str
    cidr: str
    project_id: str
    @validator("cidr")
    def validate_cidr(cls, value):
        try:
            ipaddress.ip_network(value, strict=False)
        except ValueError:
            raise ValueError("Invalid CIDR format")
        return value

class VPCCreate(VPCBase):
    pass

class VPCUpdate(BaseModel):
    name: str

class VPCResponse(VPCBase):
    vpc_id: str
    project_id: str
    status: str

    class Config:
        orm_mode = True

class VPCListResponse(BaseModel):
    vpcs: List[VPCResponse]
