import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import pandas as pd
import json
import time

# Page configuration
st.set_page_config(
    page_title="VOLAR FASHION - Leave Application",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with animations and modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        animation: gradientShift 10s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .form-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 3rem;
        border-radius: 30px;
        box-shadow: 0 30px 80px rgba(0,0,0,0.4);
        margin: 2rem auto;
        max-width: 1000px;
        animation: fadeInUp 0.8s ease;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: slideDown 0.6s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    h2 {
        color: #667eea;
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
        animation: slideDown 0.8s ease;
    }
    
    h3 {
        color: #764ba2;
        font-size: 1.5rem;
        margin-top: 2rem;
        font-weight: 600;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        border-radius: 50px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.2);
        transition: left 0.5s ease;
    }
    
    .stButton>button:hover:before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.7);
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea, .stDateInput>div>div>input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.3rem rgba(102, 126, 234, 0.25);
        transform: scale(1.02);
    }
    
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
        animation: bounceIn 0.6s ease;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .error-message {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(235, 51, 73, 0.3);
        animation: shake 0.5s ease;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
        animation: fadeIn 1s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .loading-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        animation: pulse 2s ease infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(240, 147, 251, 0.4);
    }
    
    .approval-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-approved {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-rejected {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    label {
        font-weight: 600 !important;
        color: #333 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .footer {
        text-align: center;
        color: white;
        padding: 2rem;
        margin-top: 3rem;
        opacity: 0.9;
        animation: fadeIn 2s ease;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 50px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.2);
        border-radius: 30px;
        color: white;
        font-weight: 600;
        padding: 10px 30px;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Superior details dictionary with approval links
SUPERIORS = {
    "Shantanu": "ShindeShantanu732@gmail.com",
    "Roger": "Shinde78617@gmail.com",
    "Priya Sharma": "priya.sharma@volarfashion.com",
    "Rajesh Kumar": "rajesh.kumar@volarfashion.com",
    "Anita Desai": "anita.desai@volarfashion.com",
    "Vikram Singh": "vikram.singh@volarfashion.com"
}

# Email configuration
SENDER_EMAIL = "hrvolarfashion@gmail.com"
SENDER_PASSWORD = "xlbf vfqh corg ijqr"  # Use App Password for Gmail

# Google Sheets configuration
SHEET_NAME = "Leave_Applications"
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Department options
DEPARTMENTS = [
    "Human Resources",
    "Finance",
    "Operations",
    "Sales & Marketing",
    "Production",
    "Quality Control",
    "IT",
    "Design",
    "Administration"
]

def setup_google_sheets():
    """Setup Google Sheets connection"""
    try:
        creds_dict = {
              "type": "service_account",
               "project_id": "peerless-column-439505-k8",
               "private_key_id": "9bd0a51299c21c5fe807930fa34db7ed193727e8",
               "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCljH8lNYK/9uMY\ncoA9qiQhaED5zJuRXiGYl8DbELRYP3ki8CVTShKBqha1GtlVfQXoRZw8cfepV/Co\nCYvkySMJRq4yWXWiwzrft29uPODhKLpSJz2V1sX7D59SW66db0FXDYF6r0QEA8LM\nkp36wh+/WI+XCvJT29fB9qi+cqwDx8F+CNllslGw3pDJe1ZH2tY1vDTmavqfNiDq\nFtMfPsfiNBlyuS6dpFUPyGv/vpQ1lDkS7e86IC4auGiOizeRsHTAttlk/p977ZQE\nnrCuWkDTd8Uvd+1NLM7Bkm7voNWjhXadXG0AslYSzOZ/kqft+2KkdAtPGusC4N/A\nIKr1p5vFAgMBAAECggEAB4GQzEOaW5DaqCOc6+7Yd4lOFOVxkkxF0rDixiwCOVQb\nbnmb/6RGpYlsQSbn/sfN6kOpu1XhiFSb7UqNhMCX7ZY+VLsYqdoXQ8iB7WomOh9K\nH2p3EOGtlV4Wd7n/d1TxjfxnSARFXbc78GGfdxyxKtBdplgRN7sqk7lW2lfBs+Qa\njxbN5ZHt2fvkJzFVpe7A73QySWpaMDYgiAJnJIbT6dvGdqK0LDsTYfnKaAcm1q4y\nFpq3xhcuQisHIjY0zMVrMtO8sd8aOUn983D8UGazh+onnzPhD12Q0nE+PURnjH/T\nQCn2IYp5LkqHdiZ1hCEQo86qh9aa/69I8Hg9dfDwkQKBgQDaOXYjWHtB9g0O2enY\nte/n8elsAxBY4FAJ1NIorvcr9zGOUxMGqG1GhnHgAIr4V67XSE5TiIzsCZoB0nem\nK2NEWYpx0ykTjZ2coQZ86KdZm35Wz45n3GAOtN2vdfDmTlkFVDuXamHUH4HFH9+m\nxdV5MJtCiIEKktQU8cH06VV6nQKBgQDCNLuia3rpqH1/biBYByK5scjmTJ6YvMLK\nRFsYX9PIfEnkeIAM6W8Wt2oSBYdcIQFbsSOlcf/HfGVoTs6ELWEixRWdk9VHqjvf\nULuWrys4Ug/06bY9AkygWFd5FqS1O0u8tmS9VdIlna8AZ8Lim8G8wDGp7t2FF4Es\nLcSBZM6pSQKBgBOPJumQGqwU06LLIUyNMg2F/zfxJlvw7vuSmauP0xObulNZWtEz\n82do0XgUVGBh64fcMTkHeioFyknzhUndha4woFoHZR0dikzpmd1ENQuxBifdvpPM\niseGqn/5gDgEObJilFzD6jTLBiSW8MLP5IxSMPhLp9U8x8mAybOb3k95AoGAZWqE\nUd0u4rZKUzF/UnjneXGOKDX63Gg2kMoBiEkCn7/IFreWpyeAC6zch2y7szDJNMjc\nhJlzqQkdK8t7rSrFfxLMpu18g2Ayw/u0+oufVloEWzFxKYr52QJJK8LXYI0GkBXv\npbAbfelKajvFWfFcyuTTCpris44Ctr9vzuKFyYECgYAoro6JpUbMrcRal+gFT6Ek\nN1495FJDTrAsvGH2Zr1agXgT2xSisOqWaMTeaGDTpeQWlePdmItq+zNb8zY5y9NH\ncyrJUyAvdypjNQ9WXxPKE/sGDvlHMiUUde5IJTgJMY2221AqnrGjhD/tLRfOgqTY\nt3XjBsB/djmo2RjbzngNlg==\n-----END PRIVATE KEY-----\n",
               "client_email": "leave-app-service@peerless-column-439505-k8.iam.gserviceaccount.com",
               "client_id": "111871063783796575744",
               "auth_uri": "https://accounts.google.com/o/oauth2/auth",
               "token_uri": "https://oauth2.googleapis.com/token",
               "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
               "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/leave-app-service%40peerless-column-439505-k8.iam.gserviceaccount.com",

        }
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
        client = gspread.authorize(creds)
        
        try:
            sheet = client.open(SHEET_NAME).sheet1
        except gspread.SpreadsheetNotFound:
            st.error(f"❌ Google Sheet '{SHEET_NAME}' not found!")
            return None
        
        try:
            if sheet.row_count == 0 or sheet.row_values(1) == []:
                headers = [
                    "Submission Date", "Employee Name", "Employee Code", "Department",
                    "Type of Leave", "No of Days", "Purpose of Leave", "From Date",
                    "Till Date", "Superior Name", "Superior Email", "Status", "Approval Date"
                ]
                sheet.append_row(headers)
        except Exception as e:
            pass
        
        return sheet
        
    except Exception as e:
        st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
        return None

def send_approval_email(employee_name, superior_name, superior_email, leave_details, row_number):
    """Send stunning approval request email to superior"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = superior_email
        msg['Subject'] = f"🔔 Leave Approval Request - {employee_name}"
        
        # Get the app URL (will be the Streamlit Cloud URL when deployed)
        app_url = "https://your-app-name.streamlit.app"  # Update this after deployment
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
                body {{
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 40px 20px;
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 30px;
                    overflow: hidden;
                    box-shadow: 0 30px 80px rgba(0,0,0,0.3);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px 30px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5rem;
                    font-weight: 700;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    font-size: 1.1rem;
                    opacity: 0.95;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .greeting {{
                    font-size: 1.3rem;
                    color: #333;
                    margin-bottom: 20px;
                    font-weight: 600;
                }}
                .message {{
                    color: #666;
                    font-size: 1.1rem;
                    line-height: 1.6;
                    margin-bottom: 30px;
                }}
                .details-card {{
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    border-radius: 20px;
                    padding: 30px;
                    margin: 30px 0;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }}
                .detail-row {{
                    display: flex;
                    padding: 15px 0;
                    border-bottom: 1px solid rgba(255,255,255,0.5);
                }}
                .detail-row:last-child {{
                    border-bottom: none;
                }}
                .detail-label {{
                    font-weight: 600;
                    color: #667eea;
                    width: 150px;
                    font-size: 1rem;
                }}
                .detail-value {{
                    color: #333;
                    flex: 1;
                    font-size: 1rem;
                }}
                .action-section {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 20px;
                    padding: 30px;
                    text-align: center;
                    margin: 30px 0;
                    color: white;
                }}
                .action-section h3 {{
                    margin: 0 0 20px 0;
                    font-size: 1.5rem;
                }}
                .button-container {{
                    display: flex;
                    gap: 20px;
                    justify-content: center;
                    margin-top: 20px;
                }}
                .approve-btn, .reject-btn {{
                    padding: 15px 40px;
                    border-radius: 50px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    text-decoration: none;
                    display: inline-block;
                    transition: all 0.3s ease;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
                }}
                .approve-btn {{
                    background: #11998e;
                    color: white;
                }}
                .reject-btn {{
                    background: #eb3349;
                    color: white;
                }}
                .instructions {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 30px 0;
                    color: #856404;
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 0.9rem;
                }}
                .footer-logo {{
                    font-size: 1.5rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 10px;
                }}
                .emoji {{
                    font-size: 3rem;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏢 VOLAR FASHION PVT LTD</h1>
                    <p>Human Resources Management System</p>
                </div>
                
                <div class="content">
                    <div class="emoji">📋</div>
                    <div class="greeting">Dear {superior_name},</div>
                    <div class="message">
                        A new leave application has been submitted and requires your approval. Please review the details below:
                    </div>
                    
                    <div class="details-card">
                        <div class="detail-row">
                            <div class="detail-label">👤 Employee:</div>
                            <div class="detail-value">{leave_details['employee_name']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">🔢 Employee Code:</div>
                            <div class="detail-value">{leave_details['employee_code']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">🏛️ Department:</div>
                            <div class="detail-value">{leave_details['department']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">📋 Leave Type:</div>
                            <div class="detail-value">{leave_details['leave_type']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">📊 Duration:</div>
                            <div class="detail-value">{leave_details['no_of_days']} days</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">📅 From Date:</div>
                            <div class="detail-value">{leave_details['from_date']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">📅 Till Date:</div>
                            <div class="detail-value">{leave_details['till_date']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">📝 Purpose:</div>
                            <div class="detail-value">{leave_details['purpose']}</div>
                        </div>
                    </div>
                    
                    <div class="action-section">
                        <h3>⚡ Take Action Now</h3>
                        <p style="margin: 0; font-size: 1rem;">Click the approval portal link below to review and take action</p>
                    </div>
                    
                    <div class="instructions">
                        <strong>📧 How to Approve/Reject:</strong><br><br>
                        <strong>Option 1: Use the Approval Portal (Recommended)</strong><br>
                        Click here to access the portal: <a href="{app_url}?tab=approval" style="color: #667eea; font-weight: 600;">{app_url}?tab=approval</a><br>
                        Enter the Application ID: <strong style="color: #667eea;">LA-{row_number}</strong><br><br>
                        
                        <strong>Option 2: Update Google Sheet Directly</strong><br>
                        1. Open the Google Sheet: "Leave_Applications"<br>
                        2. Find row #{row_number}<br>
                        3. Change "Status" column to "Approved" or "Rejected"<br>
                        4. Add today's date in "Approval Date" column
                    </div>
                </div>
                
                <div class="footer">
                    <div class="footer-logo">VOLAR FASHION</div>
                    <p>This is an automated email from VOLAR FASHION HR Management System</p>
                    <p style="margin: 5px 0;">📧 hrvolarfashion@gmail.com | 🌐 www.volarfashion.com</p>
                    <p style="font-size: 0.8rem; margin-top: 15px; color: #999;">
                        © 2025 VOLAR FASHION PVT LTD. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

def calculate_days(from_date, till_date, leave_type):
    """Calculate number of days"""
    if leave_type == "Half Day":
        return 0.5
    elif leave_type == "Early Exit":
        return 0.5
    else:
        delta = till_date - from_date
        return delta.days + 1

def update_leave_status(sheet, app_id, status, superior_email):
    """Update leave status in Google Sheet"""
    try:
        # Get all records
        all_records = sheet.get_all_values()
        
        # Find the row with matching application ID (row number)
        for idx, row in enumerate(all_records):
            if idx == 0:  # Skip header
                continue
            
            # Check if this is the right row (row_number = idx + 1)
            if idx + 1 == app_id and row[10] == superior_email:  # Match row and superior email
                # Update status (column 12, index 11)
                sheet.update_cell(idx + 1, 12, status)
                # Update approval date (column 13, index 12)
                sheet.update_cell(idx + 1, 13, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                return True
        
        return False
    except Exception as e:
        st.error(f"Error updating status: {str(e)}")
        return False

# Header with animations
st.markdown("<h1>🏢 VOLAR FASHION PVT LTD</h1>", unsafe_allow_html=True)
st.markdown("<h2>📝 Leave Management Portal</h2>", unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2 = st.tabs(["📝 Submit Application", "✅ Approval Portal"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        employee_name = st.text_input("👤 Employee Name", placeholder="Enter your full name", key="emp_name")
        employee_code = st.text_input("🔢 Employee Code", placeholder="e.g., EMP001", key="emp_code")
        department = st.selectbox("🏛️ Department", ["Select Department"] + DEPARTMENTS, key="dept")
        leave_type = st.selectbox(
            "📋 Type of Leave",
            ["Select Type", "Full Day", "Half Day", "Early Exit"],
            key="leave_type"
        )
    
    with col2:
        from_date = st.date_input("📅 From Date", min_value=datetime.now().date(), key="from_date")
        till_date = st.date_input("📅 Till Date", min_value=datetime.now().date(), key="till_date")
        superior_name = st.selectbox(
            "👔 Superior Name",
            ["Select Superior"] + list(SUPERIORS.keys()),
            key="superior"
        )
        
        if leave_type != "Select Type":
            no_of_days = calculate_days(from_date, till_date, leave_type)
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 0.9rem; opacity: 0.9;">📊 Leave Duration</div>
                    <div style="font-size: 2rem; font-weight: 700; margin-top: 5px;">{no_of_days}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">days</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            no_of_days = 0
    
    purpose = st.text_area(
        "📝 Purpose of Leave",
        placeholder="Please provide a detailed reason for your leave application...",
        height=120,
        key="purpose"
    )
    
    st.markdown("""
        <div class="info-box">
            <strong>ℹ️ Important Information</strong><br>
            • All fields are mandatory<br>
            • Your superior will receive an instant email notification<br>
            • You can track your application status in the Google Sheet<br>
            • Response time: Usually within 24 hours
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Submit Leave Application", key="submit_btn"):
        if not all([employee_name, employee_code, department != "Select Department", 
                    leave_type != "Select Type", purpose, superior_name != "Select Superior"]):
            st.markdown('<div class="error-message">❌ Oops! Please fill all required fields to continue.</div>', 
                       unsafe_allow_html=True)
        elif from_date > till_date:
            st.markdown('<div class="error-message">❌ Invalid dates! "Till Date" must be after or equal to "From Date".</div>', 
                       unsafe_allow_html=True)
        else:
            with st.spinner(''):
                st.markdown("""
                    <div class="loading-container">
                        <h3 style="color: #667eea; margin-bottom: 20px;">🔄 Processing Your Request</h3>
                        <p style="color: #666; font-size: 1.1rem;">📝 Saving application to database...</p>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(1)
                
                submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                superior_email = SUPERIORS[superior_name]
                
                leave_details = {
                    "employee_name": employee_name,
                    "employee_code": employee_code,
                    "department": department,
                    "leave_type": leave_type,
                    "no_of_days": no_of_days,
                    "purpose": purpose,
                    "from_date": from_date.strftime("%Y-%m-%d"),
                    "till_date": till_date.strftime("%Y-%m-%d")
                }
                
                sheet = setup_google_sheets()
                if sheet:
                    row_data = [
                        submission_date,
                        employee_name,
                        employee_code,
                        department,
                        leave_type,
                        no_of_days,
                        purpose,
                        leave_details['from_date'],
                        leave_details['till_date'],
                        superior_name,
                        superior_email,
                        "Pending",
                        ""
                    ]
                    
                    try:
                        sheet.append_row(row_data)
                        row_number = len(sheet.get_all_values())
                        
                        st.markdown("""
                            <div class="loading-container">
                                <h3 style="color: #667eea; margin-bottom: 20px;">📧 Sending Email Notification</h3>
                                <p style="color: #666; font-size: 1.1rem;">Please wait while we notify your superior...</p>
                                <p style="color: #999; font-size: 0.9rem; margin-top: 10px;">This may take a few moments</p>
                            </div>
                        """, unsafe_allow_html=True)
                        time.sleep(2)
                        
                        email_sent = send_approval_email(
                            employee_name,
                            superior_name,
                            superior_email,
                            leave_details,
                            row_number
                        )
                        
                        if email_sent:
                            st.markdown(
                                f'''<div class="success-message">
                                    <h2 style="margin: 0 0 15px 0; font-size: 2rem;">✅ Success!</h2>
                                    <p style="margin: 5px 0; font-size: 1.2rem;">Your leave application has been submitted successfully!</p>
                                    <p style="margin: 5px 0; font-size: 1.1rem;">📧 Email notification sent to {superior_name}</p>
                                    <p style="margin: 15px 0 5px 0; font-size: 0.95rem; opacity: 0.9;">
                                        <strong>Application ID:</strong> LA-{row_number}<br>
                                        <strong>Status:</strong> Pending Approval<br>
                                        <strong>Submitted on:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
                                    </p>
                                </div>''',
                                unsafe_allow_html=True
                            )
                            st.balloons()
                        else:
                            st.markdown(
                                '''<div class="success-message">
                                    ✅ Application submitted successfully!<br>
                                    ⚠️ However, there was an issue sending the email. Please contact HR.
                                </div>''',
                                unsafe_allow_html=True
                            )
                    except Exception as e:
                        st.markdown(
                            f'<div class="error-message">❌ Error submitting application: {str(e)}</div>',
                            unsafe_allow_html=True
                        )

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 👔 Superior Approval Portal")
    st.markdown("Use this portal to approve or reject leave applications")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        app_id_input = st.text_input("🔢 Application ID", placeholder="e.g., LA-15 (enter just the number: 15)", key="app_id")
        superior_email_input = st.text_input("📧 Your Email", placeholder="Enter your registered email", key="sup_email")
    
    with col2:
        action = st.selectbox("✅ Action", ["Select Action", "Approve", "Reject"], key="action")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔄 Process Application", key="process_btn"):
        if not all([app_id_input, superior_email_input, action != "Select Action"]):
            st.markdown('<div class="error-message">❌ Please fill all fields!</div>', unsafe_allow_html=True)
        else:
            try:
                # Extract number from app_id (e.g., "LA-15" or "15" -> 15)
                app_id = int(app_id_input.replace("LA-", "").replace("la-", "").strip())
                
                if superior_email_input not in SUPERIORS.values():
                    st.markdown('<div class="error-message">❌ Email not authorized! Please use your registered superior email.</div>', 
                               unsafe_allow_html=True)
                else:
                    sheet = setup_google_sheets()
                    if sheet:
                        status = "Approved" if action == "Approve" else "Rejected"
                        success = update_leave_status(sheet, app_id, status, superior_email_input)
                        
                        if success:
                            st.markdown(
                                f'''<div class="success-message">
                                    <h2 style="margin: 0 0 15px 0; font-size: 2rem;">✅ Success!</h2>
                                    <p style="margin: 5px 0; font-size: 1.2rem;">Leave application LA-{app_id} has been {status.lower()}!</p>
                                    <p style="margin: 5px 0; font-size: 1rem;">The employee will be notified and the record is updated.</p>
                                </div>''',
                                unsafe_allow_html=True
                            )
                            st.balloons()
                        else:
                            st.markdown('<div class="error-message">❌ Application not found or you are not authorized to approve this application.</div>', 
                                       unsafe_allow_html=True)
            except ValueError:
                st.markdown('<div class="error-message">❌ Invalid Application ID! Please enter only the number (e.g., 15)</div>', 
                           unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📊 Recent Applications")
    
    sheet = setup_google_sheets()
    if sheet:
        try:
            all_data = sheet.get_all_values()
            if len(all_data) > 1:
                df = pd.DataFrame(all_data[1:], columns=all_data[0])
                
                # Filter by superior email if provided
                if superior_email_input and superior_email_input in SUPERIORS.values():
                    df_filtered = df[df['Superior Email'] == superior_email_input].tail(10)
                else:
                    df_filtered = df.tail(10)
                
                if not df_filtered.empty:
                    for idx, row in df_filtered.iterrows():
                        status_class = f"status-{row['Status'].lower()}"
                        st.markdown(f"""
                            <div class="approval-card">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    <h4 style="margin: 0; color: #667eea;">👤 {row['Employee Name']}</h4>
                                    <span class="{status_class}">{row['Status']}</span>
                                </div>
                                <p style="margin: 5px 0; color: #666;"><strong>Code:</strong> {row['Employee Code']} | <strong>Dept:</strong> {row['Department']}</p>
                                <p style="margin: 5px 0; color: #666;"><strong>Type:</strong> {row['Type of Leave']} | <strong>Days:</strong> {row['No of Days']}</p>
                                <p style="margin: 5px 0; color: #666;"><strong>Period:</strong> {row['From Date']} to {row['Till Date']}</p>
                                <p style="margin: 10px 0 5px 0; color: #666;"><strong>Purpose:</strong> {row['Purpose of Leave']}</p>
                                <p style="margin: 5px 0; color: #999; font-size: 0.9rem;"><strong>Submitted:</strong> {row['Submission Date']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("📭 No applications found for your email.")
            else:
                st.info("📭 No leave applications yet.")
        except Exception as e:
            st.error(f"Error loading applications: {str(e)}")

st.markdown("""
    <div class="footer">
        <h3 style="margin: 0 0 10px 0; font-size: 1.8rem; font-weight: 700;">💼 VOLAR FASHION PVT LTD</h3>
        <p style="font-size: 1.1rem; margin: 5px 0;">Human Resources Management System</p>
        <p style="font-size: 1rem; margin: 15px 0 5px 0;">For support and queries:</p>
        <p style="font-size: 1.1rem; font-weight: 600;">📧 hrvolarfashion@gmail.com</p>
        <p style="font-size: 0.9rem; margin-top: 20px; opacity: 0.8;">© 2025 VOLAR FASHION. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)