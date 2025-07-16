from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class AvProductTable(Document):
    image = StringField(required = True)
    title = StringField(required =True)
    type = StringField(required =True)

class AvProductModel(BaseModel):
    image : str
    title : str
    type : str