from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from database import get_session
from models.models import AddUserToGroupDto, Group, GroupCreate, GroupResponse, RevoveUserFromGroupDto
from models.models import User

groups_router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@groups_router.get("/groups/")
def read_groups(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(Group).offset(offset).limit(limit)).all()
    return users

@groups_router.get("/groups/{group_id}", response_model=GroupResponse)
async def read_group(group_id: int, session: SessionDep):

    query = select(Group).where(Group.id == group_id).options(joinedload(Group.users))
    group = session.exec(query).first()

    #user = session.get(User, user_id)
    if not group:
        raise HTTPException(status_code=404, detail="group not found")
    return group

@groups_router.post("/groups/", response_model=GroupResponse)
def create_group(group: GroupCreate, session: SessionDep):

     # Query the existing user by id
    initial_group_user = session.get(User, group.users_id)

    if not initial_group_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id: " 
                            + group.users_id + " not found. Group cannot be create")

    new_group = Group(name=group.name, users=[initial_group_user])

    db_group = Group.model_validate(new_group)
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return db_group

@groups_router.put("/groups/", response_model=GroupResponse)
def add_user_to_group(dto: AddUserToGroupDto, session: SessionDep):

    group_db = session.get(Group, dto.group_id)
    if not group_db:
        raise HTTPException(status_code=404, detail="Group not found")

    user_db = session.get(User, dto.user_id)
    if not group_db:
        raise HTTPException(status_code=404, detail="User not found")
    group_db.users.append(user_db)
    group_db.sqlmodel_update(group_db)

    session.add(group_db)
    session.commit()
    session.refresh(group_db)

    return group_db

@groups_router.delete("/groups/", response_model=GroupResponse)
def remove_user_from_group(dto: RevoveUserFromGroupDto, session: SessionDep):

    group_db = session.get(Group, dto.group_id)
    if not group_db:
        raise HTTPException(status_code=404, detail="Group not found")

    user_db = session.get(User, dto.user_id)
    if not group_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    group_db.users.remove(user_db)
    group_db.sqlmodel_update(group_db)

    session.add(group_db)
    session.commit()
    session.refresh(group_db)

    return group_db

@groups_router.delete("/groups/{group_id}", response_model=GroupResponse)
async def delete_group(group_id: int, session: SessionDep):

    group_db = session.get(Group, group_id)
    if not group_db:
        raise HTTPException(status_code=404, detail="Group not found")

    session.delete(group_db)
    session.commit()

    return {"message" : status.HTTP_200_OK}