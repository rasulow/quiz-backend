from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
import models as mod


async def read_student(db: Session):
    result = db.query(
        mod.Student
    )\
        .options(joinedload(mod.Student.group))\
            .order_by(desc(mod.Student.id))\
                .all()
                
    return result


async def delete_student(id, db: Session):
    new_delete = db.query(mod.Student)\
        .filter(mod.Student.id == id)\
            .delete(synchronize_session=False)
    db.commit()
    return True