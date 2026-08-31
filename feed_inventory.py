from fastapi import Depends, APIRouter, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import Feed_inventory

router = APIRouter(prefix="/feed_inventory", tags=["feed_inventory"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_feed_inventory(
    feed_inventory: Feed_inventory, current_user: str = Depends(get_current_user)
):
    try:
        data = feed_inventory.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = (
            supabase.table("Feeds")
            .insert(data)
            .select(
                "feed_id, feed_name, feed_type, quantity, av_weight_per_bag, feed_cost_per_bag, feed_total_cost,supplier, expiry_date, purchase_date, status"
            )
            .execute()
        )
        return response.data[0]
    except Exception as error:
        print("Feed Inventory creation Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating feed inventory or feed inventory could not be created.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def get_feed_inventory(current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Feeds")
            .select(
                "feed_id, feed_name, feed_type, quantity, av_weight_per_bag, feed_cost_per_bag, feed_total_cost,supplier, expiry_date, purchase_date, status"
            )
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            return {
                "status": "Success",
                "message": "No records created for feed inventories yet. try creating one",
                "data": [],
            }

        return {"status": "Success", "data": response.data}
    except Exception as error:
        print("Feed inventory Fetch Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching Inventory records.",
        )


@router.patch("/{feed_inventory_id}", status_code=status.HTTP_200_OK)
def update_feed_inventory(
    feed_inventory_id: int,
    updates: Feed_inventory,
    current_user: str = Depends(get_current_user),
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
            supabase.table("Feeds")
            .update(filtered_updates)
            .eq("feed_id", feed_inventory_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select(
                "feed_id, feed_name, feed_type, quantity, av_weight_per_bag, feed_cost_per_bag, feed_total_cost,supplier, expiry_date, purchase_date, status"
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventories not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Inventories update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating feed Inventory.",
        )


@router.delete("/{feed_inventory_id}", status_code=status.HTTP_200_OK)
def delete_feed_inventory(
    feed_inventory_id: int, current_user: str = Depends(get_current_user)
):
    try:
        response = (
            supabase.table("Feeds")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("feed_id", feed_inventory_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory not found or unauthorized.",
            )

        return {
            "message": f"Feed inventory with ID {feed_inventory_id} deleted successfully."
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Inventory deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting feed inventory.",
        )
