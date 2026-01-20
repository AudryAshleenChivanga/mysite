# Quick Email Setup Guide

## The Problem
You set up the email, but you're not receiving messages. This is usually because the environment variable isn't set in the PowerShell session where you're running the server.

## Quick Fix (Choose One)

### Option 1: Use the Setup Script (Easiest)
```powershell
python setup_email.py
```
This will:
- Test your App Password
- Send you a test email
- Show you exactly what to do next

### Option 2: Set Environment Variable Manually

**Step 1: Get your App Password**
- Go to: https://myaccount.google.com/apppasswords
- Generate one for "Mail"
- Copy the 16-character password (remove spaces!)

**Step 2: Set it in PowerShell**
```powershell
$env:GMAIL_APP_PASSWORD = "your-16-character-password-no-spaces"
```

**Step 3: Verify it's set**
```powershell
echo $env:GMAIL_APP_PASSWORD
```
You should see your password (without spaces).

**Step 4: Start your server**
```powershell
python server.py
```

**Step 5: Test it**
- Visit: http://localhost:5000/api/test-email
- This will show if email is configured correctly

### Option 3: Use the Batch File
```powershell
start_server_with_email.bat
```
This will prompt you to enter your App Password.

## Important Notes

⚠️ **The environment variable only lasts for the current PowerShell session!**

If you:
- Close PowerShell
- Open a new terminal window
- Restart your computer

You'll need to set `$env:GMAIL_APP_PASSWORD` again.

## Making It Permanent (Optional)

If you want to set it permanently, add this to your PowerShell profile:

```powershell
# Open your profile
notepad $PROFILE

# Add this line (replace with your actual password):
$env:GMAIL_APP_PASSWORD = "your-16-character-password"
```

## Testing

1. **Test configuration:**
   ```
   python test_email.py
   ```

2. **Test from browser:**
   Visit: http://localhost:5000/api/test-email

3. **Test contact form:**
   - Go to: http://localhost:5000/#contact
   - Fill out the form
   - Check server console for detailed logs
   - Check your email inbox (and spam folder)

## Still Not Working?

Run the test script to see exactly what's wrong:
```powershell
python test_email.py
```

It will tell you:
- If the password is set
- If authentication works
- What error you're getting

