# Project Structure & File Guide

## 📁 Complete Project Structure

```
talkitoP1/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md               # Quick setup guide
├── 📄 setup.bat                   # Automated setup script
├── 📄 start-backend.bat           # Backend launcher
├── 📄 start-frontend.bat          # Frontend launcher
│
├── 📂 backend/                    # Flask API Server
│   ├── app.py                     # Main Flask app (basic)
│   ├── app_with_whisper.py        # Flask app with Whisper STT
│   ├── requirements.txt           # Python dependencies (basic)
│   ├── requirements_with_whisper.txt  # With OpenAI
│   ├── .env.example               # Environment variables template
│   ├── .env                       # Your API keys (create this!)
│   ├── .gitignore                 # Git ignore rules
│   ├── API_DOCS.md                # API endpoint documentation
│   └── venv/                      # Python virtual environment
│
├── 📂 frontend/                   # React Frontend
│   └── vite-project/
│       ├── package.json           # Node dependencies
│       ├── vite.config.js         # Vite configuration
│       ├── index.html             # HTML template
│       ├── .gitignore
│       │
│       ├── src/                   # Source code
│       │   ├── main.jsx           # App entry point
│       │   ├── App.jsx            # Main React component
│       │   ├── App.css            # Main styles
│       │   └── index.css          # Global styles
│       │
│       ├── public/                # Static assets
│       │   └── vite.svg
│       │
│       └── node_modules/          # Installed packages
│
└── 📂 ffmpeg-8.0-essentials_build/  # Audio Processing
    ├── LICENSE
    ├── README.txt
    └── bin/
        ├── ffmpeg.exe             # Main audio converter
        ├── ffplay.exe
        └── ffprobe.exe
```

---

## 🔑 Key Files Explained

### Backend Files

#### `app.py` (Main Server)
**Purpose:** Flask API server that handles all backend logic

**Key Functions:**
- `start_interview()` - Initializes interview session
- `process_audio()` - Handles audio recording processing
- `speech_to_text()` - Converts audio to text (placeholder)
- `get_gemini_response()` - Gets AI responses
- `text_to_speech()` - Converts text to speech via ElevenLabs

**API Endpoints:**
- POST `/api/start-interview` - Start interview
- POST `/api/process-audio` - Process user audio
- POST `/api/text-to-speech` - Convert text to speech
- GET `/api/conversation-history` - Get conversation
- POST `/api/reset` - Reset interview

#### `app_with_whisper.py`
Enhanced version with OpenAI Whisper integration for actual speech-to-text transcription.

**Additional Features:**
- Real speech-to-text using Whisper API
- Better audio format conversion
- Startup diagnostics

**To Use:**
1. Get OpenAI API key
2. Rename to `app.py` or modify start script
3. Install requirements_with_whisper.txt

#### `.env` (Configuration)
**Purpose:** Store sensitive API keys and configuration

**Required Variables:**
```env
GEMINI_API_KEY=your_key          # Required
ELEVENLABS_API_KEY=your_key      # Required
ELEVENLABS_VOICE_ID=voice_id     # Optional (has default)
OPENAI_API_KEY=your_key          # Optional (for Whisper)
```

**Security Note:** Never commit this file to Git!

#### `requirements.txt`
Python package dependencies:
- `flask` - Web framework
- `flask-cors` - Enable CORS for React
- `google-generativeai` - Gemini AI
- `python-dotenv` - Load .env files
- `requests` - HTTP requests
- `openai` - (Whisper version only)

---

### Frontend Files

#### `src/App.jsx` (Main Component)
**Purpose:** Main React component with all interview logic

**Key State:**
- `isInterviewActive` - Interview started or not
- `isRecording` - Currently recording audio
- `isProcessing` - Processing request
- `isSpeaking` - AI is speaking
- `conversationHistory` - Chat history

**Key Functions:**
- `startInterview()` - Initialize interview
- `startRecording()` - Start audio recording
- `stopRecording()` - Stop and send audio
- `sendAudioToServer()` - Upload audio for processing
- `playAudio()` - Play AI response
- `resetInterview()` - End interview

**Audio Handling:**
- Uses MediaRecorder API
- Records in WebM format
- Auto-plays AI responses

#### `src/App.css` (Styles)
**Purpose:** All styling for the application

**Key Sections:**
- `.app` - Main container with gradient background
- `.header` - Title and subtitle
- `.welcome-card` - Initial start screen
- `.interview-active` - Active interview UI
- `.controls` - Button controls
- `.message` - Chat messages
- Animations (fadeIn, slideIn, pulse, bounce)

**Responsive Design:**
- Mobile-friendly layout
- Adjusts for screens < 768px width

#### `src/index.css` (Global Styles)
**Purpose:** Global CSS reset and base styles

**Contains:**
- CSS reset (margin, padding)
- Base font settings
- Root element height

#### `package.json` (Dependencies)
Node.js package configuration:

**Dependencies:**
- `react` - UI library
- `react-dom` - React DOM rendering

**Dev Dependencies:**
- `vite` - Build tool
- `@vitejs/plugin-react` - React plugin
- `eslint` - Code linting

---

### FFmpeg Files

#### `ffmpeg.exe`
**Purpose:** Convert audio formats

**Used For:**
- Converting WebM to MP3/WAV
- Resampling audio (16kHz)
- Channel conversion (mono)

**How It's Used:**
```python
subprocess.run([
    FFMPEG_PATH,
    '-i', input_file,      # Input
    '-acodec', 'libmp3lame',  # Codec
    '-ar', '16000',        # Sample rate
    '-ac', '1',            # Channels (mono)
    output_file,
    '-y'                   # Overwrite
])
```

---

### Helper Scripts

#### `setup.bat`
**Purpose:** One-click setup for the entire project

**What It Does:**
1. Creates Python virtual environment
2. Installs Python packages
3. Installs Node packages
4. Creates .env template
5. Verifies FFmpeg

**When to Use:** First time setup

#### `start-backend.bat`
**Purpose:** Launch Flask server

**What It Does:**
1. Activates Python venv
2. Installs/updates dependencies
3. Checks for .env file
4. Starts Flask server on port 5000

**When to Use:** Every time you want to run the backend

#### `start-frontend.bat`
**Purpose:** Launch React development server

**What It Does:**
1. Checks for node_modules
2. Installs dependencies if needed
3. Starts Vite dev server on port 5173

**When to Use:** Every time you want to run the frontend

---

## 🔄 Data Flow

### Starting Interview
```
User clicks button
    ↓
Frontend → POST /api/start-interview
    ↓
Backend: Generate greeting text
    ↓
Backend: ElevenLabs TTS → Audio
    ↓
Backend → Audio MP3 file
    ↓
Frontend: Play audio
```

### User Speaks
```
User clicks "Start Speaking"
    ↓
Frontend: MediaRecorder starts
    ↓
User speaks
    ↓
User clicks "Stop Speaking"
    ↓
Frontend: Create audio blob (WebM)
    ↓
Frontend → POST /api/process-audio (FormData)
    ↓
Backend: Save audio file
    ↓
Backend: FFmpeg convert to MP3
    ↓
Backend: Speech-to-Text (Whisper/placeholder)
    ↓
Backend: Gemini AI processes text
    ↓
Backend: Get AI response
    ↓
Backend: ElevenLabs TTS → Audio
    ↓
Backend → JSON {user_text, ai_response}
    ↓
Frontend: Display texts
    ↓
Frontend → POST /api/text-to-speech {ai_response}
    ↓
Backend → Audio MP3
    ↓
Frontend: Play audio
```

---

## 🔧 Customization Points

### Change Greeting
**File:** `backend/app.py`
**Line:** ~49
```python
greeting = "Your custom greeting"
```

### Change AI Personality
**File:** `backend/app.py`
**Line:** ~166
```python
context = """You are..."""
```

### Change Voice
**File:** `backend/.env`
```env
ELEVENLABS_VOICE_ID=new_voice_id
```

### Change Voice Settings
**File:** `backend/app.py`
**Function:** `text_to_speech()`
```python
"voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
}
```

### Change Colors/Styling
**File:** `frontend/vite-project/src/App.css`
**Lines:** 1-10 (CSS variables)
```css
:root {
  --primary-color: #4f46e5;
  --success-color: #10b981;
  --danger-color: #ef4444;
}
```

### Change API Base URL
**File:** `frontend/vite-project/src/App.jsx`
**Line:** 4
```javascript
const API_BASE_URL = 'http://localhost:5000/api'
```

---

## 🚀 Deployment Considerations

### Backend (Flask)
**For Production:**
- Use Gunicorn or uWSGI instead of Flask dev server
- Enable HTTPS
- Set `debug=False`
- Use environment variables for all secrets
- Add rate limiting
- Implement proper logging

### Frontend (React)
**For Production:**
- Run `npm run build`
- Serve the `dist/` folder
- Update `API_BASE_URL` to production URL
- Enable HTTPS
- Add error boundaries
- Implement analytics

### FFmpeg
- Include FFmpeg in deployment
- Update path for Linux/Mac: `/usr/bin/ffmpeg`
- Ensure executable permissions

---

## 📊 File Sizes

**Estimated Sizes:**
- `backend/` (with venv): ~200 MB
- `frontend/node_modules/`: ~300 MB
- `ffmpeg/`: ~100 MB
- Source code only: ~50 KB

**Git Repository:**
- Exclude venv, node_modules, .env
- Source code only: ~50 KB

---

## 🔒 Security Notes

### Never Commit:
- `.env` file
- API keys
- `venv/` folder
- `node_modules/` folder

### Best Practices:
- Use `.gitignore` (already included)
- Rotate API keys periodically
- Use environment variables in production
- Validate all user inputs
- Implement rate limiting
- Add CORS restrictions for production

---

## 📚 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/
- **Gemini AI**: https://ai.google.dev/
- **ElevenLabs**: https://docs.elevenlabs.io/
- **FFmpeg**: https://ffmpeg.org/documentation.html

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found"
**Solution:** Install dependencies
```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd frontend\vite-project
npm install
```

### Issue: "Port already in use"
**Solution:** Change port in code or kill process
```powershell
# Find process on port 5000
netstat -ano | findstr :5000
# Kill process (use PID from above)
taskkill /PID <pid> /F
```

### Issue: "CORS error"
**Solution:** Verify Flask-CORS is installed and configured
```python
from flask_cors import CORS
CORS(app)
```

### Issue: "Microphone not working"
**Solution:**
- Check browser permissions
- Use HTTPS or localhost
- Try Chrome or Edge

---

**For more help, see QUICKSTART.md or README.md**
