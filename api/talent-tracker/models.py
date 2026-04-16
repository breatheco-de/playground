from pydantic import constr


from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RecordCreate(BaseModel):
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)
    position: str = Field(...)
    linkedin_url: Optional[str] = None
    cv_url: Optional[str] = None
    experience_years: float = Field(...)

class RecordOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: str
    position: str
    linkedin_url: Optional[str]
    cv_url: Optional[str]
    status: str
    stage: str
    experience_years: float
    notes_count: int
    applied_at: str
    updated_at: str


class NoteCreate(BaseModel):
    content: constr(min_length=1)

class NoteOut(BaseModel):
    id: str
    record_id: str
    content: str
    created_at: str