
from fastapi import Depends, FastAPI
from sqlmodel import Session
from typing_extensions import Annotated
from routes.user import user_router
from routes.group import groups_router

from database import create_db_and_tables, get_session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
app.include_router(user_router, tags=["User"])
app.include_router(groups_router,  tags=["Group"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root(session: SessionDep):

    return {"message": "321"}