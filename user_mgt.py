from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from dependencies import require_admin
from db import supabase

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/users")
def get_all_users(
    search: Optional[str] = Query(
        None, description="Search users by name or email"
    ),
    admin: dict = Depends(require_admin),
):
    try:
        query = supabase.table("admin_table").select(
            "id, name, email, is_admin, is_frozen, created_at"
        )

        # Apply search filter if a query parameter is provided
        if search:
            query = query.or_(f"name.ilike.%{search}%,email.ilike.%{search}%")

        response = query.execute()

        return {"users": response.data or []}

    except Exception as error:
        print("Error fetching users list:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users list",
        )
