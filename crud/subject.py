from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
import models as mod


async def read_subject(db: Session):
    return db.query(mod.Subject).order_by(desc(mod.Subject.id)).all()


async def create_subject(req: mod.subjectSchema, db: Session):
    new_add = mod.Subject(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


async def delete_subject(id: int, db: Session):
    new_delete = db.query(mod.Subject)\
        .filter(mod.Subject.id == id)\
            .delete(synchronize_session=False)
    db.commit()
    return True