# AI Voice chat 🎙️# 🎙️ Talkito AI Interview Platform



An AI-powered interview assistant that conducts voice-based technical interviews using Google Gemini AI and ElevenLabs text-to-speech.An AI-powered interview platform that conducts realistic technical interviews using voice interaction. Built with React, Flask, ElevenLabs TTS, Gemini AI, and FFmpeg.



## ✨ Features## 🌟 Features



- 🎤 **Voice-to-Voice Interaction** - Speak naturally and get AI responses- **Voice-Based Interview**: Natural conversation with AI interviewer

- 🤖 **AI-Powered** - Uses Google Gemini 2.0 Flash for intelligent responses  - **Real-time Speech Processing**: Uses FFmpeg for audio processing

- 🗣️ **Natural Speech** - ElevenLabs API for human-like voice synthesis- **AI-Powered Responses**: Gemini 2.0 Flash for intelligent conversation

- 🎯 **Technical Interviews** - Designed for web development interviews- **Natural Voice**: ElevenLabs text-to-speech for human-like voice

- 🔄 **Conversation Flow** - Maintains context throughout the interview- **Interactive UI**: Clean, modern React interface

- **Conversation History**: Track the entire interview dialogue

## 🚀 Quick Setup

## 🏗️ Architecture

### 1. Clone Repository

```bash```

git clone https://github.com/vandandalvi/AI_voiceChat.gitUser speaks → FFmpeg Audio Processing → Speech-to-Text → Gemini AI → ElevenLabs TTS → AI speaks

cd AI_voiceChat```

```

## 📋 Prerequisites

### 2. Backend Setup

```bash- Python 3.8+

cd backend- Node.js 16+

pip install -r requirements.txt- FFmpeg (included in project)

```- Gemini API Key

- ElevenLabs API Key

### 3. Configure API Keys

```bash## 🚀 Setup Instructions

# Copy example file

copy .env.example .env### Backend Setup



# Edit .env and add your API keys:1. Navigate to backend directory:

GEMINI_API_KEY=your_gemini_api_key_here```powershell

ELEVENLABS_API_KEY=your_elevenlabs_api_key_herecd backend

ELEVENLABS_VOICE_ID=nPczCjzI2devNBz1zQrb```

```

2. Create a virtual environment:

### 4. Get API Keys```powershell

python -m venv venv

**Gemini API (Required):**```

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Create API key and add to `.env`3. Activate virtual environment:

```powershell

**ElevenLabs API (Required):**.\venv\Scripts\Activate.ps1

1. Sign up at [ElevenLabs](https://elevenlabs.io/)```

2. Get API key from Profile → API Keys

3. Browse [Voice Library](https://elevenlabs.io/voice-library) for Voice IDs4. Install dependencies:

```powershell

### 5. Run Backendpip install -r requirements.txt

```bash```

python app.py

```5. Create `.env` file from `.env.example`:

Backend runs on `http://localhost:5000````powershell

cp .env.example .env

### 6. Frontend Setup```

```bash

cd frontend/vite-project6. Edit `.env` and add your API keys:

npm install```

npm run devGEMINI_API_KEY=your_gemini_api_key_here

```ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

Frontend runs on `http://localhost:5173`ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL

```

## 🎯 Usage

7. Run the Flask server:

1. Open `http://localhost:5173````powershell

2. Click **"Start Interview"** python app.py

3. Wait for AI greeting```

4. Click **"Start Speaking"** to respond

5. Click **"Stop Speaking"** when doneThe backend will run on `http://localhost:5000`

6. Continue the conversation!

### Frontend Setup

## 🛠️ Tech Stack

1. Navigate to frontend directory:

- **Backend:** Flask, Python 3.13```powershell

- **Frontend:** React 19, Vitecd frontend\vite-project

- **AI:** Google Gemini 2.0 Flash```

- **TTS:** ElevenLabs Flash v2.5 

- **STT:** Google Speech Recognition2. Install dependencies:

- **Audio:** FFmpeg (included)```powershell

npm install

## ⚙️ Configuration```



### Voice Settings (in `app.py`)3. Run the development server:

```python```powershell

"voice_settings": {npm run dev

    "stability": 0.3,        # Lower = more expressive  ```

    "similarity_boost": 0.8, # Higher = closer to voice

    "style": 0.3,            # Style exaggerationThe frontend will run on `http://localhost:5173`

    "use_speaker_boost": True # Enhanced clarity

}## 🔑 Getting API Keys

```

### Gemini API Key

### ElevenLabs Models (in `.env`)1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)

- `eleven_flash_v2_5` - Fastest, lowest cost ✅2. Click "Get API Key"

- `eleven_turbo_v2_5` - High quality, fast3. Create a new project or select existing

- `eleven_multilingual_v2` - 44 languages4. Copy your API key



## 🔧 Troubleshooting### ElevenLabs API Key

1. Go to [ElevenLabs](https://elevenlabs.io/)

**ElevenLabs 401 Error:** Set `USE_GTTS_FALLBACK=true` in `.env`2. Sign up for an account

**No Microphone:** Grant browser permissions3. Navigate to Profile Settings

**CORS Errors:** Ensure Flask-CORS is installed4. Copy your API key

5. (Optional) Go to Voice Library to get custom Voice IDs

## 📁 Project Structure

## 🎯 Usage

```

AI_voiceChat/1. Start both backend and frontend servers

├── backend/2. Open browser to `http://localhost:5173`

│   ├── app.py              # Main Flask server3. Click "Start Interview"

│   ├── requirements.txt    # Dependencies4. Wait for the AI to speak the greeting

│   ├── .env.example        # API keys template5. Click "Start Speaking" to respond

│   └── .env                # Your API keys (git ignored)6. Click "Stop Speaking" when done

├── frontend/vite-project/  # React frontend7. Continue the conversation!

├── ffmpeg-8.0-essentials_build/  # Audio processing

└── README.md## 📁 Project Structure

```

```

## 📜 LicensetalkitoP1/

├── backend/

MIT License - Free to use and modify!│   ├── app.py              # Flask server with API endpoints

│   ├── requirements.txt    # Python dependencies

---│   ├── .env.example        # Environment variables template

│   └── .gitignore         # Git ignore file

**Built with ❤️ using Flask, React, Gemini AI & ElevenLabs**├── frontend/
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
