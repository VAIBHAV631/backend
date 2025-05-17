from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
import auth
from donations import router as donations_router
from volunteers import router as volunteers_router
from contact import router as contact_router
app = FastAPI()
app.include_router(auth.router)
app.include_router(donations_router)
app.include_router(volunteers_router)
app.include_router(contact_router)

# Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Must be explicit for credentials
    allow_credentials=True,  # Allow cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend running"}
