from fastapi import APIRouter, Depends, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import mortality

router = APIRouter(prefix="/mortality", tags=["mortality"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def record_mortality(record: mortality, current_user: str = Depends(get_current_user)):
    try:
        data= record.model_dump()
        data["recorded_by"] = current_user

        response = supabase.table("Mortality_logs").insert(data).select("id, pond_name, Mortality_count, suspected_cause, species").execute()
        return {"status": "success", "data": response.data}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/")
def get_mortality_records(current_user: dict = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Mortality_logs")
            .select("id, pond_name, Mortality_count, suspected_cause, species")
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )
        if not response.data:
            return {
                "status": "success",
                "message": "You have no mortality records yet. Try creating one.",
                "data": [],
            }
        return {"status": "success", "data": response.data}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/{mortality_id}", status_code=status.HTTP_200_OK)
def update_mortality_record(
    mortality_id: int, updates: mortality, current_user: str = Depends(get_current_user)
):
    try:
        filtered_updates = updates.model_dump(exclude_unset=True, mode="json")

        if not filtered_updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields provided for updates.",
            )

        filtered_updates["updated_by"] = current_user

        response = (
            supabase.table("Mortality_logs")
            .update(filtered_updates)
            .eq("id", mortality_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select("id, pond_name, Mortality_count, suspected_cause, species")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mortality record not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Mortality record update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Mortality records.",
        )


@router.delete("/{mortality_id}", status_code=status.HTTP_200_OK)
def delete_mortality_logs(
    mortality_id: int, current_user: str = Depends(get_current_user)
):
    try:
        response = (
            supabase.table("Mortality_logs")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("id", mortality_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mortality record not found or unauthorized.",
            )

        return {"message": f"Mortality record with ID {mortality_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Mortality record deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting Mortality record.",
        )
