from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import require_admin
from db import supabase

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/revenue-stats", status_code=status.HTTP_200_OK)
def get_revenue_stats(admin: dict = Depends(require_admin)):
    try:
        response = supabase.table("Finance_sales").select("profit").execute()
        sales_data = response.data or []
        total_revenue = sum(
            float(item["profit"])
            for item in sales_data
            if item.get("profit") is not None
        )

        total_sales = total_revenue

        return {
            "total_sales": total_sales,
            "total_revenue": total_revenue,
        }

    except Exception as error:
        print("Error fetching revenue stats:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch revenue and sales metrics",
        )
