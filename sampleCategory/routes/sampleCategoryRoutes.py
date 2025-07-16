from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

import json
import traceback

from sampleCategory.model.sampleCategoryModel import SampleCategoryModel , SampleCategoryTable

router = APIRouter()

# Create a category
@router.post("/api/v1/add-category")
async def create_category(data: SampleCategoryModel):
    try:
        category = SampleCategoryTable(**data.dict())
        category.save()

        return JSONResponse(content={
            "message": "Sample category created successfully",
            "data": category.to_json()
        }, status_code=201)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Get all categories
@router.get("/api/v1/all-category")
async def get_all_categories():
    try:
        allCategory = []
        categories = SampleCategoryTable.objects.all()

        for value in categories:
            allCategory.append(json.loads(value.to_json()))

        return {
            "message": "Here is all sample",
            "data": allCategory,
            "status": 200
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Get category by ID
@router.get("/api/v1/category/{id}")
async def get_category_by_id(id: str):
    try:
        category = SampleCategoryTable.objects.get(id=id)
        return {
            "message": "Sample category data",
            "data": json.loads(category.to_json()),
            "status": 200
        }
    except SampleCategoryTable.DoesNotExist:
        raise HTTPException(status_code=404, detail="Sample Category not found")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Update category by ID
@router.put("/api/v1/update-category/{id}")
async def update_category(id: str, data: SampleCategoryModel):
    try:
        category = SampleCategoryTable.objects(id=id).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        category.update(**data.dict())
        updated = SampleCategoryTable.objects.get(id=id)

        return {
            "message": "Sample category updated successfully",
            "data": json.loads(updated.to_json())
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Delete category by ID
@router.delete("/api/v1/delete-category/{id}")
async def delete_category(id: str):
    try:
        category = SampleCategoryTable.objects(id=id).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        category.delete()

        return {
            "message": "Category deleted successfully",
            "status": 200
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
