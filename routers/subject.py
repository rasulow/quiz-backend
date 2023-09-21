from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core import get_current_user, authenticate_admin
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from core import get_db
import models as mod
import crud


subject_router = APIRouter(
    prefix='/subject',
    dependencies=[Depends(HTTPBearer())],
    tags=['subject']
)


@subject_router.get('/')
async def get_subject_ADMIN(
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.read_subject(db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@subject_router.post('/')
async def create_subject_ADMIN(
    req: mod.subjectSchema, 
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.create_subject(req, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
@subject_router.delete('/{id}/')
async def delete_subject_ADMIN(
    id: int, 
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.delete_subject(id, db)
    if result:
        return JSONResponse(content={'status': 'Successfully deleted!'}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)