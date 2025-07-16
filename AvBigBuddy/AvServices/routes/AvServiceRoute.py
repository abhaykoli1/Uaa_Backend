from http.client import HTTPException
import json
from bson import ObjectId
from fastapi import FastAPI ,APIRouter

from AvBigBuddy.AvServices.models.AvServiceModel import AvServiceModel, AvServiceTable



router= APIRouter()
   
@router.post("/api/v1/AvAddService")
async def addService(body : AvServiceModel):
    serviceData = AvServiceTable(**body.dict())
    serviceData.save()
    toJson = serviceData.to_json()
    fromJson = json.loads(toJson)
    return{
        "message" : "data added successfully",
        "status" : True,
        "data" :  fromJson
    }
    
@router.get("/api/v1/AvServiceList")
async def serviceList():
    serviceListData = AvServiceTable.objects.all()
    toJson = serviceListData.to_json()
    fromJson = json.loads(toJson)
    if(serviceListData): 
      return{
        "message" : "Data Fetched Successfully",
        "status" : True,
        "data" : fromJson,
    }
    else:
       return{
          "message" : "Data Not Found",
          "status" : False,
          "data": None
       }

@router.get("/api/v1/get-AvService/{_id}")
async def get_service(_id: str):
    query = _id.replace("-", " ")
    service = AvServiceTable.objects(id=query).first()
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return {
        "message": "Service data",
        "data": json.loads(service.to_json()),
        "status": 200
    }

@router.put("/api/v1/update-AvService/{_id}")
async def update_service(_id: str, body: AvServiceModel):
    query = _id.replace("-", " ")
    try:
        service = AvServiceTable.objects(id=query).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # Update the document using `modify`
        service.modify(
            image=body.image,
            title=body.title,
            description=body.description
        )
        service.reload()  # Reload to get updated data

        return {
            "message": "Service updated successfully",
            "data": json.loads(service.to_json())
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/api/v1/AvDeleteAllServices")
async def deleteServices():
   deleteServiceData = AvServiceTable.objects.delete()
   if deleteServiceData == 0:
      return{
         "message" : "data Deleted Successfully",
         "status" : True,
         "data" : None
      }
   
@router.delete("/api/v1/AvDeleteAService/{_id}")
async def ServiceDeleteById(_id : str):
    object_id = ObjectId(_id)
    item = AvServiceTable.objects(id=object_id).first()
    item.delete()
    
    return {
        "message": "Data Deleted Successfully",
        "status": True,
    }