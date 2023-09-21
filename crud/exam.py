from fastapi import Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_
import models as mod


async def read_exam(db: Session):
    return db.query(mod.Exam).order_by(desc(mod.Exam.id)).all()



async def create_exam(req: mod.examSchema, db: Session):
    new_add = mod.Exam(
        name = req.name,
        description = req.description,
        time = req.time,
        status = req.status
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


async def update_status(id, req: mod.examStatusSchema, db: Session):
    new_update = db.query(mod.Exam).filter(mod.Exam.id == id)\
        .update({
            mod.Exam.status: req.status
        }, synchronize_session=False)
    db.commit()
    return new_update


async def delete_exam(id: int, db: Session):
    new_delete = db.query(mod.Exam)\
        .filter(mod.Exam.id == id)\
            .delete(synchronize_session=False)
    db.commit()
    return True



async def get_active_exams(student_id: int, db: Session):
    passedExams = db.query(mod.PassedExams)\
        .filter(mod.PassedExams.student_id == student_id)\
            .all()
    activeExams = db.query(mod.Exam)\
        .filter(mod.Exam.status == True)\
            .order_by(desc(mod.Exam.id))\
                .all()
    resultActiveExams = []
    for active in activeExams:
        k = 0
        for passed in passedExams:
            if active.id == passed.exam_id:
                k = 1
        if k == 0:
            resultActiveExams.append(active)
    return resultActiveExams


async def get_passed_exams(student_id: int, db: Session):
    passedExams = db.query(mod.PassedExams)\
        .filter(mod.PassedExams.student_id == student_id)\
            .options(joinedload(mod.PassedExams.exam)).all()
    return passedExams


async def get_current_exam(id: int, db: Session):
    currentExam = db.query(mod.Exam)\
        .filter(mod.Exam.id == id)\
            .first()
    return currentExam


async def get_exam_results(db: Session):
    result = db.query(mod.PassedExams)\
        .options(joinedload(mod.PassedExams.exam))\
            .options(joinedload(mod.PassedExams.student))\
                .order_by(desc(mod.PassedExams.id))\
                    .all()
    return result