from fastapi import APIRouter, Depends, HTTPException, status
from auth import require_admin
from database import supabase

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/total_users", status_code=status.HTTP_200_OK)
def get_total_users(admin: dict = Depends(require_admin)):
    try:
        response = (
            supabase.table("admin_table").select("id", count="exact").execute()
        )

        total_users = response.count if response.count is not None else 0
        active_users = total_users 
        return {
            "total_users": total_users,
            "active_users": active_users,
        }

    except Exception as error:
        print("Error fetching total users:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch total users metric",
        )
