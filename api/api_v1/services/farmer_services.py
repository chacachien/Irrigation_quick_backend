from fastapi import Depends
from db.db import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_farmer import *
from fastapi import HTTPException
from core.security import AuthHandler
from starlette import status


auth_handler = AuthHandler()
class FarmerService(object):
    __instance = None
    def __init__(self) -> None:
        pass

    @staticmethod
    async def authenticate_user(farmer: FarmerLogin, session: AsyncSession):
        query = select(Farmer).where(Farmer.value == farmer.value)
        result = await session.execute(query)
        farmer_found = result.scalar()
        print(farmer_found)
        if not farmer_found:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
        elif not auth_handler.verify_password(farmer.password, farmer_found.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
        else:
            token = auth_handler.encode_token(farmer_found.id, farmer_found.username)
            return token, farmer_found.username
        
    @staticmethod
    async def register(farmer: FarmerCreate, session: AsyncSession):
        try:
            farmer_new = Farmer(
                username = farmer.username,
                hashed_password=auth_handler.get_password_hash(farmer.password),
                value = farmer.value,
                type_res = farmer.type_res,
                gender = farmer.gender,
            )
            session.add(farmer_new)
            await session.commit()
            await session.refresh(farmer_new)
            print("SERVICE ADD SUCCESSFUL!", farmer_new)
            return farmer_new
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=str(e))
    
    @staticmethod
    async def get_me(farmer_id: int, session: AsyncSession):
        try:
            query = select(Farmer).where(Farmer.id == farmer_id)
            result = await session.execute(query)
            farmer = result.scalar()
            return farmer
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
        
    @staticmethod
    async def update_me(farmer_id: int, farmer_data , session: AsyncSession):
        try:
            query = select(Farmer).where(Farmer.id == farmer_id)
            result = await session.execute(query)
            farmer = result.scalar()
            if not farmer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
            # check if update password
            if 'password' in farmer_data:
                #check password is right 
                if not auth_handler.verify_password(farmer_data['password'], farmer.hashed_password):
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
                hashed_password = auth_handler.get_password_hash(farmer_data['new_password'])
                setattr(farmer, 'hashed_password', hashed_password)
                session.add(farmer)
                await session.commit()
                await session.refresh(farmer)
                return farmer

            for key, value in farmer_data.items():
                if hasattr(farmer, key):
                    setattr(farmer, key, value)

            session.add(farmer)
            await session.commit()
            await session.refresh(farmer)
            return farmer
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
