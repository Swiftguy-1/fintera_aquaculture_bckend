from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from admin_auth import verify_password, create_access_token 
from dependencies import get_current_user
from pydantic import BaseModel, EmailStr
from db import supabase

app=FastAPI(title="Admin Dashboard Security system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AdminSignIn(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        response = supabase.table("admin_table").select("*").eq("user_name", form_data.username).execute()
        admin_list = response.data
        if not admin_list:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Usrname or password",
                headers={"WWW-Authenticate": "Bearer"},

            )
        db_admin= admin_list[0]

        if not verify_password(form_data.password, db_admin["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token= create_access_token(data={"sub": db_admin["user_name"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as error:
        print("Auth Error:", error)
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured during authentication"
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