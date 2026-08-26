from fastapi import APIRouter, Depends, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import harvest

router = APIRouter(prefix="/harvest", tags=["harvest"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_harvest_record(
    harvest_record: harvest, current_user: str = Depends(get_current_user)
):
    try:
        data = harvest_record.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = (
            supabase.table("Harvest")
            .insert(data)
            .select(
                "id, pond_name, species, harvest_quantity, total_weight, harvest_date, method_of_harvest"
            )
            .execute()
        )
        return response.data[0]
    except Exception as error:
        print("Harvest Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating harvest record or record could not be created.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def get_harvest_records(current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Harvest")
            .select(
                "id, pond_name, species, harvest_quantity, total_weight, harvest_date, method_of_harvest"
            )
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )
        if not response.data:
            return {
                "status": "success",
                "message": "You have no Harvest records yet. Try creating one.",
                "data": [],
            }
        return {"status": "success", "data": response.data}
    except Exception as error:
        print("Harvest Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching harvest records or records could not be found.",
        )


@router.patch("/{harvest_id}", status_code=status.HTTP_200_OK)
def update_harvest_records(
    harvest_id: int, updates: harvest, current_user: str = Depends(get_current_user)
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
            supabase.table("Harvest")
            .update(filtered_updates)
            .eq("id", harvest_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select(
                "id, pond_name, species, harvest_quantity, total_weight, harvest_date, method_of_harvest"
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Harvest record not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Harvest update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Harvest records",
        )


@router.delete("/{harvest_id}", status_code=status.HTTP_200_OK)
def delete_harvest_records(
    harvest_id: int, current_user: str = Depends(get_current_user)
):
    try:
        response = (
            supabase.table("Harvest")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("id", harvest_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Narvest record not found or unauthorized.",
            )

        return {"message": f"Harvest record with ID {harvest_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Harvest record deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting Harvest record.",
        )
