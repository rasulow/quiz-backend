from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core import get_current_user, authenticate_admin, authenticate_student
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from core import get_db
import models as mod
import crud
from typing import List


question_router = APIRouter(
    prefix='/question',
    dependencies=[Depends(HTTPBearer())],
    tags=['question']
)


@question_router.get('/')
async def get_question_ADMIN(header_param: Request, 
                       exam_id: int = None, 
                       subject_id: int = None, 
                       db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.read_question(exam_id, subject_id, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@question_router.post('/')
async def create_question_ADMIN(req: mod.questionSchema, 
                          header_param: Request, 
                          db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.create_question(req, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
    
@question_router.delete('/{id}/')
async def delete_question_ADMIN(id: int, 
                          header_param: Request, 
                          db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.delete_question(id, db)
    if result:
        return JSONResponse(content={'status': 'Successfully deleted!'}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
    
@question_router.get('/{exam_id}/')
async def get_current_exam_questions_STUDENT(
    exam_id: int,
    header_param: Request,
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_student(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.get_current_exam_questions(exam_id, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
@question_router.post('/result/')
async def post_results_STUDENT(
    req: List[mod.resultSchema],
    header_param: Request,
    db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_student(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    result = await crud.check_result_of_exam(req, user.id, db)
    return result