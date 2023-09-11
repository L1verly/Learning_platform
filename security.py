import json
from datetime import datetime
from datetime import timedelta
from typing import Optional
from uuid import UUID

from jose import jwt

import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Making UUID serializable
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # If the obj is UUID, we simply return the value of UUID
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class UUIDDecoder(json.JSONDecoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # If the obj is UUID, we simply return the value of UUID
            return obj.hex
        return json.JSONDecoder.default(self, obj)
