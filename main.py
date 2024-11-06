
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine
from typing_extensions import Annotated
from sqlmodel import SQLModel

from database import create_db_and_tables, get_session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root(session: SessionDep):

    return {"message": "321"}