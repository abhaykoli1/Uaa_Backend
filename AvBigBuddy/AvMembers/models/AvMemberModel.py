from mongoengine import Document,StringField,IntField
from pydantic import BaseModel 

class AvMembersTable(Document):
    image = StringField(required = True)
    name = StringField(required =True)
    designation = StringField(required =True)

class AvMembersModel(BaseModel):
    image : str
    name : str
    designation : str 