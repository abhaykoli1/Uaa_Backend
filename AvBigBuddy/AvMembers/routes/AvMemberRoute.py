from http.client import HTTPException
import json
from bson import ObjectId
from fastapi import FastAPI ,APIRouter

from AvBigBuddy.AvMembers.models.AvMemberModel import AvMembersModel, AvMembersTable




router= APIRouter()
   
@router.post("/api/v1/AvAddMembers")
async def addMembers(body : AvMembersModel):
    MembersData = AvMembersTable(**body.dict())
    MembersData.save()
    toJson = MembersData.to_json()
    fromJson = json.loads(toJson)
    
    return{
        "message" : "data added successfully",
        "status" : True,
        "data" :  fromJson
    }


@router.get("/api/v1/AvMembersList")
async def MembersList():
    MembersListData = AvMembersTable.objects.all()
    toJson = MembersListData.to_json()
    fromJson = json.loads(toJson)
    if(MembersListData): 
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
   
@router.get("/api/v1/get-AvMember/{_id}")
async def get_member(_id: str):
    query = _id.replace("-", " ")
    member = AvMembersTable.objects(id=query).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return {
        "message": "Member data",
        "data": json.loads(member.to_json()),
        "status": 200
    }

@router.put("/api/v1/update-AvMember/{_id}")
async def update_member(_id: str, body: AvMembersModel):
    query = _id.replace("-", " ")
    try:
        member = AvMembersTable.objects(id=query).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Update the document using `modify`
        member.modify(
            image=body.image,
            name=body.name,
            designation=body.designation,
        )
        member.reload()  # Reload to get updated data

        return {
            "message": "Member updated successfully",
            "data": json.loads(member.to_json())
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        
@router.delete("/api/v1/AvDeleteAllMemberss")
async def deleteMemberss():
   deleteMembersData = AvMembersTable.objects.delete()
   if deleteMembersData == 0:
      return{
         "message" : "data Deleted Successfully",
         "status" : True,
         "data" : None
      }


@router.delete("/api/v1/AvDeleteAMember/{_id}")
async def ServiceDeleteById(_id : str):
    object_id = ObjectId(_id)
    item = AvMembersTable.objects(id=object_id).first()
    item.delete()
    
    return {
        "message": "Data Deleted Successfully",
        "status": True,
    }