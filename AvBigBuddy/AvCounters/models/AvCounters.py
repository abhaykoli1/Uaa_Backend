from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class AVCountersTable(Document):
    build= StringField(required =True)
    identity = StringField(required =True)
    growth = StringField(required =True)
   
    

class AVCountersModel(BaseModel):
    build :str
    identity :str
    growth :str
