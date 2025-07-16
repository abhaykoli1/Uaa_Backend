from mongoengine import Document,StringField,IntField
from pydantic import BaseModel

class AvServiceTable(Document):
    image = StringField(required = True)
    title = StringField(required =True)
    description = StringField(required =True)

class AvServiceModel(BaseModel):
    image : str 
    title : str 
    description : str 