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

1. **Set your App Password** (see instructions above)

2. **Start your server**:
   ```bash
   python server.py
   ```

3. **Test email configuration** (optional):
   Visit http://localhost:5000/api/test-email in your browser
   This will show you if your email is configured correctly

4. **Test the contact form**:
   - Visit http://localhost:5000/#contact
   - Fill out the contact form and submit
   - Check the server console for detailed logs
   - Check your email inbox at **audryashleenchivanga@gmail.com**
   - Also check spam/junk folder

## Troubleshooting

### "Failed to send email" Error

1. **Check if App Password is set**:
   - Visit http://localhost:5000/api/test-email
   - Look for `password_configured: true`
   - If false, you need to set the environment variable

2. **Verify App Password format**:
   - Should be 16 characters (no spaces)
   - Example: `abcd efgh ijkl mnop` → use as `abcdefghijklmnop` (no spaces)

3. **Check server console logs**:
   - The server will show detailed error messages
   - Look for "SMTP Authentication failed" or similar errors

4. **Common issues**:
   - Using regular Gmail password instead of App Password → **Must use App Password**
   - 2-Step Verification not enabled → **Must enable 2-Step Verification first**
   - Wrong password format → **Remove spaces from App Password**

### Email Not Received

1. **Check spam/junk folder** - Gmail sometimes filters automated emails
2. **Check server logs** - Look for "Email sent successfully!" message
3. **Test email configuration** - Visit http://localhost:5000/api/test-email
4. **Verify recipient email** - Check `server.py` line: `RECIPIENT_EMAIL = "audryashleenchivanga@gmail.com"`
5. **Check Gmail security**:
   - Go to https://myaccount.google.com/security
   - Make sure "Less secure app access" is NOT the issue (use App Password instead)
   - Check if there are any security alerts in your Google Account

### Still Not Working?

1. **Check server console output** - It will show detailed error messages
2. **Try the test endpoint** - http://localhost:5000/api/test-email
3. **Verify environment variable**:
   ```powershell
   echo $env:GMAIL_APP_PASSWORD
   ```
4. **Restart server** after setting environment variable

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

