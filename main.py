from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from admin_auth import verify_password, get_password_hash, create_access_token
from dependencies import get_current_user
from pydantic import BaseModel, EmailStr
from db import supabase
from mortality import router as mortality_router
from harvest import router as harvest_router
from stock_records import router as stock_router
from feed_inventory import router as feed_inventory_router
from feeding_logs import router as feeding_logs_router
from invoice import router as invoice_router
from ponds import router as ponds_router
from feeding_schedule import router as schedule_router
from expenses import router as exp_router
from sales import router as sales_router
from growth_rate import router as growth_router
from users import router as users_router
from user_sales import router as user_sales
from ind_user import router as ind_router
from patch import router as patch_router
from recent_users import router as recent_router
from txns import router as txn_router
from user_mgt import router as mgt_router


app = FastAPI(title="User Dashboard Security System")

ALLOWED_ORIGINS=["fintera-app.vercel.app","https://fintera-aquaculture-bckend.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(mortality_router)
app.include_router(harvest_router)
app.include_router(stock_router)
app.include_router(feed_inventory_router)
app.include_router(feeding_logs_router)
app.include_router(invoice_router)
app.include_router(ponds_router)
app.include_router(schedule_router)
app.include_router(exp_router)
app.include_router(sales_router)
app.include_router(growth_router)
app.include_router(users_router)
app.include_router(user_sales)
app.include_router(ind_router)
app.include_router(patch_router)
app.include_router(recent_router)
app.include_router(txn_router)
app.include_router(mgt_router)


class AdminSignUp(BaseModel):
    fullname: str
    email: EmailStr
    password: str


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(admin_data: AdminSignUp):
    try:
        check_user_existence = (
            supabase.table("admin_table")
            .select("*")
            .eq("email", admin_data.email)
            .eq("name", admin_data.fullname)
            .execute()
        )

        if check_user_existence.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered. Please use a different email or login instead.",
            )

        hashed_admin_pass = get_password_hash(admin_data.password)
        new_admin = {
            "name": admin_data.fullname,
            "email": admin_data.email,
            "password": hashed_admin_pass,
        }

        supabase.table("admin_table").insert(new_admin).execute()
        return {"status": "success", "message": "User registered succesfully"}

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Signup Error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An Error occured during signup",
        )


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_email = form_data.username

        response = (
            supabase.table("admin_table").select("*").eq("email", user_email).execute()
        )

        admin_list = response.data

        if not admin_list:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        db_admin = admin_list[0]

        if not verify_password(form_data.password, db_admin["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": db_admin["email"],"is_admin": db_admin.get("is_admin", False),}
)
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Login Error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured during login",
        )


@app.get("/admin/dashboard")
def dashboard(current_admin: str = Depends(get_current_user)):
    return {
        "status": "success",
        "message": f"Welcome back, {current_admin}! You Have logged into your dashboard successfully.",
        "secret_data": "Sensors Nominal. System Online. All systems operational.",
    }


@app.get("/health")
def health_checkup():
    return {"status": "ok"}
