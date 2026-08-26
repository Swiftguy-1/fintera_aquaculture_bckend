from fastapi import APIRouter, HTTPException, status, Depends
from db import supabase
from dependencies import get_current_user
from schemas import feeding_logs

router = APIRouter(prefix="/feeding_logs", tags=["feeding_logs"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_feed_logs(
    feed_log: feeding_logs, current_user: str = Depends(get_current_user)
):
    try:
        data = feed_log.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = supabase.table("Feeding_logs").insert(data).select("log_id, pond_name, species, feed_type, feed_quantity, feeding_date, feed_cost").execute()
        return response.data[0]
    except Exception as error:
        print("Feeding Logs Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating feeding log or feeding log could not be created.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def get_feed_logs(current_user: str = Depends(get_current_user)):
    try:
         response = (
            supabase.table("Feeding_logs")
            .select(
                "log_id, pond_name, species, feed_type, feed_quantity, feeding_date, feed_cost"
            )
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

         if not response.data:
            return {
                "status": "Success",
                "message": "You hav no feed logs yet. Try creating one",
                "data": [],
            }

         return {"status": "Success", "data": response.data}
    except Exception as error:
        print("Feed logs Fetch Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching feed logs.",
        )

@router.patch("/{log_id}", status_code= status.HTTP_200_OK)
def update_feeding_logs(log_id: int, updates: feeding_logs, current_user : str = Depends(get_current_user)):
    try:
        filtered_updates = updates.model_dump(exclude_unset=True, mode="json")

        if not filtered_updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields provided for updates.",
            )

        filtered_updates["updated_by"] = current_user

        response = (
            supabase.table("Feeding_logs")
            .update(filtered_updates)
            .eq("log_id", log_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select(
                 "log_id, pond_name, species, feed_type, feed_quantity, feeding_date, feed_cost"
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feed log records not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Feeding logs update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Feeding log.",
        )
@router.delete("/{log_id}", status_code= status.HTTP_200_OK)
def delete_feeding_logs(log_id: int, current_user: str= Depends(get_current_user)):
    try:
         response = (
            supabase.table("Feeding_logs")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("log_id", log_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

         if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feed log not found or unauthorized.",
            )

         return {"message": f"Expense with ID {log_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Feeding log deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting Feeding logs.",
        )