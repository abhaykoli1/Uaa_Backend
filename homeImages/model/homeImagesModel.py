from mongoengine import Document, StringField, ListField
from pydantic import BaseModel
from typing import List

class HeroTable(Document):
    images = ListField(StringField(), required=True) 
    alt = StringField(required=True)

class HeroModel(BaseModel):
    images: List[str]
    alt: str
