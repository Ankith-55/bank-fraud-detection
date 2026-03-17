from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from fastapi import HTTPException, status
import uuid
class SecurityQuestionsSchema(str, Enum):
    MOTHER_MAIDEN_NAME = "mother_maiden_name"
    CHILDHOOD_FRIEND= "childhood_friend"
    FAVOURITE_COLOR = "favourite_color"
    BIRTH_CITY = "birth_city"
    
    @classmethod
    def get_description(cls, question) -> str:
        descriptions = {
            cls.MOTHER_MAIDEN_NAME: "What is your mother's maiden name?",
            cls.CHILDHOOD_FRIEND: "What is the name of your childhood friend?",
            cls.FAVOURITE_COLOR: "What is your favourite color?",
            cls.BIRTH_CITY: "In which city were you born?"
        }
        return descriptions.get(question, "Unknown security question")

class AccountStatusSchema(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    PENDING = "pending"
    

class RoleChoicesSchema(str, Enum):
    CUSTOMER = "customer"
    ACCOUNT_MANAGER = "account_manager"
    BRANCH_MANAGER = "branch_manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    TELLER = "teller"
    
    
class BaseUserSchema(SQLModel):
    username:str | None = Field(default=None, max_length=12, unique=True)
    email:EmailStr= Field(index=True, unique=True,max_length=255)
    first_name:str= Field(max_length=30)
    middle_name:str | None = Field(default=None, max_length=30)
    last_name:str= Field(max_length=30)
    id_no: int =Field(index=True, gt=0)
    is_active: bool = True
    is_superuser:bool=False
    secuirty_question: SecurityQuestionsSchema = Field(max_length=30)
    account_status: AccountStatusSchema = Field(default=AccountStatusSchema.INACTIVE)
    role:RoleChoicesSchema = Field(default=RoleChoicesSchema.CUSTOMER)
    
    
class UserCreateSchema(BaseUserSchema):
    password:str = Field(min_length=8, max_length=40)
    confirm_password:str = Field(min_length=8, max_length=40)
    @field_validator("confirm_password")
    def validate_passwords(cls, v, values):
        if 'password' in values and v != values['password']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Passwords do not match",
                    "action": "Please ensure that the password you entered match."
                }
            )
        return v
    
    
class UserReadSchema(BaseUserSchema):
    id: uuid.UUID
    full_name: str

class EmailRequestSchema(SQLModel):
    email: EmailStr 

    
class LoginRequestSchema(SQLModel):
    email: EmailStr
    password: str=Field(
        min_length=8, 
        max_length=40, 
    )
    
class OTPVerifyRequestSchema(SQLModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)