from fastapi import APIRouter, Depends, status, HTTPException
from schemas import Sales
from db import supabase
from dependencies import get_current_user

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_sale_record(sales: Sales, current_user: str = Depends(get_current_user)):
    try:
        data = sales.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = supabase.table("Finance_sales").insert(data).select("sales_id, date, customer, cost, species, quantity, total_weight, status, profit").execute()
        return response.data[0]
    except Exception as error:
        print("Sales Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating a sale record or sale could not be recorded.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def get_sale_record(current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Finance_sales")
            .select("sales_id, date, customer, cost, species, quantity, total_weight, status, profit")
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false") 
            .execute()
        )
        if not response.data:
            return {
                "status": "Success",
                "message": "You don't have any recorded Sales yet, try recording a Sale",
                "data": [],
            }
        return {"status": "Success", "data": response.data}

    except Exception as error:
        print("Sale record Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching sale record or couldn't be sale record found.",
        )


@router.patch("/{sales_id}", status_code=status.HTTP_200_OK)
def update_sales_record(
    sales_id: int, updates: Sales, current_user: str = Depends(get_current_user)
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
            supabase.table("Finance_sales")
            .update(filtered_updates)
            .eq("sales_id", sales_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select("sales_id, date, customer, cost, species, quantity, total_weight, status, profit")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sales record not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Sales update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Sales.",
        )

       
@router.delete("/{sales_id}", status_code=status.HTTP_200_OK)
def delete_sales_record(sales_id: int, current_user: str = Depends(get_current_user)):
    try:
         response = (
            supabase.table("Finance_sales")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("sales_id", sales_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

         if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sales not found or unauthorized.",
            )

         return {"message": f"Sales record with ID {expense_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Sales deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting Sale record.",
        )
        