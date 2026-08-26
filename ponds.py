from fastapi import APIRouter, Depends, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import ponds

router = APIRouter(prefix="/ponds", tags=["ponds"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_pond_record(current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Ponds")
            .select(
                "pond_id, pond_name,pond_stock_quantity,species_in_pond,last_harvest_date,pond_type,pond_location,pond_status,water_temp,pond_capacity,pH_level"
            )
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            return {
                "status": "Success",
                "message": "You don't have any recorded pond yet. try creating one",
                "data": [],
            }

        return {"status": "Success", "data": response.data}
    except Exception as error:
        print("Fetch Pond Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching Pond record.",
        )


@router.post("/ponds", status_code=status.HTTP_201_CREATED)
def create_pond(pond: ponds, current_user: str = Depends(get_current_user)):
    try:
        check_existing_pond = (
            supabase.table("Ponds")
            .select("pond_id, pond_name,pond_stock_quantity,species_in_pond,last_harvest_date,pond_type,pond_location,pond_status,water_temp,pond_capacity,pH_level")
            .eq("pond_name", pond.pond_name)
            .eq("recorded_by", current_user)
            .execute()
        )

        if check_existing_pond.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pond with the same name already exists.",
            )

        data = pond.model_dump(mode="json")
        data["recorded_by"] = current_user

        response = supabase.table("Ponds").insert(data).select("pond_id, pond_name,pond_stock_quantity,species_in_pond,last_harvest_date,pond_type,pond_location,pond_status,water_temp,pond_capacity,pH_level").execute()
        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Pond creation error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating pond.",
        )


@router.patch("/{pond_id}", status_code=status.HTTP_200_OK)
def update_pond_record(
    pond_id: int, updates: ponds, current_user: str = Depends(get_current_user)
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
            supabase.table("Ponds")
            .update(filtered_updates)
            .eq("pond_id", pond_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select("pond_id, pond_name,pond_stock_quantity,species_in_pond,last_harvest_date,pond_type,pond_location,pond_status,water_temp,pond_capacity,pH_level")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pond record not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Pond update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Pond record.",
        )



@router.delete("/{pond_id}", status_code=status.HTTP_200_OK)
def delete_pond_record(pond_id: int, current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Ponds")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("pond_id", pond_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pond record not found or unauthorized.",
            )

        return {"message": f"Pond record with ID {expense_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Pond record deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting pond record.",
        )

