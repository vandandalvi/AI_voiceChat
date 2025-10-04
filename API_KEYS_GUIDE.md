# 🔑 API Keys Setup Guide

Complete guide to obtaining all necessary API keys for the Talkito AI Interview project.

---

## 📋 Overview

You need **2 required** and **1 optional** API key:

| Service | Required? | Purpose | Cost |
|---------|-----------|---------|------|
| Gemini AI | ✅ Yes | AI interview responses | Free tier available |
| ElevenLabs | ✅ Yes | Text-to-speech | Free tier: 10K chars/month |
| OpenAI Whisper | ⚠️ Optional | Speech-to-text | $0.006/minute |

---

## 1️⃣ Gemini API Key (Required)

### What You Need
- Google account
- Access to Google AI Studio

### Step-by-Step Instructions

#### Step 1: Visit Google AI Studio
Go to: **https://makersuite.google.com/app/apikey**

Or:
1. Search "Google AI Studio" in Google
2. Click on the official link
3. Sign in with your Google account

#### Step 2: Get Your API Key
1. Once signed in, you'll see the API Key page
2. Click **"Get API Key"** or **"Create API Key"**
3. You may need to:
   - Create a new project, or
   - Select an existing Google Cloud project
4. The API key will be generated
5. **Copy the API key** (it will look like: `AIzaSyA...`)

#### Step 3: Important Notes
- ⚠️ **Save this key immediately** - you may not be able to see it again
- Store it in a password manager
- Never share it publicly
- Never commit it to Git

### Free Tier Limits
- ✅ **60 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **1 million tokens per month** (generous for interviews)

### Pricing (if you exceed free tier)
- Very affordable - unlikely to be charged for personal use
- Check current pricing: https://ai.google.dev/pricing

### Troubleshooting
**Issue:** "API key not working"
- Make sure you copied the entire key
- Check for extra spaces before/after the key
- Verify the key is enabled in Google Cloud Console
- Try regenerating a new key

**Issue:** "Quota exceeded"
- You've hit the daily limit (1,500 requests)
- Wait 24 hours or upgrade your plan

---

## 2️⃣ ElevenLabs API Key (Required)

### What You Need
- Email address
- ElevenLabs account (free tier available)

### Step-by-Step Instructions

#### Step 1: Create Account
Go to: **https://elevenlabs.io/**

1. Click **"Get Started Free"** or **"Sign Up"**
2. Enter your email and password
3. Verify your email address
4. Complete the onboarding

#### Step 2: Get Your API Key
1. Click on your **profile icon** (top right)
2. Select **"Profile"** or **"Profile Settings"**
3. Look for **"API Key"** section
4. Click **"Copy"** or reveal and copy the key
5. It will look like: `abc123def456...`

#### Step 3: (Optional) Choose a Voice
1. Go to **"Voice Library"** or **"Voices"**
2. Browse available voices
3. Click on a voice you like
4. Click **"Add to Lab"** (free voices)
5. Copy the **Voice ID** (looks like: `EXAVITQu4vr4xnSDxMaL`)

### Free Tier Limits
- ✅ **10,000 characters per month**
- ✅ **3 custom voices**
- ✅ **Access to pre-made voices**

**Example Usage:**
- Average interview response: ~100 characters
- Free tier: ~100 responses per month
- More than enough for testing!

### Pricing (if you need more)
- **Starter**: $5/month - 30,000 characters
- **Creator**: $22/month - 100,000 characters
- Check current pricing: https://elevenlabs.io/pricing

### Voice ID Options
**Default Voice** (included in project):
- ID: `EXAVITQu4vr4xnSDxMaL`
- Name: Sarah
- Style: Professional, clear

**Popular Alternatives:**
- Rachel (Natural, warm): `21m00Tcm4TlvDq8ikWAM`
- Domi (Strong, confident): `AZnzlk1XvdvUeBnXmlld`
- Bella (Soft, gentle): `EXAVITQu4vr4xnSDxMaL`

To change voice:
1. Get Voice ID from Voice Library
2. Update `.env`: `ELEVENLABS_VOICE_ID=your_voice_id`

### Troubleshooting
**Issue:** "Invalid API key"
- Regenerate key in profile settings
- Check for spaces before/after the key
- Make sure account is verified

**Issue:** "Character limit exceeded"
- You've used your monthly quota
- Wait until next month or upgrade plan
- Check usage: Profile → Subscription

**Issue:** "Audio quality is poor"
- Adjust voice settings in `app.py`
- Try a different voice
- Check internet connection

---

## 3️⃣ OpenAI API Key (Optional)

### What You Need
- OpenAI account
- Credit card (for paid tier)
- ~$5 minimum to start

### Why It's Optional
The basic `app.py` uses a **placeholder** for speech-to-text. It won't actually transcribe your voice, but you can test the rest of the system.

**Use OpenAI Whisper if:**
- ✅ You want actual speech-to-text
- ✅ You're willing to pay $0.006/minute
- ✅ You want high accuracy

**Skip OpenAI if:**
- ❌ Just testing the project
- ❌ Want to keep costs at $0
- ❌ Can wait to integrate another STT service

### Step-by-Step Instructions

#### Step 1: Create Account
Go to: **https://platform.openai.com/signup**

1. Click **"Sign up"**
2. Enter email or use Google/Microsoft account
3. Verify your email
4. Complete phone verification

#### Step 2: Add Payment Method
1. Go to **"Billing"** in the menu
2. Click **"Payment methods"**
3. Add a credit card
4. Set up a spending limit (recommended: $5-10/month)

#### Step 3: Get API Key
1. Go to: https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Give it a name (e.g., "Talkito Interview")
4. **Copy the key immediately** (you won't see it again!)
5. It will look like: `sk-proj-...`

### Pricing
- **Whisper API**: $0.006 per minute of audio
- **Example costs:**
  - 10-minute interview: $0.06
  - 100 interviews: $6.00

### Usage Tips
- Set a monthly spending limit
- Monitor usage in OpenAI dashboard
- Each recording is typically 10-30 seconds

### Troubleshooting
**Issue:** "Insufficient credits"
- Add more credits to your account
- Check current balance in Billing

**Issue:** "Rate limit exceeded"
- You're making too many requests
- Implement retry logic
- Upgrade tier if needed

---

## 🔐 Security Best Practices

### DO ✅
- Store keys in `.env` file
- Never commit `.env` to Git
- Use environment variables in production
- Rotate keys periodically
- Set spending limits
- Monitor API usage

### DON'T ❌
- Share keys publicly
- Commit keys to GitHub
- Hardcode keys in source code
- Use production keys for testing
- Share screenshots with visible keys

---

## 📝 Adding Keys to Your Project

### Step 1: Open `.env` File
Location: `backend\.env`

If it doesn't exist:
```powershell
cd backend
copy .env.example .env
```

### Step 2: Add Your Keys
Open `.env` in any text editor and fill in:

```env
# Replace these with your actual keys
GEMINI_API_KEY=AIzaSyA_your_actual_key_here
ELEVENLABS_API_KEY=abc123_your_actual_key_here
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
OPENAI_API_KEY=sk-proj-your_key_here
```

### Step 3: Save and Restart
1. Save the `.env` file
2. Restart the backend server
3. Test the application

---

## ✅ Verification Checklist

Before running the app, verify:

- [ ] Gemini API key is added to `.env`
- [ ] Gemini API key works (test in Google AI Studio)
- [ ] ElevenLabs API key is added to `.env`
- [ ] ElevenLabs API key works (test on their website)
- [ ] (Optional) OpenAI key is added if using Whisper
- [ ] No extra spaces before/after keys
- [ ] `.env` file is in `backend/` folder
- [ ] `.env` is listed in `.gitignore`

---

## 🧪 Testing Your Keys

### Test Gemini
1. Go to: https://makersuite.google.com/
2. Try generating text
3. If it works, your key is valid

### Test ElevenLabs
1. Go to: https://elevenlabs.io/speech-synthesis
2. Type some text
3. Click "Generate"
4. If it works, your key is valid

### Test OpenAI
1. Go to: https://platform.openai.com/playground
2. Try the Chat or Whisper API
3. If it works, your key is valid

---

## 💰 Cost Estimation

### Free Tier (Gemini + ElevenLabs only)
- **Setup cost**: $0
- **Monthly cost**: $0
- **Limitations**: 
  - 1,500 Gemini requests/day
  - 10,000 ElevenLabs characters/month
  - No actual speech-to-text

### With OpenAI Whisper
- **Setup cost**: $5 (minimum OpenAI deposit)
- **Per interview**: ~$0.06 (10 minutes)
- **Monthly cost**: Depends on usage
  - 10 interviews: $0.60
  - 50 interviews: $3.00
  - 100 interviews: $6.00

### Recommended Starting Plan
1. **Week 1**: Use free tier only (no Whisper)
   - Cost: $0
   - Test everything except actual transcription
   
2. **Week 2**: Add Whisper if satisfied
   - Add $5 to OpenAI account
   - Use Whisper for real transcription
   - Monitor usage

---

## 🆘 Help & Support

### Gemini Support
- Documentation: https://ai.google.dev/docs
- Community: Google AI Forum

### ElevenLabs Support
- Documentation: https://docs.elevenlabs.io/
- Support: help@elevenlabs.io
- Discord: https://discord.gg/elevenlabs

### OpenAI Support
- Documentation: https://platform.openai.com/docs
- Help Center: https://help.openai.com/
- Community: https://community.openai.com/

---

## 📌 Quick Reference

### Copy-Paste Template for .env

```env
# === REQUIRED ===
GEMINI_API_KEY=paste_your_key_here
ELEVENLABS_API_KEY=paste_your_key_here

# === OPTIONAL ===
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
OPENAI_API_KEY=paste_your_key_here
```

### Key Format Examples
```
Gemini:      AIzaSyA_1234567890abcdef
ElevenLabs:  abc123def456ghi789jkl012
Voice ID:    EXAVITQu4vr4xnSDxMaL
OpenAI:      sk-proj-abc123...
```

---

## 🎉 Next Steps

Once you have your keys:

1. ✅ Add them to `backend\.env`
2. ✅ Run `start-backend.bat`
3. ✅ Run `start-frontend.bat`
4. ✅ Open http://localhost:5173
5. ✅ Start interviewing!

---

**Need help? See QUICKSTART.md or open an issue!**
