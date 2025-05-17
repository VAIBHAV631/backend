from fastapi import APIRouter, Form
from database import get_db_connection

router = APIRouter()

@router.post("/contact")
async def submit_contact_form(
    full_name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    conn = get_db_connection()
    conn.execute(
        '''
        INSERT INTO contact (full_name, email, message)
        VALUES (?, ?, ?)
        ''',
        (full_name, email, message)
    )
    conn.commit()
    conn.close()

    return {"message": "Contact form submitted successfully!"}