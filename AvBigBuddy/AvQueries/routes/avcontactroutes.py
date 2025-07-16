import json
from fastapi import APIRouter

from AvBigBuddy.AvQueries.models.avcontactquery import AvContactQueryModel, AvContactQueryTable



router = APIRouter()

@router.post("/api/v1/add-AvContact-query")
async def addAvContactQuery(body: AvContactQueryModel):
    savedata = AvContactQueryTable(**body.dict())
    savedata.save()

    return {
        "message": "contact added",
        "status":200
    }


@router.get("/api/v1/get-all-AvContact")
async def getAllAvContact():
    findata = AvContactQueryTable.objects.all()
    return {
        "message": "all contact query",
        "data": json.loads(findata.to_json()),
        "status": 200
    }