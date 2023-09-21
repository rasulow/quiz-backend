from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core import get_current_user, authenticate_admin, authenticate_student
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from core import get_db
import models as mod
import crud


exam_router = APIRouter(
    prefix='/exam',
    dependencies=[Depends(HTTPBearer())],
    tags=['exam']
)


@exam_router.get('/')
async def get_exams_ADMIN(
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.read_exam(db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
@exam_router.get('/results/')
async def get_results_admin(
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = jsonable_encoder(await crud.get_exam_results(db))
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
@exam_router.post('/')
async def create_exam_ADMIN(
    req: mod.examSchema, 
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.create_exam(req, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
@exam_router.patch('/{id}/')
async def update_status_ADMIN(
    id: int, 
    req: mod.examStatusSchema, 
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.update_status(id, req, db)
    if result:
        return JSONResponse(content={'status': 'Successfully updated!'}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
    
@exam_router.delete('/{id}/')
async def delete_exam_ADMIN(
    id: int, 
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.delete_exam(id, db)
    if result:
        return JSONResponse(content={'status': 'Successfully deleted!'}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST) 
    
                
@exam_router.get('/active/')
async def active_exams_STUDENT(
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_student(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.get_active_exams(user.id, db)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@exam_router.get('/passed/')
async def passed_exams_STUDENT(
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_student(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = jsonable_encoder(await crud.get_passed_exams(user.id, db))
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    

@exam_router.get('/{id}/')
async def get_current_exam_STUDENT(
    id: int, 
    header_param: Request, 
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_student(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = jsonable_encoder(await crud.get_current_exam(id, db))
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    

    