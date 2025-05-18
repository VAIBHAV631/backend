from fastapi import APIRouter, HTTPException, Form, Response
from database import get_db_connection
import hashlib
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
import time

router = APIRouter()
SECRET_KEY = "f3G9zK2aL8pQvX1mN7wR5tY0"
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
    except:
        raise HTTPException(status_code=400, detail="Username already exists.")
    finally:
        conn.close()
    return {"message": "User registered"}



@router.get("/auth-check")
def auth_check(request: Request):
    token = request.cookies.get("token")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"message": "Authenticated", "user": payload["sub"]}
    except:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

@router.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if not user or user["password"] != hash_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    token = jwt.encode({"sub": username, "exp": time.time() + 3600}, SECRET_KEY, algorithm="HS256")

    # Set token in cookie
    response.set_cookie(
    key="token",
    value=token,
    httponly=True,
    samesite="None",  # Must be "None" for cross-site
    secure=True,      # Required for SameSite=None
    path="/",
    domain=".up.railway.app"  # Important: common domain for both frontend and backend
    )

    return {"message": "Login successful"}

@router.post("/forgot-password")
def forgot_password(username: str = Form(...), new_password: str = Form(...)):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    conn.execute("UPDATE users SET password = ? WHERE username = ?", (hash_password(new_password), username))
    conn.commit()
    conn.close()
    return {"message": "Password reset successfully"}


@router.post("/logout")
def logout(response: Response):
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="token")
    return response
