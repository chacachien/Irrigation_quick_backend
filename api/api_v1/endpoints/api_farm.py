from email import message
import glob
from api.api_v1.services.farmer_services import FarmerService
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from db.db import get_session
from sqlmodel import select, delete, update
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_farm import *
from typing import Annotated
from core.security import AuthHandler
from api.api_v1.services.user_services import UserService
from db.script import scripts
import logging
logger = logging.getLogger()
auth_handler = AuthHandler()


router = APIRouter()

global script 
script = scripts

@router.get("/", status_code=200)
async def get_farms(
                    session: AsyncSession = Depends(get_session), 
                    farm_id: Annotated[str | None, Query(max_length=20)]=None,
                    user = Depends(auth_handler.auth_wrapper)):
    try:

        print('USER: ', user)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_info = await FarmerService.get_me(user['userid'], session)

        if not user_info:
            raise HTTPException(status_code=403, detail="Forbidden")
        print('FARM_ID: ', farm_id)
        # query = select(Farm).where(Farm.farmer_id == user_info.id and Farm.id ==farm_id) if farm_id else select(Farm).where(Farm.farmer_id == user_info.id)
        if farm_id:
            query = select(Farm).where(Farm.id == int(farm_id) and Farm.farmer_id == user_info.id)
        else:
            query = select(Farm).where(Farm.farmer_id == user_info.id)
        result = await session.execute(query)
        farms = result.scalars().all()
        # if not farms:
        #     raise HTTPException(status_code=404, detail=f"No farms with the category {farm_id} found")

        return {"total": len(farms), "farms": farms}
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)})")

@router.post("/", status_code=200, response_model=Farm)
async def create_farm(farm_data: FarmCreate, session: AsyncSession = Depends(get_session), 
                    user = Depends(auth_handler.auth_wrapper)):
    try:
        print('USER: ', user)
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
        await session.refresh(farm)
        return farm
    except Exception as e:
        # Handle unexpected errors gracefully
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/", status_code=200, response_model=Farm)
async def update_farm(
                    farm_data: FarmUpdate, session: AsyncSession = Depends(get_session), 
                    user = Depends(auth_handler.auth_wrapper)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_info = await FarmerService.get_me(user['userid'], session)

        if not user_info:
            raise HTTPException(status_code=403, detail="Forbidden")
        # Retrieve the farm with the specified ID
        query = select(Farm).where(Farm.id == farm_data.id and Farm.farmer_id == user_info.id)
        result = await session.execute(query)
        farm = result.scalar()
        if not farm:
            raise HTTPException(status_code=404, detail=f"Farm with ID {farm_data.id} not found")
        # Update the farm with the provided data
        query = update(Farm).where(Farm.id == farm_data.id).values(farm_data.model_dump())
        await session.execute(query)

        # Commit the transaction and refresh the farm to populate auto-generated values
        await session.commit()
        await session.refresh(farm)
        return farm
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/scripts")
async def get_scripts(
                    session: AsyncSession = Depends(get_session), 
                    script_id: Annotated[str | None, Query(max_length=20)]=None,
                    user = Depends(auth_handler.auth_wrapper)):
    try:
        print('USER: ', user)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_info = await FarmerService.get_me(user['userid'], session)
        print('USER_INFO: ', user_info)
        if not user_info:
            raise HTTPException(status_code=403, detail="Forbidden")

        # if not farms:
        #     raise HTTPException(status_code=404, detail=f"No farms with the category {farm_id} found")
        global script
        if script_id:
            script = script[script_id]
        return {"total": len(script), "scripts": script}
    
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)})")
    
