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
import secrets
import string

# Page configuration
st.set_page_config(
    page_title="VOLAR FASHION - Leave Management",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Beautiful Elegant CSS with Premium Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8f9ff 0%, #f5f7fa 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8f9ff 0%, #f5f7fa 100%);
        background-attachment: fixed;
    }
    
    .form-container {
        background: white;
        padding: 3.5rem;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(103, 58, 183, 0.08);
        margin: 2rem auto;
        max-width: 1000px;
        border: 1px solid rgba(103, 58, 183, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .form-container:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #673ab7, #9c27b0, #2196f3);
    }
    
    h1 {
        background: linear-gradient(135deg, #673ab7 0%, #2196f3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.2rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        font-family: 'Playfair Display', serif;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #5a6c7d;
        text-align: center;
        font-size: 1.6rem;
        margin-bottom: 3rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
        opacity: 0.9;
    }
    
    h3 {
        color: #4a5568;
        font-size: 1.4rem;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        position: relative;
        padding-bottom: 10px;
    }
    
    h3:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #673ab7, #9c27b0);
        border-radius: 2px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #673ab7 0%, #9c27b0 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.1rem;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(103, 58, 183, 0.25);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    
    .stButton>button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        100% {
            transform: scale(20, 20);
            opacity: 0;
        }
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(103, 58, 183, 0.35);
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>select, 
    .stTextArea>div>div>textarea, .stDateInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.875rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #fafbfc;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, 
    .stTextArea>div>div>textarea:focus, .stDateInput>div>div>input:focus {
        border-color: #673ab7;
        box-shadow: 0 0 0 4px rgba(103, 58, 183, 0.1);
        background: white;
        outline: none;
    }
    
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        color: #155724;
        padding: 1.75rem;
        border-radius: 16px;
        text-align: center;
        font-weight: 500;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.1);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
        color: #721c24;
        padding: 1.75rem;
        border-radius: 16px;
        text-align: center;
        font-weight: 500;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(220, 53, 69, 0.1);
        animation: shake 0.5s ease;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        color: #0d47a1;
        padding: 1.75rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(33, 150, 243, 0.1);
    }
    
    .thumbsup-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 4px solid #4caf50;
        color: #2e7d32;
        padding: 1.75rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.1);
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(156, 39, 176, 0.1);
        border: 1px solid rgba(156, 39, 176, 0.1);
    }
    
    .approval-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .status-pending {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 0.5rem 1.25rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(255, 193, 7, 0.3);
    }
    
    .status-approved {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 0.5rem 1.25rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(40, 167, 69, 0.3);
    }
    
    .status-rejected {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 0.5rem 1.25rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(220, 53, 69, 0.3);
    }
    
    label {
        font-weight: 600 !important;
        color: #4a5568 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
        display: block;
    }
    
    .stTextInput>div>label, .stSelectbox>div>label, 
    .stTextArea>div>label, .stDateInput>div>label {
        color: #4a5568 !important;
        font-weight: 600 !important;
    }
    
    .footer {
        text-align: center;
        color: #718096;
        padding: 3rem 2rem;
        margin-top: 4rem;
        position: relative;
    }
    
    .footer:before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #673ab7, transparent);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: white;
        padding: 12px;
        border-radius: 16px;
        border: 1px solid rgba(103, 58, 183, 0.1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 12px;
        color: #718096;
        font-weight: 500;
        padding: 12px 28px;
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #673ab7 0%, #9c27b0 100%);
        color: white;
        border-color: #673ab7;
        box-shadow: 0 4px 12px rgba(103, 58, 183, 0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .password-field {
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
        font-weight: 600;
        color: #673ab7;
    }
    
    .company-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 15px 40px rgba(103, 58, 183, 0.08);
        border: 1px solid rgba(103, 58, 183, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .company-header:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #673ab7, #9c27b0, #2196f3);
    }
    
    .glass-effect {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #673ab7 0%, #2196f3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .icon-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, #673ab7 0%, #9c27b0 100%);
        color: white;
        margin-right: 12px;
        font-size: 1.2rem;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f1f5f9;
    }
    
    .floating-element {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .sparkle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: white;
        border-radius: 50%;
        animation: sparkle 2s infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #673ab7 0%, #9c27b0 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5e35b1 0%, #8e24aa 100%);
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background: #673ab7;
        opacity: 0;
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.9rem;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #673ab7 0%, #9c27b0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .thumbsup-emoji {
        font-size: 3rem;
        animation: thumbsupAnimation 2s ease-in-out infinite;
    }
    
    @keyframes thumbsupAnimation {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.1) rotate(-5deg); }
        50% { transform: scale(1.2) rotate(5deg); }
        75% { transform: scale(1.1) rotate(-5deg); }
    }
    </style>
""", unsafe_allow_html=True)

# Superior details dictionary
SUPERIORS = {
 
    "Shantanu": "s37@vfemails.com",
    "Ayushi": "ayushi@volarfashion.in",

}

# Email configuration
SENDER_EMAIL = "hrvolarfashion@gmail.com"
SENDER_PASSWORD = "xlbf vfqh corg ijqr"

# Google Sheets configuration
SHEET_NAME = "Leave_Applications"
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Department options
DEPARTMENTS = [
    "Human Resources",
    "Finance",
    "Ecom",
    "Graphic Design",
    "Sales and Marketing",
    "Quality Control",
    "IT",
    "Administration"
]

def generate_approval_password():
    """Generate a 12-digit alphanumeric password"""
    alphabet = string.ascii_uppercase + string.digits
    # Remove confusing characters (0, O, 1, I, L)
    alphabet = alphabet.replace('0', '').replace('O', '').replace('1', '').replace('I', '').replace('L', '')
    return ''.join(secrets.choice(alphabet) for _ in range(5))

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
        
        # Check if headers exist, add them if not
        try:
            if sheet.row_count == 0 or not sheet.row_values(1):
                headers = [
                    "Submission Date", "Employee Name", "Employee Code", "Department",
                    "Type of Leave", "No of Days", "Purpose of Leave", "From Date",
                    "Till Date", "Superior Name", "Superior Email", "Status", 
                    "Approval Date", "Approval Password"
                ]
                sheet.append_row(headers)
        except Exception as e:
            pass
        
        return sheet
        
    except Exception as e:
        st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
        return None

def calculate_days(from_date, till_date, leave_type):
    """Calculate number of days"""
    if leave_type == "Half Day":
        return 0.5
    elif leave_type == "Early Exit":
        return "N/A"  # Changed for Early Exit
    else:
        delta = till_date - from_date
        return delta.days + 1

def send_approval_email(employee_name, superior_name, superior_email, leave_details, approval_password):
    """Send beautiful approval request email to superior"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"VOLAR FASHION HR <{SENDER_EMAIL}>"
        msg['To'] = superior_email
        msg['Subject'] = f"✨ Leave Approval Required: {employee_name}"
        
        app_url = "https://hr-application-rtundoncudkzt9efwnscey.streamlit.app/"
        
        # Determine duration display
        if leave_details['leave_type'] == 'Early Exit':
            duration_display = 'N/A'
        else:
            duration_display = f"{leave_details['no_of_days']} days"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
                body {{
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #f8f9ff 0%, #f5f7fa 100%);
                    margin: 0;
                    padding: 40px 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 24px;
                    overflow: hidden;
                    box-shadow: 0 20px 60px rgba(103, 58, 183, 0.1);
                    border: 1px solid rgba(103, 58, 183, 0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #673ab7 0%, #9c27b0 100%);
                    padding: 40px 30px;
                    text-align: center;
                    color: white;
                    position: relative;
                    overflow: hidden;
                }}
                .header:before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #ff9800, #ff5722);
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                    letter-spacing: -0.5px;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    font-size: 16px;
                    opacity: 0.9;
                }}
                .content {{
                    padding: 40px;
                }}
                .greeting {{
                    font-size: 18px;
                    color: #333;
                    margin-bottom: 25px;
                    line-height: 1.6;
                }}
                .details-card {{
                    background: #f8f9ff;
                    border-radius: 16px;
                    padding: 30px;
                    margin: 30px 0;
                    border: 1px solid rgba(103, 58, 183, 0.1);
                }}
                .detail-item {{
                    display: flex;
                    align-items: center;
                    padding: 15px 0;
                    border-bottom: 1px solid rgba(103, 58, 183, 0.1);
                }}
                .detail-item:last-child {{
                    border-bottom: none;
                }}
                .detail-icon {{
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #673ab7 0%, #9c27b0 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    margin-right: 15px;
                    font-size: 18px;
                }}
                .detail-content {{
                    flex: 1;
                }}
                .detail-label {{
                    font-weight: 500;
                    color: #666;
                    font-size: 14px;
                    margin-bottom: 4px;
                }}
                .detail-value {{
                    color: #333;
                    font-size: 16px;
                    font-weight: 500;
                }}
                .password-section {{
                    background: linear-gradient(135deg, #673ab7 0%, #2196f3 100%);
                    border-radius: 16px;
                    padding: 30px;
                    text-align: center;
                    margin: 40px 0;
                    color: white;
                    position: relative;
                    overflow: hidden;
                }}
                .password {{
                    font-family: 'Courier New', monospace;
                    font-size: 28px;
                    letter-spacing: 3px;
                    background: rgba(255,255,255,0.15);
                    padding: 20px;
                    border-radius: 12px;
                    margin: 20px 0;
                    display: inline-block;
                    font-weight: 600;
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                .action-button {{
                    display: inline-block;
                    background: white;
                    color: #673ab7;
                    padding: 16px 40px;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: 600;
                    margin-top: 20px;
                    transition: all 0.3s ease;
                    box-shadow: 0 8px 25px rgba(103, 58, 183, 0.2);
                }}
                .action-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 12px 35px rgba(103, 58, 183, 0.3);
                }}
                .instructions {{
                    background: #fff8e1;
                    border-radius: 12px;
                    padding: 25px;
                    margin: 30px 0;
                    border-left: 4px solid #ff9800;
                }}
                .footer {{
                    background: #f5f7fa;
                    padding: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 14px;
                    border-top: 1px solid #e0e0e0;
                }}
                .company-name {{
                    color: #673ab7;
                    font-weight: 600;
                    font-size: 18px;
                    margin-bottom: 10px;
                }}
                .badge {{
                    display: inline-block;
                    background: #673ab7;
                    color: white;
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 500;
                    margin-bottom: 20px;
                }}
                .emoji {{
                    font-size: 48px;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="emoji">📋</div>
                    <h1>Leave Approval Required</h1>
                    <p>VOLAR FASHION HR Management System</p>
                </div>
                
                <div class="content">
                    <div class="greeting">
                        Dear <strong style="color: #673ab7;">{superior_name}</strong>,<br><br>
                        An employee has submitted a leave request that requires your approval. 
                        Please review the details below and take appropriate action.
                    </div>
                    
                    <div class="badge">Action Required</div>
                    
                    <div class="details-card">
                        <div class="detail-item">
                            <div class="detail-icon">👤</div>
                            <div class="detail-content">
                                <div class="detail-label">Employee Name</div>
                                <div class="detail-value">{leave_details['employee_name']}</div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-icon">🔢</div>
                            <div class="detail-content">
                                <div class="detail-label">Employee Code</div>
                                <div class="detail-value">{leave_details['employee_code']}</div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-icon">🏛️</div>
                            <div class="detail-content">
                                <div class="detail-label">Department</div>
                                <div class="detail-value">{leave_details['department']}</div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-icon">📅</div>
                            <div class="detail-content">
                                <div class="detail-label">Leave Period</div>
                                <div class="detail-value">{leave_details['from_date']} to {leave_details['till_date']}</div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-icon">📊</div>
                            <div class="detail-content">
                                <div class="detail-label">Duration</div>
                                <div class="detail-value">{duration_display} ({leave_details['leave_type']})</div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-icon">📝</div>
                            <div class="detail-content">
                                <div class="detail-label">Purpose</div>
                                <div class="detail-value">{leave_details['purpose']}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="password-section">
                        <div style="font-size: 20px; margin-bottom: 10px;">Your Secure Approval Code</div>
                        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 20px;">Use this code in the approval portal</div>
                        <div class="password">{approval_password}</div>
                        <div style="font-size: 14px; opacity: 0.9; margin-top: 15px;">
                            Valid for single use only
                        </div>
                    </div>
                    
                    <div class="instructions">
                        <strong style="color: #ff9800; display: block; margin-bottom: 10px;">📋 How to Approve/Reject:</strong>
                        1. <strong>Access the Portal:</strong> <a href="{app_url}" style="color: #673ab7; font-weight: 500;">{app_url}</a><br>
                        2. <strong>Switch to "Approval Portal" tab</strong><br>
                        3. <strong>Enter your email:</strong> {superior_email}<br>
                        4. <strong>Enter the approval code above</strong><br>
                        5. <strong>Select your decision</strong> and submit
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{app_url}" class="action-button">🚀 Go to Approval Portal</a>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="company-name">VOLAR FASHION PVT LTD</div>
                    <div style="margin-top: 10px; color: #888;">
                        Human Resources Department<br>
                        📧 hrvolarfashion@gmail.com | 🌐 www.volarfashion.com
                    </div>
                    <div style="margin-top: 20px; font-size: 12px; color: #aaa;">
                        This is an automated message. Please do not reply directly to this email.
                    </div>
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

def update_leave_status(sheet, superior_email, approval_password, status):
    """Update leave status in Google Sheet using email and password"""
    try:
        all_records = sheet.get_all_values()
        
        for idx, row in enumerate(all_records):
            if idx == 0:
                continue
            
            if len(row) > 13 and row[10] == superior_email and row[13] == approval_password:
                sheet.update_cell(idx + 1, 12, status)
                sheet.update_cell(idx + 1, 13, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                sheet.update_cell(idx + 1, 14, "USED")
                return True
        
        return False
    except Exception as e:
        st.error(f"Error updating status: {str(e)}")
        return False

# Beautiful Company Header with Floating Animation
st.markdown("""
    <div class="company-header floating-element">
        <h1>VOLAR FASHION</h1>
        <h2>Leave Management System</h2>
   
    </div>
""", unsafe_allow_html=True)

# Create beautiful tabs
tab1, tab2 = st.tabs(["📝 Submit Leave Application", "✅ Approval Portal"])

with tab1:
    
    
    # Form Header with Icon
    st.markdown("""
        <div class="section-header">
            <div class="icon-badge">📋</div>
            <div>
                <h3 style="margin: 0;">Leave Application Form</h3>
                <p style="margin: 5px 0 0 0; color: #718096; font-size: 0.95rem;">
                    Complete all fields below to submit your leave request
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        employee_name = st.text_input(
            "👤 Full Name",
            placeholder="Enter your full name",
            help="Please enter your complete name as per company records"
        )
        employee_code = st.text_input(
            "🔢 Employee ID",
            placeholder="e.g., VF-EMP-001",
            help="Your unique employee identification code"
        )
        department = st.selectbox(
            "🏛️ Department",
            ["Select Department"] + DEPARTMENTS,
            help="Select your department from the list"
        )
    
    with col2:
        leave_type = st.selectbox(
            "📋 Leave Type",
            ["Select Type", "Full Day", "Half Day", "Early Exit"],
            help="Select the type of leave you are requesting"
        )
        from_date = st.date_input(
            "📅 Start Date",
            min_value=datetime.now().date(),
            help="Select the first day of your leave"
        )
        till_date = st.date_input(
            "📅 End Date",
            min_value=datetime.now().date(),
            help="Select the last day of your leave"
        )
    
    # Duration Card with Animation - Show based on leave type
    if leave_type != "Select Type":
        no_of_days = calculate_days(from_date, till_date, leave_type)
        
        # Only show duration card for leave types that have duration
        if leave_type != "Early Exit":
            st.markdown(f"""
                <div class="metric-card floating-element">
                    <div style="font-size: 0.9rem; color: #6b46c1; font-weight: 500;">Leave Duration</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #553c9a; margin: 10px 0;">
                        {no_of_days}
                    </div>
                    <div style="font-size: 0.9rem; color: #805ad5;">days requested</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # For Early Exit, show thumbs up with animation
            st.markdown(f"""
                <div class="thumbsup-box floating-element">
                    <div class="thumbsup-emoji">👍</div>
                    <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 8px;">Early Exit Request</div>
                    <div style="font-size: 0.95rem;">
                        You're requesting to leave early from work today.Only 2 Early Leaves are Permitted per month.
                    </div>
    
                </div>
            """, unsafe_allow_html=True)
    else:
        no_of_days = "N/A"  # Default value when no type selected
    
    # Purpose Section
    st.markdown("""
        <div style="margin-top: 2.5rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div class="icon-badge" style="background: linear-gradient(135deg, #2196f3 0%, #03a9f4 100%);">📝</div>
                <div>
                    <h3 style="margin: 0;">Leave Details</h3>
                    <p style="margin: 5px 0 0 0; color: #718096; font-size: 0.95rem;">
                        Provide detailed information about your leave request
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    purpose = st.text_area(
        "Purpose of Leave",
        placeholder="Please provide a clear and detailed explanation for your leave request...",
        height=120,
        help="Be specific about the reason for your leave"
    )
    
    # Manager Selection
    superior_name = st.selectbox(
        "👔 Reporting Manager",
        ["Select Manager"] + list(SUPERIORS.keys()),
        help="Select your direct reporting manager"
    )
    
    # Information Box
    st.markdown("""
        <div class="info-box">
            <div style="display: flex; align-items: flex-start;">
                <div style="font-size: 1.5rem; margin-right: 15px;">ℹ️</div>
                <div>
                    <strong style="display: block; margin-bottom: 8px;">Important Guidelines</strong>
                    • All fields are required for submission<br>
                    • Your manager will receive a secure approval code via email<br>
                    • Approval decisions are typically made within 24 hours<br>
                    • You'll be notified once a decision is made<br>
                    • For urgent requests, please contact your manager directly
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Submit Button with Beautiful Design
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        if st.button("🚀 Submit Leave Request", type="primary", use_container_width=True):
            if not all([employee_name, employee_code, department != "Select Department", 
                        leave_type != "Select Type", purpose, superior_name != "Select Manager"]):
                st.markdown('''
                    <div class="error-message">
                        <div style="display: flex; align-items: center; justify-content: center;">
                            <div style="font-size: 1.5rem; margin-right: 10px;">⚠️</div>
                            <div>
                                <strong>Please complete all required fields</strong><br>
                                Ensure all sections are properly filled before submission
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
            elif from_date > till_date:
                st.markdown('''
                    <div class="error-message">
                        <div style="display: flex; align-items: center; justify-content: center;">
                            <div style="font-size: 1.5rem; margin-right: 10px;">📅</div>
                            <div>
                                <strong>Date Error</strong><br>
                                End date must be after or equal to start date
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                with st.spinner(''):
                    # Add loading animation
                    st.markdown("""
                        <div style="text-align: center; padding: 3rem;">
                            <div style="font-size: 3rem; color: #673ab7; margin-bottom: 1rem;">⏳</div>
                            <div style="font-size: 1.2rem; color: #4a5568; margin-bottom: 0.5rem;">
                                Processing your request
                            </div>
                            <div style="color: #718096;">
                                Please wait while we submit your application...
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Get form data
                    submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    superior_email = SUPERIORS[superior_name]
                    approval_password = generate_approval_password()
                    
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
                    
                    # Save to Google Sheets
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
                            "",
                            approval_password
                        ]
                        
                        try:
                            sheet.append_row(row_data)
                            
                            # Send email
                            email_sent = send_approval_email(
                                employee_name,
                                superior_name,
                                superior_email,
                                leave_details,
                                approval_password
                            )
                            
                            if email_sent:
                                st.markdown('''
                                    <div class="success-message">
                                        <div style="font-size: 3rem; margin-bottom: 1rem;">✨</div>
                                        <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 10px; color: #166534;">
                                            Application Submitted Successfully!
                                        </div>
                                        <div style="color: #155724; margin-bottom: 15px;">
                                            Your leave request has been sent to your manager for approval.
                                        </div>
                                        <div style="font-size: 0.95rem; color: #0f5132; opacity: 0.9;">
                                            You will receive a notification once a decision is made.
                                        </div>
                                    </div>
                                ''', unsafe_allow_html=True)
                                
                                # Add celebration
                                st.balloons()
                                
                                # Add success animation
                                st.markdown("""
                                    <div style="text-align: center; margin-top: 2rem;">
                                        <div style="display: inline-block; animation: float 2s ease-in-out infinite;">
                                            ✅
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Clear form after successful submission
                                st.rerun()
                            else:
                                st.markdown('''
                                    <div class="error-message">
                                        <div style="display: flex; align-items: center; justify-content: center;">
                                            <div style="font-size: 1.5rem; margin-right: 10px;">📧</div>
                                            <div>
                                                <strong>Email Notification Failed</strong><br>
                                                Application saved, but email could not be sent.<br>
                                                Please inform your manager directly.
                                            </div>
                                        </div>
                                    </div>
                                ''', unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(
                                f'''<div class="error-message">
                                    <strong>Submission Error</strong><br>
                                    Please try again or contact HR: {str(e)}
                                </div>''',
                                unsafe_allow_html=True
                            )
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    
    
    # Approval Portal Header
    st.markdown("""
        <div class="section-header">
            <div class="icon-badge" style="background: linear-gradient(135deg, #2196f3 0%, #03a9f4 100%);">✅</div>
            <div>
                <h3 style="margin: 0;">Manager Approval Portal</h3>
                <p style="margin: 5px 0 0 0; color: #718096; font-size: 0.95rem;">
                    Securely approve or reject leave requests using your approval code
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Security Info
    st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; 
                    border: 1px solid rgba(33, 150, 243, 0.2);">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 15px; color: #2196f3;">🔒</div>
                <div>
                    <strong style="color: #0d47a1;">Secure Authentication Required</strong><br>
                    <span style="color: #1565c0; font-size: 0.95rem;">
                        Use the unique approval code sent to your email for authentication
                    </span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Form Fields
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        superior_email_input = st.text_input(
            "📧 Manager Email",
            placeholder="your.email@volarfashion.com",
            help="Enter your registered manager email address"
        )
    
    with col2:
        approval_password_input = st.text_input(
            "🔑 Approval Code",
            type="password",
            placeholder="Enter 5-character code",
            help="Enter the unique code from the approval email"
        )
    
    # Decision Section
    st.markdown("---")
    
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div class="icon-badge" style="background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);">📋</div>
                <div>
                    <h4 style="margin: 0;">Decision</h4>
                    <p style="margin: 5px 0 0 0; color: #718096; font-size: 0.9rem;">
                        Select your decision for this leave request
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    action = st.selectbox(
        "Select Action",
        ["Select Decision", "✅ Approve", "❌ Reject"],
        label_visibility="collapsed"
    )
    
    # Submit Decision Button
    if st.button("Submit Decision", type="primary", use_container_width=True):
        if not all([superior_email_input, approval_password_input, action != "Select Decision"]):
            st.markdown('''
                <div class="error-message">
                    <div style="display: flex; align-items: center; justify-content: center;">
                        <div style="font-size: 1.5rem; margin-right: 10px;">⚠️</div>
                        <div>
                            <strong>Missing Information</strong><br>
                            Please complete all fields and select a decision
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        elif superior_email_input not in SUPERIORS.values():
            st.markdown('''
                <div class="error-message">
                    <div style="display: flex; align-items: center; justify-content: center;">
                        <div style="font-size: 1.5rem; margin-right: 10px;">📧</div>
                        <div>
                            <strong>Unauthorized Access</strong><br>
                            This email is not authorized for approvals
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        elif len(approval_password_input) != 5:
            st.markdown('''
                <div class="error-message">
                    <div style="display: flex; align-items: center; justify-content: center;">
                        <div style="font-size: 1.5rem; margin-right: 10px;">🔑</div>
                        <div>
                            <strong>Invalid Code Format</strong><br>
                            Please enter the exact 5-character code from your email
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            sheet = setup_google_sheets()
            if sheet:
                status = "Approved" if action == "✅ Approve" else "Rejected"
                success = update_leave_status(sheet, superior_email_input, approval_password_input, status)
                
                if success:
                    status_color = "#155724" if status == "Approved" else "#721c24"
                    status_bg = "#d4edda" if status == "Approved" else "#f8d7da"
                    status_icon = "✅" if status == "Approved" else "❌"
                    
                    st.markdown(f'''
                        <div style="background: {status_bg}; border-left: 4px solid {status_color}; 
                                  color: {status_color}; padding: 2rem; border-radius: 16px; 
                                  margin: 2rem 0; text-align: center; animation: slideIn 0.5s ease-out;">
                            <div style="font-size: 3rem; margin-bottom: 1rem;">{status_icon}</div>
                            <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 10px;">
                                Decision Submitted Successfully!
                            </div>
                            <div style="margin-bottom: 15px;">
                                The leave request has been <strong>{status.lower()}</strong>.
                            </div>
                            <div style="font-size: 0.95rem; opacity: 0.9;">
                                The employee has been notified of your decision.
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    st.balloons()
                    
                    # Clear form after submission
                    time.sleep(2)
                    st.rerun()
                else:
                    st.markdown('''
                        <div class="error-message">
                            <div style="display: flex; align-items: center; justify-content: center;">
                                <div style="font-size: 1.5rem; margin-right: 10px;">🔐</div>
                                <div>
                                    <strong>Authentication Failed</strong><br>
                                    Invalid code or code already used.<br>
                                    Please check your email or contact HR for assistance.
                                </div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


