from fastapi import Depends
from db.db import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_farmer import *
from fastapi import HTTPException
from core.security import AuthHandler
from starlette import status

import logging
logger = logging.getLogger()
auth_handler = AuthHandler()

class FarmService:
    @staticmethod
    async def get_farms(user: dict, session: AsyncSession, farm_id: str = None):
        try:
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                user_info = await FarmerService.get_me(user['userid'], session)
                print('USER_ID: ',user_info.id)
            
            query = select(Farm).where(Farm.farmer_id == user_info.id and Farm.id ==farm_id) if farm_id else select(Farm).where(Farm.farmer_id == user_info.id)
            result = await session.execute(query)
            farms = result.scalars().all()
            # if not farms:
            #     raise HTTPException(status_code=404, detail=f"No farms with the category {farm_id} found")

            return {"total": len(farms), "farms": farms}
        except HTTPException as he:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)})")

    @staticmethod
    async def create_farm(farm_data: FarmCreate, session: AsyncSession, user: dict):
        try:
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            logger.info(f"User {user['userid']} is trying to create a new farm.")
            user_info = await FarmerService.get_me(user['userid'], session)

            if not user_info:
                raise HTTPException(status_code=403, detail="Forbidden")

            # Create a new Farm instance using the provided data
            farm = Farm(**farm_data.model_dump(), farmer_id=user_info.id)
            # Add the farm to the session, commit the transaction, and refresh the farm to populate auto-generated values
            print(farm)
            session.add(farm)
            await session.commit()
        except HTTPException as he:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)})")
