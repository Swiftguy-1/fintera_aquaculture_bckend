from fastapi import APIRouter, Depends, HTTPException, status
from db import supabase
from dependencies import get_current_user
from schemas import invoices

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: invoices, current_user: str = Depends(get_current_user)):
    try:
        data = invoice.model_dump(mode="json")
        data["recorded_by"] = current_user
        response = supabase.table("Invoices").insert(data).select("invoice_id, customer, date, due_date, amount, status").execute()
        return response.data[0]
    except Exception as error:
        print("Invoice Error Details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating invoice or invoice could not be created.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def get_invoices(current_user: str = Depends(get_current_user)):
    try:

        response = (
            supabase.table("Invoices")
            .select("invoice_id, customer, date, due_date, amount, status")
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .eq("recorded_by", current_user)
            .execute()
        )

        if not response.data:
            return {
                "status": "Success",
                "message": "You don't have any recorded invoices yet, try creating one",
                "data": [],
            }

        return {"status": "Success", "data": response.data}

    except Exception as error:
        print("Invoice Error Details:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching invoices or Invoices couldn't be found.",
        )


@router.patch("/{invoice_id}", status_code=status.HTTP_200_OK)
def update_invoice(
    invoice_id: int, updates: invoices, current_user: str = Depends(get_current_user)
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
            supabase.table("Invoices")
            .update(filtered_updates)
            .eq("invoice_id", invoice_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .select("invoice_id, customer, date, due_date, amount, status")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice record not found or unauthorized.",
            )

        return response.data[0]

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Invoice record update error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating Invoice record.",
        )


@router.delete("/{invoice_id}", status_code=status.HTTP_200_OK)
def delete_invoice(invoice_id: int, current_user: str = Depends(get_current_user)):
    try:
        response = (
            supabase.table("Invoices")
            .update({"is_deleted": True, "deleted_by": current_user})
            .eq("invoice_id", invoice_id)
            .eq("recorded_by", current_user)
            .or_("is_deleted.is.null,is_deleted.eq.false")
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice record not found or unauthorized.",
            )

        return {"message": f"Invoice record with ID {invoice_id} deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Invoice record deletion error details:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting invoice record.",
        )