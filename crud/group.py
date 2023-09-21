from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
import models as mod


async def read_groups(db: Session):
    return db.query(mod.Group).order_by(desc(mod.Group.id)).all()


async def create_group(db: Session, req: mod.groupSchema):
    new_add = mod.Group(
        no = req.no
    )
    
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


async def delete_group(id, db: Session):
    new_delete = db.query(mod.Group)\
        .filter(mod.Group.id == id)\
            .delete(synchronize_session=False)
    db.commit()
    return True