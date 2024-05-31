from models.model_farm import FarmCreate
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import JsonValue
from starlette.responses import JSONResponse
from starlette import status
from db.db import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_farmer import *
from typing import Annotated
from core.security import AuthHandler
import logging

from api.api_v1.services.farmer_services import FarmerService
router = APIRouter()
# dependencies=[Depends(oauth2_bearer), Depends(get_current_user)]
#user_dependency = Annotated[dict, Depends(get_current_user)]
auth_handler = AuthHandler()
logger = logging.getLogger()

@router.get("/")
async def get_farmers(
                    session: AsyncSession = Depends(get_session), 
                    q: Annotated[str | None, Query(max_length=20)]=None,
                    #user = Depends(auth_handler.auth_wrapper)
                    ):
    # if user is None:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    farmers = await session.execute(select(Farmer))

    if q is not None:
        farmers = await session.execute(select(Farmer).where(Farmer.name == q))
        farmers_result = farmers.scalar()
        return {"farmers": [farmer for farmer in farmers_result]}
    else:
        farmers = farmers.scalars().all()
        return {"total": len(farmers), "farmers": [farmer for farmer in farmers]}
    

# @router.get("/{farmer_id}")
# async def get_farmer(farmer_id: Annotated[int, Path(title='The id')], session: AsyncSession = Depends(get_session)):
#     farmer = await session.exec(select(Farmer).where(Farmer.id == farmer_id)).first()
#     return farmer

@router.get("/{farmer_id}/blogs")
async def get_farmer_blogs(farmer_id: Annotated[int, Path(title='The farmer id')], session: AsyncSession = Depends(get_session),
                           farm_id: Annotated[str | None, Query(max_length=20)]=None
                           ):
    farmer = await session.exec(select(Farmer).where(Farmer.id == farmer_id)).first()
    return farmer.blogs


# register
@router.post("/register")
async def create_farmer(farmer_data: FarmerCreate, user_service: FarmerService = Depends(), session: AsyncSession = Depends(get_session)):
    #farmer = Farmer(**farmer_data.model_dump())
    farmer_new = await user_service.register(farmer_data, session)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=f"Successful!, User: {farmer_new}")

@router.post('/login')
async def login(farmer: FarmerLogin, user_service: FarmerService = Depends(), session: AsyncSession= Depends(get_session) ):
    token, user_name = await user_service.authenticate_user(farmer, session=session)
    return {"token": token, "user": user_name}

@router.get('/me')
async def get_me(current_farmer: JsonValue = Depends(auth_handler.auth_wrapper), user_service: FarmerService = Depends(), session:AsyncSession=Depends(get_session)):
    logger.debug(f"current farmer: {current_farmer} ")
    current_user = await user_service.get_me(current_farmer['userid'], session)
    return current_user

@router.patch('/me')
async def update_me(farmer_data: dict, current_farmer: JsonValue = Depends(auth_handler.auth_wrapper), user_service: FarmerService = Depends(), session: AsyncSession = Depends(get_session)):
    current_user = await user_service.update_me(current_farmer['userid'], farmer_data, session)
    return current_user


@router.get('/{farmer_id}/farms')
async def get_farmes(farmer_id: Annotated[int, Path(title='The farmer id')], session: AsyncSession = Depends(get_session),
                    farm_id: Annotated[str | None, Query(max_length=20)]=None

                     ):
    try:
        query = select(Farm).where(Farm.farmer_id == farmer_id and Farm.id == farm_id) if farm_id else select(Farm).where(Farm.farmer_id == farmer_id)
        result = await session.execute(query)
        farms = result.scalars().all()
        return {"total": len(farms), "farms": farms}
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)})")
    
@router.post('/{farmer_id}/farms')
async def create_farm(farm_data: FarmCreate, farmer_id: Annotated[int, Path(title='The farmer id')], session: AsyncSession = Depends(get_session), user = Depends(auth_handler.get_current_user) ):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        logger.info(f"User {user['userid']} is trying to get farms")
        user_info = await FarmerService.get_me(user['userid'], session)

        if not user_info:
            raise HTTPException(status_code=403, detail="Forbidden")

        # Create a new Farm instance using the provided data
        farm = Farm(**farm_data.model_dump(), farmer_id=farmer_id)
        # Add the farm to the session, commit the transaction, and refresh the farm to populate auto-generated values
        print(farm)
        session.add(farm)
        await session.commit()
        await session.refresh(farm)
        
        return farm
    except Exception as e:
        # Handle unexpected errors gracefully
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
