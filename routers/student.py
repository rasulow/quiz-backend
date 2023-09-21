from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core import get_current_user, authenticate_admin
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from core import get_db
import models as mod
import crud



student_router = APIRouter(
    prefix='/student', 
    dependencies=[Depends(HTTPBearer())], 
    tags=['student']
)


@student_router.get('/')
async def get_student_ADMIN(
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.read_student(db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
@student_router.delete('/{id}/')
async def create_student_ADMIN(
    id: int, 
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.delete_student(id, db)
    if result:
        return JSONResponse(content={'status': 'Successfully deleted!'}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)