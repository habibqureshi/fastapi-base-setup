from logging import Logger
from sqlalchemy.orm import Session, joinedload
from models.roles_model import Role
from models.user_model import User
from fastapi import HTTPException

from schemas.user_schema import UserCreateWithRole


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


def create_new_user(user: UserCreateWithRole, db: Session, logger: Logger):
    logger.info(f'creating new user {user}')
    try:
        new_user = User(**user.__dict__)
        new_user.roles = [db.merge(Role(id=role.id)) for role in user.roles]
        logger.info(f'new user {new_user.roles[0]}')
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        if hasattr(e, 'message'):
            logger.error(f'error while creating user message {e.message}')
        else:
            logger.error(f'error while creating user {e}')
        error_message = str(e)
        raise HTTPException(
            status_code=400, detail=f"Error while creating new user {error_message}")
