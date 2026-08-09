from fastapi import APIRouter, HTTPException, status
from supabase import Client
from schemas import Feeds, Finance_sales, Finance_cost, ponds, Fish_stock
from db import supabase
router= APIRouter()


@router.get("/ponds")
def get_ponds():
    response1 = supabase.table("Ponds").select("*").execute()
    print("Response from Ponds table:", response1)
    try:
        if response1 is not None:
            return response1.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching ponds data or ponds could not be found.")

@router.post("/ponds", status_code=201)
def create_pond(pond: ponds):
    try:
        check_existing_pond = supabase.table("Ponds").select("*").eq("pond_name", pond.pond_name).execute()

        if check_existing_pond.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Pond with the same name already exists."
            )

        data = pond.model_dump(mode='json')
        response = supabase.table("Ponds").insert(data).execute()
        return response.data[0]
        
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Pond creation error details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating pond or pond could not be created.")
@router.patch("/ponds/{pond_id}", status_code=200)
def update_pond(pond_id: int, updates: dict):
    try:
        response = supabase.table("Ponds").update(updates).eq("id", pond_id).execute()
        return response.data
    except Exception as error:
        print("Pond update error details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating pond or pond could not be updated.")
    
@router.delete("/ponds/{pond_id}", status_code=200)
def delete_pond(pond_id: int):
    try:
        response = supabase.table("Ponds").update({"is_deleted": True}).eq("id", pond_id).execute()
        return {"message": f"Pond with ID {pond_id} has been deleted successfully."}
    except Exception as error:
        print("Pond deletion error details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting pond or pond could not be deleted.")

@router.get("/feeds")
def get_feeds():
    response2 = supabase.table("Feeds").select("*").execute()
    print("Response from Feeds table:", response2)
    try:
        if response2 is not None:
            return response2.data
    except Exception as error:
        print("Error Details:", error)  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching feeds data or feeds could not be found.")

@router.get("/cost")
def get_cost():
    response3 = supabase.table("Finance_cost").select("*").execute()
    print("Response from Finance_cost table:", response3)
    try:
        if response3 is not None:
            return response3.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching cost data or cost could not be found.")

@router.get("/sales")
def get_sales():
    response4 = supabase.table("Finance_sales").select("*").execute()
    print("Response from Finance_sales table:", response4)
    try:
        if response4 is not None:
            return response4.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching sales data or sales could not be found.")

@router.get("/fish_stock")
def get_fish_stock():
    response5 = supabase.table("Fish_Stock").select("*").execute()
    print("Response from Fish_Stock table:", response5)
    try:
        if response5 is not None:
            return response5.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching fish stock data or fish stock could not be found.")

@router.get("/mortality_logs")
def get_mortality_logs():
    response6 = supabase.table("Mortality_Logs").select("*").execute()
    print("Response from Mortality_Logs table:", response6)
    try:
        if response6 is not None:
            return response6.data
    except Exception as error:
        print("Error Details:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching mortality logs data or mortality logs could not be found.")