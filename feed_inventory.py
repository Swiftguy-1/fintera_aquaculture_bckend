from fastapi import Depends, APIRouter, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import Feed_inventory

router = APIRouter(prefix = "/feed_inventory", tags = ["feed_inventory"])

@router.post("/", status_code = status.HTTP_201_CREATED)

def create_feed_inventory(feed_inventory: Feed_inventory, current_user: str = Depends(get_current_user)):
  try:  
    data = feed_inventory.model_dump(mode="json")
    data["recorded_by"] = current_user
    response = supabase.table("Feeds").insert(data).execute()
    return response.data[0]
  except Exception as error:
    print("Feed Inventory Error Details:", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Error creating feed inventory or feed inventory could not be created."
    ) 

@router.get("/", status_code = status.HTTP_200_OK)

def get_feed_inventory( current_user: str = Depends(get_current_user)):
  try:
    response = supabase.table("Feeds").select("*").eq("recorded_by", current_user).execute()
    if not response.data:
      return {
        "status": "success",
        "message": "You have no feed inventory records yet. Try creating one.",
        "data": []
      }
    return {"status": "success", "data": response.data}
  except Exception as error:
    print("Feed Inventory Error Details:", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Error fetching feed inventory or feed inventory could not be found."
    )