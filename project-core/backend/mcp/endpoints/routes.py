from fastapi import APIRouter, Depends, HTTPException, Security, Request, BackgroundTasks
from sqlalchemy.orm import Session
from mcp.db.session import get_db
from app.models import User, Profile, Role, UserPasswordResetToken
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from fastapi.security import APIKeyHeader
import logging
from app.services.auth_logging import log_auth_attempt_sp
import hashlib
import secrets
from datetime import datetime, timedelta
import os
from app.services.email_utils import send_reset_email

# Placeholder for actual provider validation and DB logic

router = APIRouter(
    prefix="/api/v1",
    tags=["Users"]
)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

class UserCreate(BaseModel):
    name: str = Field(..., example="Jane Doe")
    email: EmailStr = Field(..., example="jane@example.com")
    password: str = Field(..., example="securepassword123")

    class Config:
        json_schema_extra = {
            "description": "Request model for creating a new user with password."
        }

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
        json_schema_extra = {
            "description": "Response model for user information."
        }

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="password123")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }

class LoginResponse(BaseModel):
    message: str
    user_id: int
    name: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "user_id": 1,
                "name": "John Doe",
                "email": "john@example.com"
            }
        }

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

@router.post(
    "/users",
    response_model=UserOut,
    summary="Create a new user",
    description="""
Create a new user in the database.

- Validates if the email already exists.
- Creates a profile for the user.
- Hashes the password securely.
- Returns the newly created user's information.

Requires a unique email.
""",
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Security(api_key_header)
):
    logging.info(f"Registration attempt for email: {user.email}")
    logging.info(f"API key provided: {api_key is not None}")
    
    # Check if user already exists
    db_user = db.query(User).filter(User.EmailAddress == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        # Create profile first
        profile = Profile(
            FirstName=user.name.split()[0] if user.name else "",
            LastName=" ".join(user.name.split()[1:]) if len(user.name.split()) > 1 else "",
            EmailAddress=user.email,
            createdBy="system"
        )
        db.add(profile)
        db.flush()  # Get the ProfileID without committing
        
        # Hash password
        hashed_password = hash_password(user.password)
        
        # Get the User role ID
        user_role = db.query(Role).filter(Role.RoleName == "User").first()
        if not user_role:
            raise HTTPException(status_code=500, detail="User role not found in database")
        
        # Create user
        new_user = User(
            Username=user.email,  # Use email as username for now
            EmailAddress=user.email,
            HashedPassword=hashed_password,
            ProfileID=profile.ProfileID,
            RoleID=user_role.RoleID,  # Dynamic role ID
            createdBy="system"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return UserOut(
            id=new_user.UserID,
            name=user.name,
            email=new_user.EmailAddress
        )
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating user: {str(e)}")
        logging.error(f"Error type: {type(e).__name__}")
        import traceback
        logging.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Registration failed. Please try again or use another method.")

@router.post(
    "/auth/login",
    response_model=LoginResponse,
    summary="User login with email and password",
    description="""
Authenticate a user with email and password.

- Validates email exists in database
- Verifies password hash matches
- Returns user information on success
- Logs authentication attempt
""",
)
def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    logging.info("=" * 60)
    logging.info("🔐 LOGIN ATTEMPT STARTED")
    logging.info("=" * 60)
    logging.info(f"📧 Email provided: {login_data.email}")
    logging.info(f"🔑 Password provided: {login_data.password}")
    
    # Find user by email
    user = db.query(User).filter(User.EmailAddress == login_data.email).first()
    if not user:
        logging.error(f"❌ Login failed: Email not found - {login_data.email}")
        logging.info("=" * 60)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    logging.info(f"✅ User found in database:")
    logging.info(f"   User ID: {user.UserID}")
    logging.info(f"   Username: {user.Username}")
    logging.info(f"   Email: {user.EmailAddress}")
    logging.info(f"   Stored hashed password: {user.HashedPassword}")
    logging.info(f"   Profile ID: {user.ProfileID}")
    logging.info(f"   Role ID: {user.RoleID}")
    
    # Verify password
    try:
        logging.info("🔍 PASSWORD VERIFICATION STARTED")
        
        # Extract salt and hash from stored password
        stored_password = user.HashedPassword
        logging.info(f"📦 Stored password format: {stored_password}")
        
        if not stored_password or '$' not in stored_password:
            logging.error(f"❌ Login failed: Invalid password format for user {user.UserID}")
            logging.error(f"   Stored password: '{stored_password}'")
            logging.info("=" * 60)
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        salt, stored_hash = stored_password.split('$', 1)
        logging.info(f"🧂 Extracted salt: {salt}")
        logging.info(f"🔐 Stored hash: {stored_hash}")
        
        # Hash the provided password with the same salt
        logging.info(f"🔄 Hashing provided password with salt...")
        logging.info(f"   Password to hash: {login_data.password}")
        logging.info(f"   Salt to use: {salt}")
        
        hash_obj = hashlib.sha256((login_data.password + salt).encode())
        provided_hash = hash_obj.hexdigest()
        logging.info(f"🔑 Generated hash: {provided_hash}")
        
        logging.info("🔍 COMPARING HASHES:")
        logging.info(f"   Stored hash:    {stored_hash}")
        logging.info(f"   Provided hash:  {provided_hash}")
        logging.info(f"   Match: {stored_hash == provided_hash}")
        
        if provided_hash != stored_hash:
            logging.error(f"❌ Login failed: Invalid password for user {user.UserID}")
            logging.error(f"   Hash mismatch - stored: {stored_hash}, provided: {provided_hash}")
            logging.info("=" * 60)
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        logging.info("✅ PASSWORD VERIFICATION SUCCESSFUL")
        
        # Get user profile for name
        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        user_name = f"{profile.FirstName} {profile.LastName}".strip() if profile else user.Username
        logging.info(f"👤 User name: {user_name}")
        
        # Update last login time
        user.LastLogin = datetime.utcnow()
        db.commit()
        
        logging.info(f"🎉 LOGIN SUCCESSFUL for user {user.UserID}")
        logging.info("=" * 60)
        
        return LoginResponse(
            message="Login successful",
            user_id=user.UserID,
            name=user_name,
            email=user.EmailAddress
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed. Please try again.")

@router.get(
    "/users",
    response_model=List[UserOut],
    summary="Get all users",
    description="""
Fetch a list of all users stored in the database.

This endpoint is useful for:
- Debugging
- Admin management
- Reviewing test data
""",
)
def get_users(
    db: Session = Depends(get_db),
    api_key: str = Security(api_key_header)
):
    return db.query(User).all()

@router.post("/test-echo")
async def test_echo(request: dict):
    print("Received test-echo:", request)
    return request

@router.post("/auth/{provider}", summary="Social login callback handler")
def social_login(provider: str, request: Request, db: Session = Depends(get_db)):
    """
    Handles OAuth callback/token for social login providers (Google, Microsoft, Facebook, Apple).
    Validates the token, logs the attempt, and returns a generic error message on failure.
    """
    try:
        # Extract token from request (assume JSON body with 'token')
        data = request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
        token = data.get("token")
        ip_address = request.client.host if request.client else None
        if not token:
            log_auth_attempt_sp(db, provider, False, "Missing token", None, ip_address)
            raise HTTPException(status_code=400, detail="Login failed. Please try again or use another method.")

        # Validate token with provider (pseudo-code, replace with real validation)
        user_info = None
        if provider == "google":
            # user_info = validate_google_token(token)
            pass
        elif provider == "microsoft":
            # user_info = validate_microsoft_token(token)
            pass
        elif provider == "facebook":
            # user_info = validate_facebook_token(token)
            pass
        elif provider == "apple":
            # user_info = validate_apple_token(token)
            pass
        else:
            log_auth_attempt_sp(db, provider, False, "Unknown provider", None, ip_address)
            raise HTTPException(status_code=400, detail="Login failed. Please try again or use another method.")

        if not user_info:
            log_auth_attempt_sp(db, provider, False, "Token validation failed", None, ip_address)
            raise HTTPException(status_code=401, detail="Login failed. Please try again or use another method.")

        # Call stored procedure to create/update user and manage session (pseudo-code)
        user_id = None  # Replace with actual DB call
        log_auth_attempt_sp(db, provider, True, None, user_id, ip_address)
        return {"message": "Login successful", "user_id": user_id}

    except Exception as e:
        log_auth_attempt_sp(db, provider, False, str(e), None, None)
        raise HTTPException(status_code=400, detail="Login failed. Please try again or use another method.")

@router.post("/auth/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,  # Pydantic model, not Request
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        email = request.email  # Only use the Pydantic model
        print(f"Received forgot password for: {email}")
        user = db.query(User).filter(User.EmailAddress == email).first()
        if user:
            print("User found, generating token...")
            token = UserPasswordResetToken.generate_token()
            expires_at = datetime.utcnow() + timedelta(hours=1)
            reset_token = UserPasswordResetToken(
                UserID=user.UserID,
                Token=token,
                ExpiresAt=expires_at,
                CreatedDate=datetime.utcnow(),
                CreatedBy="system"
            )
            db.add(reset_token)
            db.commit()
            frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
            reset_link = f"{frontend_url}/reset-password?token={token}"
            background_tasks.add_task(send_reset_email, user.EmailAddress, reset_link)
        else:
            print("User not found.")
        return {"message": "If an account with that email exists, a reset link has been sent."}
    except Exception as e:
        import traceback
        print("EXCEPTION:", e)
        traceback.print_exc()
        raise

@router.post("/auth/reset-password")
def reset_password(token: str, password: str, db: Session = Depends(get_db)):
    reset_token = db.query(UserPasswordResetToken).filter(UserPasswordResetToken.token == token).first()
    if not reset_token or reset_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.UserID == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    # Hash new password (reuse your hash_password function)
    user.HashedPassword = hash_password(password)
    db.delete(reset_token)
    db.commit()
    return {"message": "Password has been reset successfully."}
