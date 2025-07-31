from pydantic import BaseModel

class ARUserCreate(BaseModel):
    name: str
    email: str
    phone: str
    role: str

class ARUserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str

    class Config:
        orm_mode = True
