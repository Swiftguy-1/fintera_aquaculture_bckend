from fastapi import APIRouter, HTTPException, status, Depends
from dependencies import get_current_user
from supabase import Client
from schemas import Finance_sales, Finance_cost, ponds, Fish_stock
from db import supabase
router= APIRouter()


@router.get("/ponds")
def get_ponds(current_user: str = Depends(get_current_user)):
    try:
        response1 = supabase.table("Ponds").select("*").eq("recorded_by", current_user).eq("is_deleted", False).execute()
        return response1.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching ponds data.")

@router.post("/ponds", status_code=status.HTTP_201_CREATED)
def create_pond(pond: ponds, current_user: str = Depends(get_current_user)):
    try:
        check_existing_pond = supabase.table("Ponds").select("*").eq("pond_name", pond.pond_name).eq("recorded_by", current_user).execute()

        if check_existing_pond.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Pond with the same name already exists."
            )

        data = pond.model_dump(mode='json')
        data["recorded_by"] = current_user

        response = supabase.table("Ponds").insert(data).execute()
        return response.data[0]
        
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Pond creation error details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating pond.")

@router.patch("/ponds/{pond_id}", status_code=status.HTTP_200_OK)
def update_pond(pond_id: int, updates: dict, current_user: str = Depends(get_current_user)):
    try:
        # Check if record exists and belongs to this user
        existing = supabase.table("Ponds").select("*").eq("id", pond_id).eq("recorded_by", current_user).execute()
        if not existing.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pond not found or unauthorized.")

        # Attach updated_by tag alongside updates
        updates["updated_by"] = current_user
        response = supabase.table("Ponds").update(updates).eq("id", pond_id).eq("recorded_by", current_user).execute()
        return response.data[0]
        
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Pond update error details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating pond.")

@router.delete("/ponds/{pond_id}", status_code=status.HTTP_200_OK)
def delete_pond(pond_id: int, current_user: str = Depends(get_current_user)):
    try:
        # Check if record exists and belongs to this user
        existing = supabase.table("Ponds").select("*").eq("id", pond_id).eq("recorded_by", current_user).execute()
        if not existing.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pond not found or unauthorized.")

        # Soft delete record
        response = supabase.table("Ponds").update({"is_deleted": True, "deleted_by": current_user}).eq("id", pond_id).eq("recorded_by", current_user).execute()
        return {"message": f"Pond with ID {pond_id} deleted successfully."}
        
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Pond deletion error details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting pond.")
@router.get("/cost")
def get_cost():
    response3 = supabase.table("Finance_cost").select("*").execute()
    print("Response from Finance_cost table:", response3)
    try:
        if response3 is not None:
            return response3.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching cost data or cost could not be found.")

@router.get("/sales")
def get_sales():
    response4 = supabase.table("Finance_sales").select("*").execute()
    print("Response from Finance_sales table:", response4)
    try:
        if response4 is not None:
            return response4.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching sales data or sales could not be found.")

@router.get("/fish_stock")
def get_fish_stock():
    response5 = supabase.table("Fish_Stock").select("*").execute()
    print("Response from Fish_Stock table:", response5)
    try:
        if response5 is not None:
            return response5.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching fish stock data or fish stock could not be found.")

