from fastapi import APIRouter, Depends, status, HTTPException
from schemas import Expenses
from db import supabase
from dependencies import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_expenses(expenses: Expenses, current_user: str = Depends(get_current_user)):
    try:
        data = expenses.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = supabase.table("Expenses").insert(data).select("expense_id, date, category, description, amount, status, created_at").execute()
        return response.data[0]
    except Exception as error:
        print("Expense Creation Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating expense record.",
        )



@router.get("/", status_code=status.HTTP_200_OK)
def get_expenses(current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Expenses")
            .select("expense_id, date, category, description, amount, status, created_at")
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false") 
            .execute()
        )
        
        if not response.data:
            return {
                "status": "Success",
                "message": "You don't have any recorded expenses yet. try creating one",
                "data": [],
            }

        return {"status": "Success", "data": response.data}
    except Exception as error:
        print("Expense Fetch Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching Expenses.",
        )



@router.patch("/{expense_id}", status_code=status.HTTP_200_OK)
def update_expense(
    expense_id: int, updates: Expenses, current_user: str = Depends(get_current_user)
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
            supabase.table("Expenses")
            .update(filtered_updates)
            .eq("expense_id", expense_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select("expense_id, date, category, description, amount, status, created_at")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense record not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Expense update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Expense.",
        )



@router.delete("/{expense_id}", status_code=status.HTTP_200_OK)
def delete_expenses(expense_id: int, current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Expenses")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("expense_id", expense_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found or unauthorized.",
            )

        return {"message": f"Expense with ID {expense_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Expense deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting expense.",
        )