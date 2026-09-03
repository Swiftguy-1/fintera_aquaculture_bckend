from fastapi import APIRouter, Depends, HTTPException, status
from auth import require_admin
from database import supabase

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/users/{user_id}/transactions")
def get_user_transactions(user_id: str, admin: dict = Depends(require_admin)):
    try:
        # Fetch transaction history for this specific user
        response = (
            supabase.table("Finance_sales")
            .select("id, user_id, profit, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return {
            "user_id": user_id,
            "transactions": response.data or [],
        }

    except Exception as error:
        print("Error fetching user transactions:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user transaction history",
        )
