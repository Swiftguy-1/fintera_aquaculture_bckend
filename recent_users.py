from fastapi import APIRouter, Depends, HTTPException, status
from auth import require_admin
from database import supabase

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/recent-users")
def get_recent_users(
    limit: int = 5, admin: dict = Depends(require_admin)
):
    try:
        response = (
            supabase.table("admin_table")
            .select("id, name, email, created_at")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        return {"recent_users": response.data or []}

    except Exception as error:
        print("Error fetching recent users:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recent users",
        )