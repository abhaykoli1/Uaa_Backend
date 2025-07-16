from mongoengine import Document, StringField
from pydantic import BaseModel

class SampleCategoryTable(Document):
    category = StringField(required=True)

class  SampleCategoryModel(BaseModel):
    category : str