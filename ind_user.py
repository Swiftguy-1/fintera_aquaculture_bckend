from fastapi import APIRouter, Depends, HTTPException, status
from auth import require_admin
from database import supabase

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/users/{user_id}")
def get_user_details(user_id: str, admin: dict = Depends(require_admin)):
    try:
        # 1. Fetch individual user profile from admin_table
        user_res = (
            supabase.table("admin_table")
            .select("id, name, email, is_admin, is_frozen, created_at")
            .eq("id", user_id)
            .execute()
        )

        if not user_res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user_info = user_res.data[0]

        # 2. Fetch profit records specific to this user from Finance_sales
        sales_res = (
            supabase.table("Finance_sales")
            .select("profit")
            .eq("user_id", user_id)
            .execute()
        )
        sales_data = sales_res.data or []

        # Total revenue is the sum of profit values for this user
        total_revenue = sum(
            float(item["profit"])
            for item in sales_data
            if item.get("profit") is not None
        )

        # Setting total_sales = total_revenue
        total_sales = total_revenue

        return {
            "user": {
                "id": user_info.get("id"),
                "name": user_info.get("name"),
                "email": user_info.get("email"),
                "is_frozen": user_info.get("is_frozen", False),
                "is_admin": user_info.get("is_admin", False),
                "created_at": user_info.get("created_at"),
                "total_sales": total_sales,
                "total_revenue": total_revenue,
            }
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Error fetching user details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user details",
        )
