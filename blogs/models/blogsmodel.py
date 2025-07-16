from mongoengine import Document, StringField, DictField
from pydantic import BaseModel

class BlogsTable(Document):
    seo_title = StringField(required=True)
    seo_description=StringField(required=True)
    title = StringField(required=True)
    shortDec = StringField(required=True)
    description = StringField(required=True)
    bannerImg = StringField(required=True)
    service_category = StringField(required=False)
    cr_date = StringField(required=False)
    seo_keywords = StringField(required=True)
class BlogSchema(BaseModel):
    title:str
    shortDec:str
    bannerImg:str
    seo_title:str
    seo_description: str
    service_category: str
    seo_keywords:str
    description:str