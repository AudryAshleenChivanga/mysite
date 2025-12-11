# Email Setup Guide

Your contact form is now configured to send emails directly to **audryashleenchivanga@gmail.com**.

## Setup Instructions

### Option 1: Using Gmail App Password (Recommended)

1. **Enable 2-Step Verification** on your Google Account:
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification" if not already enabled

2. **Generate an App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Portfolio Contact Form" as the name
   - Click "Generate"
   - Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)

3. **Set the App Password as Environment Variable**:

   **Windows (PowerShell):**
   ```powershell
   $env:GMAIL_APP_PASSWORD = "your-16-character-app-password"
   python server.py
   ```

   **Windows (Command Prompt):**
   ```cmd
   set GMAIL_APP_PASSWORD=your-16-character-app-password
   python server.py
   ```

   **Linux/Mac:**
   ```bash
   export GMAIL_APP_PASSWORD="your-16-character-app-password"
   python server.py
   ```

### Option 2: Direct Configuration (Less Secure)

If you prefer to set the password directly in the code (not recommended for production):

1. Edit `server.py` and replace:
   ```python
   SMTP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
   ```
   with:
   ```python
   SMTP_PASSWORD = "your-16-character-app-password"
   ```

⚠️ **Warning**: Never commit your password to version control!

## Testing

1. Start your server:
   ```bash
   python server.py
   ```

2. Visit http://localhost:5000 and navigate to the Contact section

3. Fill out the contact form and submit

4. Check your email inbox at **audryashleenchivanga@gmail.com**

## Troubleshooting

### "Failed to send email" Error

- Make sure you've set the `GMAIL_APP_PASSWORD` environment variable
- Verify your App Password is correct (16 characters, no spaces)
- Check that 2-Step Verification is enabled on your Google Account
- Ensure your internet connection is working

### Email Not Received

- Check your spam/junk folder
- Verify the email address in `server.py` is correct: `RECIPIENT_EMAIL = "audryashleenchivanga@gmail.com"`
- Check server logs for error messages

### Development Mode (No Email Configuration)

If you don't configure the email password, the form will still work but will only print messages to the server console instead of sending emails. This is useful for testing.

## Security Notes

- **Never share your App Password** publicly
- **Don't commit passwords** to Git repositories
- Use environment variables for sensitive data
- Consider using a dedicated email account for production

## Alternative: Using Other Email Providers

If you want to use a different email provider, update these settings in `server.py`:

```python
SMTP_SERVER = "smtp.your-provider.com"  # e.g., "smtp.outlook.com" for Outlook
SMTP_PORT = 587  # Usually 587 for TLS, 465 for SSL
SMTP_USERNAME = "your-email@example.com"
SMTP_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
```

Common SMTP settings:
- **Gmail**: smtp.gmail.com, port 587
- **Outlook**: smtp-mail.outlook.com, port 587
- **Yahoo**: smtp.mail.yahoo.com, port 587

