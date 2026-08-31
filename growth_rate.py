from fastapi import APIRouter, Depends, status, HTTPException
from schemas import growth_rate
from db import supabase
from dependencies import get_current_user

router = APIRouter(prefix="/growth", tags=["growth"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_growth_rate(
    Growth_rate: growth_rate, current_user=Depends(get_current_user)
):
    try:
        data = Growth_rate.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = supabase.table("Growth_rate").insert(data).select("id, pond_name, species, sample_date, sample_count, avg_weight, total_feed_used, feed_conversion_rate, specific_growth_rate").execute()
        return response.data[0]
    except Exception as error:
        print("Growth rate creation Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating growth record or record could not be created.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def get_growth_rate(current_user=Depends(get_current_user)):
    try:
        response = (
            supabase.table("Growth_rate").select("id, pond_name, species, sample_date, sample_count, avg_weight, total_feed_used, feed_conversion_rate, specific_growth_rate").eq("recorded_by", current_user).or_("is_deleted.is.null,is_deleted.eq.false").execute()
        )
        if not response.data:
            return {
                "status": "Success",
                "message": "You don't have any growth records set yet, try creating one",
                "data": [],
            }
        return {"status": "Success", "data": response.data}

    except Exception as error:
        print("Fetch Growth rate Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching growth records or records couldn't be found.",
        )


@router.patch("/{growth_id}", status_code=status.HTTP_200_OK)
def update_schedule(
    growth_id: int, updates: growth_rate, current_user: str = Depends(get_current_user)
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
            supabase.table("Growth_rate")
            .update(filtered_updates)
            .eq("id", growth_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select("id, pond_name, species, sample_date, sample_count, avg_weight, total_feed_used, feed_conversion_rate, specific_growth_rate")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Growth record not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Growth rate update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Growth rate.",
        )

@router.delete("/{growth_id}", status_code=status.HTTP_200_OK)
def delete_growth_rate(growth_id: int, current_user: str = Depends(get_current_user)):
    try:
         response = (
            supabase.table("Growth_rate")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("id", growth_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

         if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Growth rate not found or unauthorized.",
            )

         return {"message": f"Growth record with ID {growth_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Growth rate deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting growth records.",
        )
