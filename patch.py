from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from auth import require_admin
from database import supabase

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


class AccountStatusUpdate(BaseModel):
    is_frozen: bool


@router.patch("/users/{user_id}/status")
def toggle_account_status(
    user_id: str,
    payload: AccountStatusUpdate,
    admin: dict = Depends(require_admin),
):
    try:
        # Update the is_frozen status in admin_table
        response = (
            supabase.table("admin_table")
            .update({"is_frozen": payload.is_frozen})
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        status_text = "frozen" if payload.is_frozen else "unfrozen"
        return {
            "message": f"User account has been successfully {status_text}."
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Error updating user status:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update account status",
        )
