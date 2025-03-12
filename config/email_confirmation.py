import smtplib
from email.mime.text import MIMEText
import jwt
import datetime
from fastapi import HTTPException


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "noreply.hrin@gmail.com"
SMTP_PASSWORD = "tksd pynp dole gzyk"


def send_verification_email(email: str, token: str):
    subject = "HRIN: Confirm your email"
    body = f"Click the link to confirm your email: http://localhost:8000/verifications/{token}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, email, msg.as_string())


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def generate_email_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_email_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")