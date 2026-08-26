from fastapi import APIRouter, Depends, status, HTTPException
from schemas import feeding_schedule
from db import supabase
from dependencies import get_current_user

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_schedule(
    Feeding_schedule: feeding_schedule, current_user: str = Depends(get_current_user)
):
    try:
        data = Feeding_schedule.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = (
            supabase.table("feeding_schedule")
            .insert(data)
            .select(
                "id, pond_name, species, feed_type, target_amount, feeding_time, frequency, is_active, note"
            )
            .execute()
        )
        return response.data[0]
    except Exception as error:
        print("Feeding schedule Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating schedule or schedule could not be created.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def get_schedules(current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("feeding_schedule")
            .select(
                "id, pond_name, species, feed_type, target_amount, feeding_time, frequency, is_active, note"
            )
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )
        if not response.data:
            return {
                "status": "Success",
                "message": "You don't have any schedules set yet, try creating one",
                "data": [],
            }
        return {"status": "Success", "data": response.data}

    except Exception as error:
        print("Schedule Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching feeding schedule or schedules couldn't be found.",
        )


@router.patch("/{schedule_id}", status_code=status.HTTP_200_OK)
def update_schedule(
    schedule_id: int,
    updates: feeding_schedule,
    current_user: str = Depends(get_current_user),
):
    try:
        filtered_updates = updates.model_dump(exclude_unset=True, mode="json")

        if not filtered_updates:
            raise HTTPException(
                status=HPPT_400_BAD_REQUEST,
                detail="No valid fields provided for updates",
            )

        response = (
            supabase.table("feeding_schedule")
            .update(filtered_updates)
            .eq("id", schedule_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select(
                "pond_name, species, feed_type, target_amount, feeding_time, frequency, is_active, note"
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record for schedule not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Schedule update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating schedule.",
        )


@router.delete("/{schedule_id}", status_code=status.HTTP_200_OK)
def delete_schedule(schedule_id: int, current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("feeding_schedule")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("id", schedule_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record for schedule not found or unauthorized.",
            )

        return {"message": f"Schedule with ID {schedule_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Schedule deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting feeding schedule.",
        )
