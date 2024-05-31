from typing import List
from models.model_farm import Farm
from pydantic import validator
from sqlmodel import Field, SQLModel, Relationship
from models.model_base import TimestampModel


class FarmerBase(SQLModel):
    username: str
    type_res: str
    # set value is primary key
    value: str = Field(unique = True)
    gender: str


class FarmerCreate(FarmerBase):
    password: str = Field(max_length=256, min_length=5)
    password2: str
    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    

class FarmerLogin(SQLModel):
    value: str
    password: str

class Farmer(FarmerBase, TimestampModel, table = True):
    __tablename__ = "farmer"
    id: int|None = Field(default=None, primary_key=True)
    hashed_password: str| None = None
    #farms: List[Farm] = Relationship(back_populates="farmer")

    def __repr__(self):
        return f"User: {self.username}"
    
