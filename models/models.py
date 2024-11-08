from typing import List, Union
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from typing import List, Optional, Union
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    name: str
    email: str

class GroupBase(SQLModel):
    name: str

class UserGroupLink(SQLModel, table=True):
    group_id: Optional[int] = Field(
        default=None, foreign_key="group.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )

class User(UserBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    password: str
    groups: List["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)
    entries: List["Entry"] = Relationship(back_populates="user")

class Group(GroupBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="groups", link_model=UserGroupLink)
    entries: List["Entry"] = Relationship(back_populates="group")


class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    saldo: float

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="entries")

    group_id: Optional[int] = Field(default=None, foreign_key="group.id")
    group: Optional[Group] = Relationship(back_populates="entries")

    type: int
    description: str


class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    groups: List["Group"] = []
    entries: List["Entry"] = []

class UserResponseForGroup(UserBase):
    pass

class GroupCreate(GroupBase):
    users_id: int

class GroupResponse(GroupBase):
    users: List["UserResponseForGroup"] = []    # using UserResponse in order to prevent sending sensitive data
    #entries: List["Entry"] = []

class AddUserToGroupDto(BaseModel):
    group_id: int
    user_id: int

class RevoveUserFromGroupDto(BaseModel):
    group_id: int
    user_id: int