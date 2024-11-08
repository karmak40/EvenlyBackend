from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from database import get_session
from models.models import UserBase, UserCreate, UserResponse
from models.models import User

user_router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@user_router.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@user_router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, session: SessionDep):

    query = select(User).where(User.id == user_id).options(joinedload(User.groups))
    user = session.exec(query).first()

    #user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user