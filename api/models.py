import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, validator, ConfigDict
from pydantic import EmailStr


#########################
# BLOCK WITH API MODELS #
#########################


LETTER_MATCH_PATTERN = re.compile(r"^[A-Za-z\-]+$")


class TunedModel(BaseModel):
    """For Pydantic to convert even non-dict obj to JSON"""
    model_config = ConfigDict(from_attributes=True)
        
        
# Pydantic Model User to show to client
class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    
# Pydantic Model User for creating user and validate input
class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    
    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value
    
    
    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value