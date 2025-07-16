from datetime import datetime
from typing import Optional
from mongoengine import Document, StringField ,DateTimeField , BooleanField
from pydantic import BaseModel



class UserTable(Document):
    name= StringField(required=True)
    email = StringField(required=True)
    password = StringField(required= True)
    phone = StringField(required=True)
    country_code = StringField(required=True)
    has_downloaded = BooleanField(required=False, default=False)
    created_at = DateTimeField(default=datetime.utcnow)
class UserCreateModel(BaseModel):
    name: str
    email:str
    password:str
    phone:str
    country_code:str
    has_downloaded: Optional[bool] = False
    created_at: Optional[datetime] = None
    
# dsds