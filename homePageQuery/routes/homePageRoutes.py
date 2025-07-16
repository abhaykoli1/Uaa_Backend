import json
import os
import smtplib
from fastapi import APIRouter
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from homePageQuery.models.homePageQuery import HomeQueryModel, HomeQueryTable
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()
# --- SMTP CONFIG ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") 


def send_email(to_email, name ,total_queries):
    
    print(f"SMTP_EMAIL: {SMTP_EMAIL}")
    print(f"SMTP_PASSWORD: {'*' * len(SMTP_PASSWORD) if SMTP_PASSWORD else 'None'}")
    print(f"SMTP_PASSWORD: " , SMTP_PASSWORD)

    subject = "Thank you for your query!"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Thank You</title>
        <style>
          body {{
            margin: 0;
            padding: 0;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #f7f7f7;
            color: #333;
          }}
          .container {{
            max-width: 600px;
            margin: 40px auto;
            background-color: #fff;
            padding: 20px 30px;
            text-align: center;
            border-radius: 8px;
            box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.05);
          }}
          .logo img {{
            height: 130px;
          }}
          h1 {{
            font-size: 22px;
            margin-bottom: 20px;
          }}
          p {{
            font-size: 16px;
            line-height: 1.6;
          }}
          .highlight {{
            color: red;
            text-decoration: none;
          }}
          .line {{
            border-top: 1px solid #ccc;
            margin: 30px 0;
          }}
          .social-icons {{
            margin: 20px 0;
          }}
          .social-icons a {{
            display: inline-block;
            margin: 0 8px;
          }}
          .social-icons img {{
            width: 35px;
            height: 35px;
            border-radius: 50%;
          }}
          .footer {{
            font-size: 14px;
            color: #888;
            margin-top: 40px;
          }}
          .footer a {{
            color: #888;
            text-decoration: none;
            margin: 0 5px;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="logo">
            <img src="https://blackwhite.blr1.digitaloceanspaces.com/UAASITE/b682c444-9393-4683-a71f-0bbe40a4d34d.png" alt="UAA Logo" />
          </div>
          <h1>Thank you for reaching out, {name}!</h1>
          <p>There are currently <strong>10,5{total_queries}</strong> people ahead of you.</p>
          <div class="line"></div>
          <h3>Want to get in sooner?</h3>
          <p>
            Recommend for Academic Help to your friends using this link: <br />
            <a target="_blank" href="https://uniacademicassistance.in" class="highlight">https://uniacademicassistance.in</a>
          </p>
          <div class="social-icons">
            <a href="https://www.instagram.com/uniassignassets" target="_blank">
              <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram" />
            </a>
            <a href="https://www.facebook.com/yourpage" target="_blank">
              <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" />
            </a>
          </div>
          <div class="footer">
            &copy; 2022 <a href="https://uniacademicassistance.in">Uni Academic Assistance.</a>
            <div>All rights reserved.</div>
          </div>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # Attach HTML version
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
    except Exception as e:
        print(f"Email sending failed: {e}")


# --- Route to Add Query ---
@router.post("/api/v1/add-home-query")
async def addHomeQuery(body: HomeQueryModel):
    print(body)
  
    
 # Save the new query
    savedata = HomeQueryTable(**body.dict())
    savedata.save()

    # Get the updated count after saving
    total_queries = HomeQueryTable.objects.count()
    
    # Send email with count
    send_email(body.email, body.name, total_queries)

    # Send Email

    return {
        "message": "Query Added and email sent",
        "status": 200
    }

# --- Route to Get All Queries ---
@router.get("/api/v1/get-all-queries")
async def getAllQueries():
    findata = HomeQueryTable.objects.all()
    print(len(findata)) 
    return {
        "message": "All Queries",
        "data": json.loads(findata.to_json()),
        "status": 200
    }
