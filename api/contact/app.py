from typing import List, Optional, Annotated

from fastapi import (
    FastAPI, Request, Response, HTTPException,
    Query, Depends, Path, status,
)
from fastapi.openapi.docs import get_swagger_ui_html

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from sqlmodel import (
    Session, select
)

from api.contact.models import (
    Agenda, AgendaCreate, AgendaRead,
    Contact, ContactCreate, ContactRead, ContactUpdate,
    AgendaList, ContactList, AgendaReadWithItems,
)
from api.db import get_session

app = FastAPI(
    title="Contact List API",
    description="An API for storing contacts.",
    docs_url=None,
)

limiter = Limiter(key_func=get_remote_address)
# Limiter requires the request to be in the args for your routes!
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        title="4Geeks Playground - Contact List API",
        openapi_url="/contact/openapi.json",
        swagger_favicon_url="/favicon.ico"
    )


@app.get(
    "/agendas",
    response_model=AgendaList,
    tags=["Agenda operations"],
)
@limiter.limit("120/minute")
def get_agendas(
    request: Request,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session)
):
    return {
        "agendas": session.exec(
            select(Agenda).offset(offset).limit(limit)
        ).all()
    }


@app.get(
    "/agendas/{slug}",
    response_model=AgendaReadWithItems,
    tags=["Agenda operations"],
)
@limiter.limit("120/minute")
def get_agenda(
    request: Request,
    slug: Annotated[str, Path(title="slug")],
    session: Session = Depends(get_session)
):
    agenda = session.exec(select(Agenda).where(
        Agenda.slug == slug)
    ).first()
    if agenda:
        return agenda
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"""Agenda "{slug}" doesn't exist."""
    )


@app.post(
    "/agendas/{slug}",
    status_code=status.HTTP_201_CREATED,
    response_model=AgendaRead,
    tags=["Agenda operations"],
)
@limiter.limit("15/minute")
def create_agenda(
    request: Request,
    slug: Annotated[str, Path(title="slug")],
    session: Session = Depends(get_session)
) -> None:
    user_exists = session.exec(select(Agenda).where(
        Agenda.slug == slug)).first()
    if not user_exists:
        db_user = Agenda(slug=slug)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User already exists."
    )


@app.delete(
    "/agendas/{slug}",
    tags=["Agenda operations"],
)
@limiter.limit("15/minute")
def delete_agenda(
    request: Request,
    slug: Annotated[str, Path(title="slug")],
    session: Session = Depends(get_session),
    tags=["Agenda operations"],
):
    user = session.exec(select(Agenda).where(
        Agenda.slug == slug)
    ).first()
    if user:
        session.delete(user)
        session.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"""Agenda "{slug}" doesn't exist."""
    )


@app.post(
    "/agendas/{slug}/contact",
    response_model=ContactRead,
    tags=["Contact operations"],
)
@limiter.limit("60/minute")
def post_agenda_contact(
    request: Request,
    contact: ContactCreate,
    session: Session = Depends(get_session)
):
    agenda = session.exec(select(Agenda).where(
        Agenda.slug == contact.slug)
    ).first()
    if agenda:
        db_todo = Contact.model_validate(contact)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User #{contact.user_id} doesn't exist."
    )
