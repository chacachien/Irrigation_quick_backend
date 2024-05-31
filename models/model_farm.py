from typing import Optional
from pydantic import validator
from sqlmodel import Field, SQLModel, Relationship
from models.model_base import TimestampModel


class FarmBase(SQLModel):
    name: str|None = Field(default=None, unique=True)   
    type: str
    address: str
    area: float 
    script: str | None = None

class FarmCreate(FarmBase):
    pass

class FarmUpdate(FarmBase):
    id: int
    

class Farm(FarmBase, TimestampModel, table = True):
    __tablename__ = "farm"
    id: int|None = Field(default=None, primary_key=True)
    farmer_id: Optional[int] = Field(default=None, foreign_key="farmer.id")
    #farmer: Optional["Farmer"] = Relationship(back_populates="farms")

    def __repr__(self):
        return f"User: {self.name}"
    
    
