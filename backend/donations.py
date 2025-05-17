from fastapi import APIRouter, Form
from database import get_db_connection

router = APIRouter()

@router.post("/donations")
def submit_donation(
    donor_name: str = Form(...),
    donor_email: str = Form(...),
    donor_phone: str = Form(...),
    donation_amount: int = Form(...),
    donation_message: str = Form("")
):
    conn = get_db_connection()
    conn.execute(
        '''
        INSERT INTO donations (full_name, email, phone, amount, message)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (donor_name, donor_email, donor_phone, donation_amount, donation_message)
    )
    conn.commit()
    conn.close()
    return {"message": "Donation submitted successfully"}
