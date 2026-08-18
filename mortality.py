from fastapi import APIRouter, Depends, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import mortality

router = APIRouter(prefix="/mortality", tags=["mortality"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def record_mortality(
    record: mortality,
    current_user: str = Depends(get_current_user)
):
    try:
      payload = record.model_dump()
      payload["recorded_by"] = current_user

      response = supabase.table("Mortality_logs").insert(payload).execute()
      return {"status": "success", "data": response.data}

    except Exception as e:
        raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail= str(e)
        )
@router.get("/")
def get_mortality_records(current_user: dict = Depends(get_current_user)):
    try:
        response = supabase.table("Mortality_logs").select("*").execute()
        return {"status": "success", "data": response.data}

    except Exception as e:
        raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail= str(e)
        )