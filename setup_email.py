#!/usr/bin/env python3
"""
Email Setup Helper
This script helps you set up your Gmail App Password securely
"""

import os
import getpass
import smtplib
from email.mime.text import MIMEText

print("="*70)
print("EMAIL SETUP FOR PORTFOLIO CONTACT FORM")
print("="*70)
print()
print("This will help you configure your Gmail App Password.")
print()
print("Steps to get your App Password:")
print("1. Go to: https://myaccount.google.com/apppasswords")
print("2. Select 'Mail' and 'Other (Custom name)'")
print("3. Name it 'Portfolio Contact Form'")
print("4. Copy the 16-character password (it will look like: abcd efgh ijkl mnop)")
print()
print("IMPORTANT: Remove all spaces from the password!")
print("Example: 'abcd efgh ijkl mnop' becomes 'abcdefghijklmnop'")
print()

# Get App Password
app_password = getpass.getpass("Enter your Gmail App Password (16 characters, no spaces): ").strip()

# Remove any spaces
app_password = app_password.replace(' ', '')

if len(app_password) != 16:
    print(f"\n⚠ WARNING: Password should be 16 characters, but you entered {len(app_password)} characters.")
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        exit()

# Test the password
print("\nTesting your App Password...")
print("-" * 70)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "audryashleenchivanga@gmail.com"
RECIPIENT_EMAIL = "audryashleenchivanga@gmail.com"

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, app_password)
    
    # Send a test email
    print("✓ Authentication successful!")
    print("Sending test email...")
    
    msg = MIMEText("This is a test email. If you received this, your email setup is working!")
    msg['From'] = SMTP_USERNAME
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Portfolio Email Test - Setup Successful!"
    
    server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    
    print("✓ Test email sent successfully!")
    print(f"✓ Check your inbox at: {RECIPIENT_EMAIL}")
    print("✓ Also check spam/junk folder")
    print()
    print("="*70)
    print("SUCCESS! Your email is configured correctly.")
    print("="*70)
    print()
    print("To use this in your server, run:")
    print()
    print(f'  $env:GMAIL_APP_PASSWORD = "{app_password}"')
    print("  python server.py")
    print()
    print("Or use the batch file:")
    print("  start_server_with_email.bat")
    print()
    print("NOTE: You need to set this environment variable EVERY TIME you open a new PowerShell window.")
    print("To make it permanent, you can add it to your PowerShell profile.")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n✗ Authentication FAILED!")
    print(f"Error: {str(e)}")
    print()
    print("Common issues:")
    print("- Using regular Gmail password instead of App Password")
    print("- App Password has spaces (should be 16 characters with no spaces)")
    print("- 2-Step Verification not enabled on your Google Account")
    print("- Wrong App Password")
    print()
    print("Get a new App Password: https://myaccount.google.com/apppasswords")
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    print("\nCheck your internet connection and try again.")



