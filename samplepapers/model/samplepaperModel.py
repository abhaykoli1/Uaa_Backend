from mongoengine import Document, StringField, ListField, IntField ,ReferenceField
from pydantic import BaseModel
from sampleCategory.model.sampleCategoryModel import SampleCategoryTable

class SamplePaperTable(Document):
    seo_title = StringField(required=True)
    seo_description = StringField(required=True)
    seo_keywords = StringField(required=True)
    fileimages = ListField(StringField())
    pageCount = IntField(required=True)
    moduleName = StringField(required=True)
    moduleCode = StringField(required=True)
    wordcount = IntField(required=True)
    price = IntField(required=True)
    description = StringField(required=True)
    sample_file = StringField(required=True)
    sample_category =  ReferenceField(SampleCategoryTable, required=True) 
    file = StringField(required=True)

# class  SamplePaperModel(BaseModel):
#     seo_title:str
#     seo_description : str
#     seo_keywords : str
#     pageCount:int
#     moduleName:str
#     moduleCode:str
#     wordcount:int
#     price : int
#     sample_file : str
#     sample_category : str
#     description: str


class SampleBodyModel(BaseModel):
    seo_title : str
    seo_description : str
    seo_keywords :str
    fileimages : list[str]
    pageCount : int
    moduleName : str
    moduleCode : str
    wordcount : int
    price : int
    sample_file : str
    sample_category : str
    description : str
    file : str