from pydantic import BaseModel
from datetime import time

class groupSchema(BaseModel):
    no: int
    
    
class studentSchema(BaseModel):
    student_id: int
    name: str
    surname: str
    username: str
    password: str
    group_id: int
    
    
class subjectSchema(BaseModel):
    name: str
    
    
    
class examSchema(BaseModel):
    name: str
    description: str
    time: time
    status: bool = False
    
    
class examStatusSchema(BaseModel):
    status: bool
    
    
    
class questionSchema(BaseModel):
    question_text: str
    option1: str
    option2: str
    option3: str
    option4: str
    correct_answer: int
    subject_id: int
    exam_id: int
    
    
class resultSchema(questionSchema):
    id: int = None
    result: int = None