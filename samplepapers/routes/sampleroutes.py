
import io
import json
import os
from typing import List
import uuid
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from samplepapers.model.samplepaperModel import SamplePaperTable, SampleBodyModel
from boto3 import client
from mongoengine.errors import DoesNotExist, ValidationError
from bson import ObjectId
from datetime import datetime

from sampleCategory.model.sampleCategoryModel import SampleCategoryTable


PACES_ACCESS_KEY = 'DO00AJFUXFALT4K6L69E'
SPACES_SECRET_KEY = 'kn2jUm8ox9W6fPQXvJ6E5kBtVZtzF5V5MvY6sJ8Cr8U'
SPACES_ENDPOINT_URL = 'https://blackwhite.blr1.digitaloceanspaces.com'
SPACES_BUCKET_NAME = 'UAASITE'

# S3 client for DigitalOcean Spaces
s3 = client('s3',
            region_name='blr1',
            endpoint_url=SPACES_ENDPOINT_URL,
            aws_access_key_id=PACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_KEY)

router = APIRouter()

# Function to upload file to DigitalOcean Spaces
def upload_file_to_space(file_content: bytes, filename: str) -> str:
    try:
        # Generate a random filename with the original extension
        random_filename = str(uuid.uuid4())
        file_extension = os.path.splitext(filename)[1]
        random_filename_with_extension = f"{random_filename}{file_extension}"

        # Create a BytesIO stream
        file_content_stream = io.BytesIO(file_content)

        # Upload the file without setting ContentLength
        s3.upload_fileobj(
            file_content_stream,
            SPACES_BUCKET_NAME,
            random_filename_with_extension,
            ExtraArgs={
                'ACL': 'public-read'
            }
        )

        # Return the file's public URL
        return f"{SPACES_ENDPOINT_URL}/UAASITE/{random_filename_with_extension}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
    



# FastAPI route to upload a sample



@router.post("/api/v1/upload-sample")
async def upload_sample(body: SampleBodyModel):
    try:
        # Resolve category reference
        category_ref = SampleCategoryTable.objects(id=ObjectId(body.sample_category)).first()
        if not category_ref:
            raise HTTPException(status_code=404, detail="Sample category not found")

        sample = SamplePaperTable(
            seo_title=body.seo_title,
            seo_description=body.seo_description,
            seo_keywords=body.seo_keywords,
            fileimages=body.fileimages,
            pageCount=body.pageCount,
            moduleName=body.moduleName,
            moduleCode=body.moduleCode,
            wordcount=body.wordcount,
            price=body.price,
            sample_file=body.sample_file,
            sample_category=category_ref,  # ReferenceField set properly
            description=body.description,
            file=body.file
        )
        sample.save()

        return JSONResponse(content={
            "message": "Sample uploaded successfully",
            "status": 201
        }, status_code=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/api/v1/all-sample")
async def getAllSample():
    try:
        samples = SamplePaperTable.objects()
        allSamples = []

        for sample in samples:
            data = sample.to_mongo().to_dict()
            data["_id"] = str(sample.id)

            try:
                if sample.sample_category:
                    data["sample_category"] = {
                        "_id": str(sample.sample_category.id),
                        "category": sample.sample_category.category
                    }
                else:
                    data["sample_category"] = None
            except DoesNotExist:
                data["sample_category"] = None

            allSamples.append(data)

        return {
            "message": "All sample papers fetched successfully",
            "data": allSamples,
            "status": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/api/v1/get-sample-perticuler/{title}")
async def getSamplePerticuler(title: str):
    query = title.replace("-", " ")
    try:
        sample = SamplePaperTable.objects.get(seo_title=query)
        data = sample.to_mongo().to_dict()
        data["_id"] = str(sample.id)

        if sample.sample_category:
            data["sample_category"] = {
                "_id": str(sample.sample_category.id),
                "category": sample.sample_category.category
            }

        return {
            "message": "Sample data fetched successfully",
            "data": data,
            "status": 200
        }

    except SamplePaperTable.DoesNotExist:
        raise HTTPException(status_code=404, detail="Sample paper not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.put("/api/v1/update-sample/{seo_title}")
async def update_sample(seo_title: str, body: SampleBodyModel):
    try:
        query = seo_title.replace("-", " ")
        sample_paper = SamplePaperTable.objects(seo_title=query).first()

        if not sample_paper:
            raise HTTPException(status_code=404, detail="Sample paper not found")

        category_ref = SampleCategoryTable.objects(id=ObjectId(body.sample_category)).first()
        if not category_ref:
            raise HTTPException(status_code=404, detail="Category not found")

        sample_paper.update(
            seo_title=body.seo_title,
            seo_description=body.seo_description,
            seo_keywords=body.seo_keywords,
            fileimages=body.fileimages,
            pageCount=body.pageCount,
            moduleName=body.moduleName,
            moduleCode=body.moduleCode,
            wordcount=body.wordcount,
            sample_file=body.sample_file,
            sample_category=category_ref,
            price=body.price,
            description=body.description,
            file=body.file
        )

        return {
            "message": "Sample paper updated successfully",
            "status": 200
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/api/v1/delete-sample/{sampleTitle}")
async def delete_sample(sampleTitle: str):
    query = sampleTitle.replace("-", " ")
    sample = SamplePaperTable.objects(seo_title=query).first()

    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    sample.delete()
    return {
        "message": "Sample deleted successfully",
        "status": 200
    }

@router.get("/api/v1/search/sample/{query}")
async def searchSample(query: str):
    try:
        results = SamplePaperTable.objects(moduleName__icontains=query)
        allSamples = []

        for sample in results:
            data = sample.to_mongo().to_dict()
            data["_id"] = str(sample.id)

            if sample.sample_category:
                data["sample_category"] = {
                    "_id": str(sample.sample_category.id),
                    "category": sample.sample_category.category
                }

            allSamples.append(data)

        return {
            "message": "Search result",
            "data": allSamples,
            "status": 200
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



   
   
@router.delete("/api/v1/delete-sample/{sampleTitle}")
async def delete_sample(sampleTitle: str): 
    query = sampleTitle.replace("-", " ")
    
    # Find the sample
    findata = SamplePaperTable.objects.filter(seo_title=query).first()
    
    if not findata:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    # Delete the sample
    findata.delete()
    
    return {
        "message": "Sample deleted successfully",
        "status": 200
    }


@router.post("/api/v1/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read file content
        file_content = await file.read()

        # Upload to DigitalOcean Spaces
        file_url = upload_file_to_space(file_content, file.filename)

        return {"message": "File uploaded successfully", "file_url": file_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    

@router.post("/api/v1/upload-pdf")
async def upload_image(sample_file: UploadFile = File(...)):
    try:
        # Read file content
        file_content = await sample_file.read()

        # Upload to DigitalOcean Spaces
        file_url = upload_file_to_space(file_content, sample_file.filename)

        return {"message": "File uploaded successfully", "file_url": file_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    


