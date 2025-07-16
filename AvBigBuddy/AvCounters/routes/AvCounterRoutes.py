from http.client import HTTPException
import json
from fastapi import APIRouter

from AvBigBuddy.AvCounters.models.AvCounters import AVCountersModel, AVCountersTable



router = APIRouter()

@router.post("/api/v1/add-avcounters")
async def addCounters(body: AVCountersModel):
    savedata = AVCountersTable(**body.dict())
    savedata.save()
    
    return {
        "message": "Counters Added",
        "status":200
    }


@router.get("/api/v1/get-all-avcounters")
async def getAllCounters():
    findata = AVCountersTable.objects.all()
    return {
        "message": "all Counters",
        "data": json.loads(findata.to_json()),
        "status": 200
    }

@router.put("/api/v1/update-avcounters/{counter_id}")
async def updateCounter(counter_id: str, body: AVCountersModel):
    query = counter_id.replace("-", " ")
    try:
        counter = AVCountersTable.objects(id=query).first()
        if not counter:
            raise HTTPException(status_code=404, detail="Counter not found")  
        counter.modify(
            build=body.build,
            identity=body.identity,
            growth=body.growth,
        )   
        counter.reload()  

        return {
            "message": "Counter updated successfully",
            "data": json.loads(counter.to_json())
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# @router.put("/api/v1/update-avcounters/{counter_id}")
# async def updateCounter(counter_id: str, body: AVCountersModel):
#     counter = AVCountersTable.objects.filter(id=counter_id).first()
#     if not counter:
#         return {"message": "Counter not found", "status": 404}
    
#     counter.update(**body.dict())
#     return {"message": "Counter updated successfully", "status": 200}
    
@router.delete("/api/v1/deleteAvCounters")
def delete_all_samples():
    deleted = AVCountersTable.objects.all().delete()
    return {
        "message": f"Deleted  successfully",
        "status": 200
    }