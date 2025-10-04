# 🚀 Quick Start Guide - Talkito AI Interview

## Prerequisites Checklist
- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] Gemini API Key from Google AI Studio
- [ ] ElevenLabs API Key
- [ ] (Optional) OpenAI API Key for Whisper speech-to-text

---

## 🔥 Quick Setup (5 minutes)

### Step 1: Get API Keys

#### Gemini API Key (Required)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Create or select a project
4. Copy the API key

#### ElevenLabs API Key (Required)
1. Visit: https://elevenlabs.io/
2. Sign up for a free account
3. Go to Profile → API Keys
4. Copy your API key

#### OpenAI API Key (Optional - for better speech recognition)
1. Visit: https://platform.openai.com/api-keys
2. Create an account
3. Generate a new API key
4. Copy it (you'll need credits for Whisper API)

### Step 2: Run Setup Script

Simply double-click: **`setup.bat`**

This will:
- Create Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Create `.env` file template

### Step 3: Add Your API Keys

1. Open `backend\.env` in a text editor
2. Replace the placeholder values:

```env
GEMINI_API_KEY=your_actual_gemini_key_here
ELEVENLABS_API_KEY=your_actual_elevenlabs_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional
```

3. Save the file

### Step 4: Start the Application

**Option A: Using Batch Files (Easiest)**
1. Double-click **`start-backend.bat`** (starts Flask server)
2. Double-click **`start-frontend.bat`** (starts React app)

**Option B: Manual Start**

Terminal 1 (Backend):
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

Terminal 2 (Frontend):
```powershell
cd frontend\vite-project
npm run dev
```

### Step 5: Open the App

Open your browser to: **http://localhost:5173**

---

## 🎙️ Using the Application

1. **Start Interview**: Click the "Start Interview" button
2. **Listen**: Wait for the AI to speak the greeting
3. **Respond**: Click "Start Speaking" and talk to your microphone
4. **Stop**: Click "Stop Speaking" when you're done
5. **Continue**: The AI will process and respond to you
6. **Repeat**: Continue the conversation!

---

## 🔧 Choosing Speech-to-Text Implementation

### Option 1: Without Speech-to-Text (Testing Only)
Use the default `app.py` - it will show placeholder text instead of actual transcription.

**Pros:** No additional API costs
**Cons:** Can't actually transcribe your speech

### Option 2: With OpenAI Whisper (Recommended)
Use `app_with_whisper.py` instead of `app.py`

1. Rename files:
   ```powershell
   cd backend
   move app.py app_basic.py
   move app_with_whisper.py app.py
   move requirements.txt requirements_basic.txt
   move requirements_with_whisper.txt requirements.txt
   ```

2. Install new requirements:
   ```powershell
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Add OpenAI API key to `.env`

**Pros:** Excellent accuracy, easy to use
**Cons:** Costs $0.006 per minute of audio

### Option 3: Other Services
See `README.md` for integration examples with:
- Google Cloud Speech-to-Text
- Azure Speech Services

---

## 🎛️ Configuration Options

### Change AI Voice

1. Visit [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
2. Browse and preview voices
3. Click on a voice you like
4. Copy the Voice ID
5. Update in `.env`:
   ```env
   ELEVENLABS_VOICE_ID=your_voice_id_here
   ```

### Customize Interview Questions

Edit `backend/app.py`:

```python
# Line ~49: Change the greeting
greeting = "Your custom greeting here"

# Line ~166: Change AI personality
context = """You are [your custom interviewer personality]..."""
```

### Adjust Voice Settings

Edit `backend/app.py` in the `text_to_speech()` function:

```python
"voice_settings": {
    "stability": 0.5,        # 0-1: Higher = more consistent
    "similarity_boost": 0.75, # 0-1: Higher = closer to original
    "style": 0.0,            # 0-1: Exaggeration level
    "use_speaker_boost": True # Enhance clarity
}
```

---

## ⚠️ Troubleshooting

### Backend won't start
**Error:** "Python not found"
- Install Python from python.org
- Make sure "Add to PATH" was checked during installation

**Error:** "Module not found"
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error:** "Port 5000 already in use"
- Edit `app.py`, change port:
  ```python
  app.run(debug=True, port=5001)
  ```
- Update frontend API URL in `src/App.jsx`

### Frontend won't start
**Error:** "npm not found"
- Install Node.js from nodejs.org

**Error:** "Cannot find module"
```powershell
cd frontend\vite-project
rm -r node_modules
npm install
```

### Microphone Issues
- Grant microphone permissions in your browser
- Use Chrome or Edge (best compatibility)
- Check browser settings: Settings → Privacy → Microphone

### API Errors
- Double-check your API keys in `.env`
- Ensure no extra spaces or quotes
- Restart the backend after editing `.env`
- Check API quotas/credits

### FFmpeg Issues
**Error:** "FFmpeg not found"
- Verify path in `app.py` line ~34
- Make sure `ffmpeg-8.0-essentials_build/bin/ffmpeg.exe` exists

---

## 💡 Tips for Best Experience

1. **Use a good microphone**: Built-in laptop mics work, but headset mics are better
2. **Quiet environment**: Reduces background noise
3. **Clear speech**: Speak naturally but clearly
4. **Wait for AI**: Let the AI finish speaking before responding
5. **Chrome/Edge**: Best browser compatibility for audio

---

## 📊 Cost Estimates

### Free Tier Limits
- **Gemini 2.0 Flash**: 1500 requests/day (generous free tier)
- **ElevenLabs**: 10,000 characters/month free
- **OpenAI Whisper**: $0.006/minute (no free tier)

### Typical Interview Costs
- 10-minute interview with Whisper: ~$0.06
- AI responses: Free (within Gemini limits)
- Voice generation: Free (within ElevenLabs limits)

---

## 🆘 Getting Help

### Check These First
1. Backend terminal output for errors
2. Browser console (F12) for frontend errors
3. Verify all API keys are correct
4. Restart both servers

### Still Having Issues?
1. Check the main `README.md` for detailed docs
2. Review `backend/API_DOCS.md` for API details
3. Open an issue on GitHub

---

## 🎉 Next Steps

Once everything is working:
- [ ] Customize the AI interviewer personality
- [ ] Try different ElevenLabs voices
- [ ] Modify interview questions for your needs
- [ ] Add more advanced features
- [ ] Share with others!

---

**Enjoy your AI interview! 🚀**
