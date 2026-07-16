from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
admin_password= "key."
print(pwd_context.hash(admin_password[:72]))