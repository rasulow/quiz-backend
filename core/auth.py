from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from .db_connection import SessionLocal
from models import Admin, Student, studentSchema
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class UserRequest(BaseModel):
    username: str = 'admin'
    password: str = 'admin'
    
    
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@auth_router.post('/create-admin/', status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: UserRequest, 
    db: Session = Depends(get_db),):
    create_user_model = Admin(
        username = create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    access_token = create_access_token(
        create_user_request.username, 
        create_user_request.password, 
        create_user_model.id)
    update_user_model = db.query(Admin)\
        .filter(Admin.id == create_user_model.id)\
    .update({Admin.token: access_token}, synchronize_session=False)
    db.commit()
    return JSONResponse(content={'status': 'Successfully created'}, 
                        status_code=status.HTTP_201_CREATED)
    
    
@auth_router.post('/token-admin/')
async def login_for_access_token(user: UserRequest,
                                db: Session = Depends(get_db)):
    user = authenticate_admin(user.username, user.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
    
    user = jsonable_encoder(user)
    del user['hashed_password']
    return JSONResponse(content=user, status_code=status.HTTP_200_OK)




@auth_router.post('/create-student/', status_code=status.HTTP_201_CREATED)
async def create_user(req: studentSchema, db: Session = Depends(get_db),):
    create_user_model = Student(
        student_id=req.student_id,
        name=req.name,
        surname=req.surname,
        username = req.username,
        hashed_password = bcrypt_context.hash(req.password),
        group_id=req.group_id
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    access_token = create_access_token(
        req.username, 
        req.password, 
        create_user_model.id)
    update_user_model = db.query(Student)\
        .filter(Student.id == create_user_model.id)\
    .update({Student.token: access_token}, synchronize_session=False)
    db.commit()
    return JSONResponse(content={'status': 'Successfully created'}, 
                        status_code=status.HTTP_201_CREATED)
    
    
@auth_router.post('/token-student/')
async def login_for_access_token(user: UserRequest,
                                db: Session = Depends(get_db)):
    user = authenticate_student(user.username, user.password, db)
    # if user.in_exam:
    #     return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                          detail='This student already in exam!')
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
    
    db.query(Student).filter(Student.id == user.id)\
        .update({
            Student.in_exam: True
        }, synchronize_session=False)
    db.commit()
    result = {
        'id': user.id,
        'username': user.username,
        'token': user.token
    }
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)



def authenticate_student(username: str, password: str, db):
    user = db.query(Student).filter(Student.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user



@auth_router.delete('/logout/', dependencies=[Depends(HTTPBearer())])
async def logout_student(header_param: Request, 
                         db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_student(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    db.query(Student).filter(Student.id == user.id)\
        .update({
            Student.in_exam: False            
        }, synchronize_session=False)
    db.commit()
    return JSONResponse(content={'status': 'Successfully logged out!'}, status_code=status.HTTP_200_OK)




def create_access_token(username: str, password: str, user_id: int):
    encode = {'username': username, 'password': password, 'id': user_id}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_admin(username: str, password: str, db):
    user = db.query(Admin).filter(Admin.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user





async def get_current_user(header_params: Request):
    token = header_params.headers.get('Authorization').split('Bearer ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        password: str = payload.get('password')
        user_id: int = payload.get('id')
        if username is None or user_id is None or password is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return  {
                    'username': username, 
                    'password': password, 
                    'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
   
