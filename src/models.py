# Models for the API requests and responses
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime

class MovieModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    title: str = Field(...)
    director: str = Field(...)
    genres: Optional[List[str]] = None
    description: Optional[str] = None
    release_date: Optional[int] = Field(None, le=datetime.now().year + 5)


    @validator("release_date", allow_reuse=True)
    @classmethod
    def release_date_must_be_reasonable(cls, v):
        if v and (v < 1878 or v > datetime.now().year + 5):
            raise ValueError('release_date must be between 1878 and the current year plus five')
        return v

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Inception",
                "director": "Christopher Nolan",
                "genres": ["Action", "Adventure", "Sci-Fi"],
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology...",
                "release_date": 2010
            }
        }

class MovieUpdateModel(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    genres: Optional[List[str]] = None
    description: Optional[str] = None
    release_date: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Inception",
                "director": "Christopher Nolan",
                "genres": ["Action", "Adventure", "Sci-Fi"],
                "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O....",
                "release_date": 2010
            }
        }


