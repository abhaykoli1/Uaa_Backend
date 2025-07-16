from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class AvContactQueryTable(Document):
    name = StringField(required=True)
    phone = StringField(required=True)
    email = StringField(required=True)
    country_code = StringField()
    message = StringField(required=True)

class AvContactQueryModel(BaseModel):
    name :str
    phone :str
    email :str
    country_code :str
    message :str