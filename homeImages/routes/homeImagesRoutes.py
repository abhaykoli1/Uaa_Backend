from fastapi import APIRouter, HTTPException
from bson import ObjectId
from homeImages.model.homeImagesModel import HeroModel, HeroTable

router = APIRouter()

# Helper to convert MongoEngine document to dict
def serialize_hero(hero: HeroTable):
    return {
        "id": str(hero.id),
        "images": hero.images,
        "alt": hero.alt
    }

# Create a new Hero entry
@router.post("/api/v1/heroes")
def create_hero(hero: HeroModel):
    new_hero = HeroTable(images=hero.images, alt=hero.alt)
    new_hero.save()
    return serialize_hero(new_hero)

# Get all Hero entries
@router.get("/api/v1/heroes")
def get_all_heroes():
    heroes = HeroTable.objects()
    return [serialize_hero(hero) for hero in heroes]

# Get a single Hero by ID
@router.get("/api/v1/heroes/{hero_id}")
def get_hero(hero_id: str):
    hero = HeroTable.objects(id=hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return serialize_hero(hero)

# Update a Hero by ID
@router.put("/api/v1/heroes/{hero_id}")
def update_hero(hero_id: str, hero_data: HeroModel):
    hero = HeroTable.objects(id=hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    hero.images = hero_data.images
    hero.alt = hero_data.alt
    hero.save()
    return serialize_hero(hero)

# Delete a Hero by ID
@router.delete("/api/v1/heroes/{hero_id}")
def delete_hero(hero_id: str):
    hero = HeroTable.objects(id=hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    hero.delete()
    return {"detail": "Hero deleted successfully"}
