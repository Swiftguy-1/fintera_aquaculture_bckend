from fastapi import APIRouter, Depends, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import stock_records

router = APIRouter(prefix="/stock", tags=["stock"])

@router.post("/", status_code=status.HTTP_201_CREATED)

def stocking_records(stock_record: stock_records, current_user: str = Depends(get_current_user)):
    try:
        data = stock_record.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = (
        supabase.table("stocking_records")
        .insert(data)
        .execute()
    )
        return response.data[0]

    except Exception as error:
        print("Stock Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create stock record"
        )
@router.get("/", status_code=status.HTTP_201_CREATED)

def get_stock_records (current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("stocking_records")
            .select("*")
            .eq("recorded_by", current_user)
            .execute()
        )
        if not response.data:
            return {
                "status": "success",
                "message": "You have no stock records yet. Try creating one.",
                "data": []
            }
        return {"status": "success", "data": response.data}

    except Exception as error:
        print("Stock Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch stock records"
        )