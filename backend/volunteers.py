from fastapi import APIRouter, Form
from database import get_db_connection

router = APIRouter()

@router.post("/volunteers")
def submit_volunteer(
    vol_name: str = Form(...),
    vol_email: str = Form(...),
    vol_phone: str = Form(...),
    vol_location: str = Form(...),
    vol_message: str = Form(...)
):
    conn = get_db_connection()
    conn.execute(
        '''
        INSERT INTO volunteers (full_name, email, phone, location, reason)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (vol_name, vol_email, vol_phone, vol_location, vol_message)
    )
    conn.commit()
    conn.close()
    return {"message": "Volunteer form submitted successfully"}
