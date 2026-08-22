from fastapi import APIRouter, HTTPException, status, Depends
from db import supabase
from dependencies import get_current_user
from schemas import feeding_logs

router = APIRouter(prefix= "/feeding_logs", tags=["feeding_logs"])

@router.post("/", status_code=status.HTTP_201_CREATED)

def create_feed_logs(feed_log: feeding_logs, current_user: str = Depends(get_current_user)):
    try:
        data = feed_log.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = supabase.table("Feeding_logs").insert(data).execute()
        return response.data[0]
    except Exception as error:
        print("Feeding Logs Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating feeding log or feeding log could not be created."
        )

@router.get("/", status_code=status.HTTP_200_OK)

def get_feed_logs(current_user: str = Depends(get_current_user)):
    try:
        response = supabase.table("Feeding_logs").select("*").eq("recorded_by", current_user).execute()
        if not response.data:
            return{
                "status": "success",
                "message": "You have no feeding logs yet. Try creating one.",
                "data": []
            }
        return {"status": "success", "data": response.data}
    except Exception as error:
        print("Feeding Logs Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching feeding logs or feeding logs could not be found."
        )