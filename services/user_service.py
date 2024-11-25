from sqlalchemy.orm import Session, joinedload
from models.roles_model import Role
from models.user_model import User
from fastapi import HTTPException


def getUserById(id: int,  db: Session) -> User:
    print(db)
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        print(f'user not found with id ${id}')
        raise HTTPException(status_code=400, detail="User not found")
    else:
        print(f'user found with id ${db_user}')
        return db_user


def getUserWithRoleAndPermissions(filter,  db: Session) -> User:
    print(db)
    db_user = db.query(User).options(joinedload(User.roles)
                                     .joinedload(Role.permissions)
                                     ).filter(*filter).first()

    if not db_user:
        print(f'user not found with id ${id}')
        raise HTTPException(status_code=400, detail="User not found")
    else:
        print(f'user found with id ${db_user}')
        return db_user
