from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from admin_auth import verify_password, get_password_hash, create_access_token 
from dependencies import get_current_user
from pydantic import BaseModel, EmailStr
from db import supabase

app=FastAPI(title="User Dashboard Security System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AdminSignUp(BaseModel):
    fullname: str
    email: EmailStr
    password: str

@app.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(admin_data: AdminSignUp):
    try:
        check_user_existence= (
            supabase.table("admin_table")
            .select("*")
            .eq("email", admin_data.email)
            .eq("name", admin_data.fullname)
            .execute()
        )

        if check_user_existence.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        hashed_admin_pass= get_password_hash(admin_data.password)
        new_admin= {
            "name": admin_data.fullname,
            "email": admin_data.email,
            "password": hashed_admin_pass
        }

        supabase.table("admin_table").insert(new_admin).execute()
        return {"status": "success", "message": "User registered succesfully"}
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Signup Error:", error)
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An Error occured during signup"
        )



@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_email = form_data.username

        response = (
            supabase.table("admin_table")
            .select("*")
            .eq("email", user_email)
            .execute()
        )
        return {'Message': "User logged in successfully"}

        admin_list = response.data

        if not admin_list:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
        )

        db_admin= admin_list[0]

        if not verify_password(form_data.password, db_admin["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}

            )
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print("Login Error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured during login"
        )


@app.get('/admin/dashboard')
def dashboard(current_admin: str = Depends(get_current_user)):
    return {
      "status": "success",
      "message": f'Welcome back, {current_admin}! You Have entered the admin dashboard successfully.',
      "secret_data": "Sensors Nominal. System Online. All systems operational."
    }  

@app.get("/health")
def health_checkup():
    return{"status": "ok"}