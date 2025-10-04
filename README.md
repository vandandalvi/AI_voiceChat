# 🎙️ Talkito AI Interview Platform

An AI-powered interview platform that conducts realistic technical interviews using voice interaction. Built with React, Flask, ElevenLabs TTS, Gemini AI, and FFmpeg.

## 🌟 Features

- **Voice-Based Interview**: Natural conversation with AI interviewer
- **Real-time Speech Processing**: Uses FFmpeg for audio processing
- **AI-Powered Responses**: Gemini 2.0 Flash for intelligent conversation
- **Natural Voice**: ElevenLabs text-to-speech for human-like voice
- **Interactive UI**: Clean, modern React interface
- **Conversation History**: Track the entire interview dialogue

## 🏗️ Architecture

```
User speaks → FFmpeg Audio Processing → Speech-to-Text → Gemini AI → ElevenLabs TTS → AI speaks
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- FFmpeg (included in project)
- Gemini API Key
- ElevenLabs API Key

## 🚀 Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```powershell
cd backend
```

2. Create a virtual environment:
```powershell
python -m venv venv
```

3. Activate virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:
```powershell
pip install -r requirements.txt
```

5. Create `.env` file from `.env.example`:
```powershell
cp .env.example .env
```

6. Edit `.env` and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
```

7. Run the Flask server:
```powershell
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```powershell
cd frontend\vite-project
```

2. Install dependencies:
```powershell
npm install
```

3. Run the development server:
```powershell
npm run dev
```

The frontend will run on `http://localhost:5173`

## 🔑 Getting API Keys

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new project or select existing
4. Copy your API key

### ElevenLabs API Key
1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for an account
3. Navigate to Profile Settings
4. Copy your API key
5. (Optional) Go to Voice Library to get custom Voice IDs

## 🎯 Usage

1. Start both backend and frontend servers
2. Open browser to `http://localhost:5173`
3. Click "Start Interview"
4. Wait for the AI to speak the greeting
5. Click "Start Speaking" to respond
6. Click "Stop Speaking" when done
7. Continue the conversation!

## 📁 Project Structure

```
talkitoP1/
├── backend/
│   ├── app.py              # Flask server with API endpoints
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variables template
│   └── .gitignore         # Git ignore file
├── frontend/
│   └── vite-project/
│       ├── src/
│       │   ├── App.jsx    # Main React component
│       │   ├── App.css    # Styles
│       │   └── index.css  # Global styles
│       └── package.json   # Node dependencies
└── ffmpeg-8.0-essentials_build/
    └── bin/
        └── ffmpeg.exe     # FFmpeg executable
```

## 🔧 API Endpoints

### `POST /api/start-interview`
Start a new interview session and get greeting audio

### `POST /api/process-audio`
Process user audio: STT → AI → TTS
- Body: FormData with `audio` file

### `POST /api/text-to-speech`
Convert text to speech
- Body: `{ "text": "string" }`

### `GET /api/conversation-history`
Get conversation history

### `POST /api/reset`
Reset conversation

## ⚠️ Important Notes

### Speech-to-Text Integration
The current implementation includes a **placeholder** for speech-to-text conversion. You need to integrate one of these services:

#### Option 1: OpenAI Whisper API (Recommended)
```python
import openai

def speech_to_text(audio_path):
    with open(audio_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text
```

#### Option 2: Google Cloud Speech-to-Text
```python
from google.cloud import speech

def speech_to_text(audio_path):
    client = speech.SpeechClient()
    with open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript
```

#### Option 3: Azure Speech Services
```python
import azure.cognitiveservices.speech as speechsdk

def speech_to_text(audio_path):
    speech_config = speechsdk.SpeechConfig(
        subscription="YOUR_KEY", 
        region="YOUR_REGION"
    )
    audio_config = speechsdk.AudioConfig(filename=audio_path)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )
    result = speech_recognizer.recognize_once()
    return result.text
```

## 🐛 Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `app.py`: `app.run(port=5001)`
- **API key errors**: Double-check your `.env` file
- **FFmpeg not found**: Verify FFmpeg path in `app.py`

### Frontend Issues
- **CORS errors**: Ensure Flask-CORS is installed and configured
- **Microphone access denied**: Grant browser microphone permissions
- **No audio playback**: Check browser audio permissions

### Audio Issues
- **Recording doesn't work**: Check browser compatibility (Chrome/Edge recommended)
- **Poor audio quality**: Adjust ElevenLabs voice settings in `app.py`

## 🎨 Customization

### Change AI Interviewer Personality
Edit the context in `app.py` → `get_gemini_response()`:
```python
context = """You are a [YOUR_PERSONALITY] interviewer..."""
```

### Change Voice
1. Get voice ID from [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
2. Update `ELEVENLABS_VOICE_ID` in `.env`

### Modify Interview Questions
Edit the greeting in `app.py` → `start_interview()`:
```python
greeting = "Your custom greeting here"
```

## 📝 License

MIT License

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📧 Support

For issues and questions, please open a GitHub issue.

---

Built with ❤️ using React, Flask, Gemini AI, ElevenLabs, and FFmpeg
