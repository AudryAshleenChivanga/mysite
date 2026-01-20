#!/usr/bin/env python3
"""
Email Test Script - Debug email configuration
Run this to test if your email setup is working
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
RECIPIENT_EMAIL = "audryashleenchivanga@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "audryashleenchivanga@gmail.com"
SMTP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

def test_email_config():
    print("="*70)
    print("EMAIL CONFIGURATION TEST")
    print("="*70)
    print()
    
    # Check 1: Environment variable
    print("1. Checking environment variable...")
    if SMTP_PASSWORD:
        print(f"   ✓ GMAIL_APP_PASSWORD is set")
        print(f"   ✓ Password length: {len(SMTP_PASSWORD)} characters")
        if ' ' in SMTP_PASSWORD:
            print(f"   ⚠ WARNING: Password contains spaces! Remove them.")
            print(f"   Current: '{SMTP_PASSWORD}'")
            print(f"   Should be: '{SMTP_PASSWORD.replace(' ', '')}'")
        else:
            print(f"   ✓ Password format looks good (no spaces)")
    else:
        print("   ✗ GMAIL_APP_PASSWORD is NOT set!")
        print("   Set it with: $env:GMAIL_APP_PASSWORD = 'your-password'")
        return False
    print()
    
    # Check 2: SMTP Connection
    print("2. Testing SMTP connection...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        print(f"   ✓ Connected to {SMTP_SERVER}:{SMTP_PORT}")
        
        # Enable debug output
        server.set_debuglevel(1)
        
        # Check 3: TLS
        print("3. Starting TLS...")
        server.starttls()
        print("   ✓ TLS started successfully")
        print()
        
        # Check 4: Authentication
        print("4. Testing authentication...")
        try:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            print("   ✓ Authentication successful!")
        except smtplib.SMTPAuthenticationError as e:
            print(f"   ✗ Authentication FAILED!")
            print(f"   Error: {str(e)}")
            print()
            print("   Common issues:")
            print("   - Using regular password instead of App Password")
            print("   - App Password has spaces (remove them)")
            print("   - 2-Step Verification not enabled")
            print("   - Wrong App Password")
            server.quit()
            return False
        print()
        
        # Check 5: Send test email
        print("5. Sending test email...")
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "Test Email from Portfolio - If you see this, it works!"
        
        body = """
This is a test email from your portfolio contact form.

If you received this email, your email configuration is working correctly!

You can now receive messages from your portfolio contact form.
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())
            print(f"   ✓ Test email sent successfully!")
            print(f"   ✓ Check your inbox at: {RECIPIENT_EMAIL}")
            print(f"   ✓ Also check spam/junk folder")
        except Exception as e:
            print(f"   ✗ Failed to send email: {str(e)}")
            server.quit()
            return False
        
        server.quit()
        print()
        print("="*70)
        print("SUCCESS! Email configuration is working!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"   ✗ Connection failed: {str(e)}")
        print()
        print("   Check:")
        print("   - Internet connection")
        print("   - Firewall settings")
        print("   - SMTP server settings")
        return False

if __name__ == "__main__":
    print()
    success = test_email_config()
    print()
    
    if not success:
        print("="*70)
        print("TROUBLESHOOTING STEPS:")
        print("="*70)
        print()
        print("1. Make sure you set the environment variable:")
        print("   PowerShell: $env:GMAIL_APP_PASSWORD = 'your-16-char-password'")
        print("   (Remove spaces from the App Password!)")
        print()
        print("2. Get a new App Password:")
        print("   https://myaccount.google.com/apppasswords")
        print()
        print("3. Make sure 2-Step Verification is enabled:")
        print("   https://myaccount.google.com/security")
        print()
        print("4. Check Gmail security alerts:")
        print("   https://myaccount.google.com/security")
        print()
        print("5. Try restarting your server after setting the variable")
        print()

