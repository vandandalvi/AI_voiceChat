# 🎤 How to Enable Speech-to-Text (Whisper)

Your interview app now supports **real speech-to-text** using OpenAI Whisper!

## Current Status

**Without OpenAI Key:**
- ❌ Shows: `[Please add OPENAI_API_KEY to .env to enable speech recognition]`
- ❌ AI won't understand what you actually said

**With OpenAI Key:**
- ✅ Your speech is accurately transcribed
- ✅ AI responds based on what you actually said
- ✅ Full natural conversation

---

## 🔑 Getting OpenAI API Key (5 minutes)

### Step 1: Create OpenAI Account
1. Go to: **https://platform.openai.com/signup**
2. Sign up with email or Google/Microsoft account
3. Verify your email
4. Complete phone verification

### Step 2: Add Payment Method
1. Go to: **https://platform.openai.com/settings/organization/billing/overview**
2. Click **"Add payment method"**
3. Add your credit card
4. **Add credits**: Minimum $5 (recommended: $10)
   - This will last for 100+ interviews!

### Step 3: Create API Key
1. Go to: **https://platform.openai.com/api-keys**
2. Click **"+ Create new secret key"**
3. Name it: "Talkito Interview"
4. Click **"Create secret key"**
5. **COPY THE KEY IMMEDIATELY** (you won't see it again!)
   - It looks like: `sk-proj-abc123...`

### Step 4: Add to Your Project
1. Open `backend\.env` in a text editor
2. Find the line: `OPENAI_API_KEY=`
3. Paste your key after the `=`
   ```env
   OPENAI_API_KEY=sk-proj-your_actual_key_here
   ```
4. Save the file

### Step 5: Restart Backend
1. Stop the current backend (Ctrl+C in terminal)
2. Run: `python c:\projects\talkitoP1\backend\app.py`
3. You should see: `✓ Speech-to-Text: OpenAI Whisper`

---

## 💰 Cost Breakdown

### Whisper API Pricing
- **Cost**: $0.006 per minute of audio
- **Typical recording**: 10-30 seconds each

### Example Costs
- **1 recording (15 sec)**: $0.0015 (~¢0.15)
- **10-minute interview**: ~$0.06 (6 cents)
- **100 interviews**: ~$6.00
- **$10 credit**: ~160 interviews

**Bottom line**: Very affordable! $5-10 will last you a long time.

---

## ⚙️ How It Works

### When You Speak:
1. **Record**: Browser captures your voice
2. **Send**: Audio sent to backend
3. **Convert**: FFmpeg converts WebM → MP3
4. **Transcribe**: OpenAI Whisper → Text ✨
5. **Display**: You see what you said
6. **Process**: Gemini AI generates response
7. **Speak**: gTTS converts to audio
8. **Play**: You hear AI's response

---

## 🧪 Testing Without OpenAI Key

If you want to test before adding OpenAI:

**What Works:**
- ✅ UI and buttons
- ✅ Audio recording
- ✅ AI generates responses
- ✅ Text-to-speech (gTTS)

**What Shows Placeholder:**
- ⚠️ Your speech shows as: `[Please add OPENAI_API_KEY...]`
- ⚠️ AI won't respond to your actual words

---

## 🔒 Security Tips

- ✅ Never share your API key
- ✅ Never commit `.env` to Git (already in `.gitignore`)
- ✅ Set spending limits in OpenAI dashboard
- ✅ Monitor usage regularly

---

## 📊 Monitor Usage

1. Go to: **https://platform.openai.com/usage**
2. Check your daily usage
3. Set up email alerts for spending limits

---

## ⚡ Quick Commands

### Check if Whisper is enabled:
```powershell
cd c:\projects\talkitoP1\backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✓ OpenAI Key Found!' if os.getenv('OPENAI_API_KEY') else '✗ No OpenAI Key')"
```

### Test your OpenAI key:
```powershell
python -c "import openai, os; from dotenv import load_dotenv; load_dotenv(); openai.api_key=os.getenv('OPENAI_API_KEY'); print(openai.models.list().data[0])"
```

---

## 🆘 Troubleshooting

### Error: "Invalid API key"
- Check for spaces before/after the key
- Make sure you copied the entire key
- Regenerate a new key

### Error: "Insufficient credits"
- Add more credits to your OpenAI account
- Check: https://platform.openai.com/settings/organization/billing/overview

### Error: "Rate limit exceeded"
- You're making too many requests
- Wait a few seconds between requests
- Upgrade your tier if needed

---

## 🎉 You're Done!

Once you add the OpenAI key:
1. You'll see your actual speech transcribed
2. AI will respond to what you actually said
3. Full natural conversation experience!

**Cost**: About 6 cents per 10-minute interview
**Value**: Priceless for realistic interview practice! 🚀

---

**Ready to add your key?**
1. Get key from: https://platform.openai.com/api-keys
2. Add to: `backend\.env`
3. Restart backend
4. Start interviewing! 🎙️
