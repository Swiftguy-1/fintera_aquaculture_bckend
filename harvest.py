from fastapi import APIRouter, Depends, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import harvest

router = APIRouter(prefix="/harvest", tags=["harvest"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_harvest_record(harvest_record: harvest, current_user: str = Depends(get_current_user)):
    try:
        data = harvest_record.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = supabase.table("Harvest").insert(data).execute()
        return response.data[0]
    except Exception as error:
        print("Harvest Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating harvest record or record could not be created."
        )

@router.get("/", status_code=status.HTTP_200_OK)
def get_harvest_records(current_user: str = Depends(get_current_user)):
    try:
        response = (
          supabase.table("Harvest")
          .select("*")
          .eq("recorded_by", current_user)
          .execute()
        )
        if not response.data:
            return {
              "status": "success",
              "message": "You have no Harvest records yet. Try creating one.",
              "data": []
            }
        return{"status": "success", "data": response.data}
    except Exception as error:
        print("Harvest Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching harvest records or records could not be found."
        )
