from fastapi import FastAPI, status, Depends, HTTPException
from core import auth_router, Base, engine, get_db, get_current_user
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import routers

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)

Base.metadata.create_all(engine)


app.include_router(auth_router)
app.include_router(routers.group_router)
app.include_router(routers.student_router)
app.include_router(routers.subject_router)
app.include_router(routers.exam_router)
app.include_router(routers.question_router)

