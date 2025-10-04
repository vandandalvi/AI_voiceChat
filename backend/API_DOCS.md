# Talkito Backend API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### Health Check
**GET** `/health`

Check if the server is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

---

### Start Interview
**POST** `/start-interview`

Initialize a new interview session and get the AI greeting as audio.

**Response:**
- Content-Type: `audio/mpeg`
- Body: MP3 audio file

**Example:**
```javascript
const response = await fetch('http://localhost:5000/api/start-interview', {
  method: 'POST'
});
const audioBlob = await response.blob();
```

---

### Process Audio
**POST** `/process-audio`

Process user's audio recording through the full pipeline:
1. Convert audio format using FFmpeg
2. Transcribe speech to text (STT)
3. Get AI response from Gemini
4. Convert response to speech (TTS)

**Request:**
- Content-Type: `multipart/form-data`
- Body: FormData with `audio` field (WebM audio file)

**Response:**
```json
{
  "user_text": "I've been developing web apps for 3 years...",
  "ai_response": "That's great! Can you tell me about your experience with React?",
  "audio_url": "/api/get-latest-audio"
}
```

**Example:**
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.webm');

const response = await fetch('http://localhost:5000/api/process-audio', {
  method: 'POST',
  body: formData
});
const data = await response.json();
```

---

### Text to Speech
**POST** `/text-to-speech`

Convert text to speech using ElevenLabs.

**Request:**
```json
{
  "text": "Hello, how are you?"
}
```

**Response:**
- Content-Type: `audio/mpeg`
- Body: MP3 audio file

**Example:**
```javascript
const response = await fetch('http://localhost:5000/api/text-to-speech', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ text: 'Hello!' })
});
const audioBlob = await response.blob();
```

---

### Get Conversation History
**GET** `/conversation-history`

Retrieve the conversation history.

**Response:**
```json
{
  "history": [
    {
      "role": "assistant",
      "content": "Hello, tell me about yourself."
    },
    {
      "role": "user",
      "content": "I'm a web developer..."
    }
  ]
}
```

---

### Reset Conversation
**POST** `/reset`

Clear the conversation history.

**Response:**
```json
{
  "message": "Conversation reset"
}
```

---

## Error Responses

All endpoints may return error responses:

```json
{
  "error": "Error message description"
}
```

Common status codes:
- `400`: Bad Request (missing parameters)
- `500`: Internal Server Error (API failures, processing errors)

---

## Configuration

Set these environment variables in `.env`:

```bash
GEMINI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
ELEVENLABS_VOICE_ID=voice_id_here  # Optional
```

---

## Notes

1. **Speech-to-Text**: Current implementation uses a placeholder. Integrate with:
   - OpenAI Whisper API
   - Google Cloud Speech-to-Text
   - Azure Speech Services

2. **Rate Limits**: Be aware of API rate limits for Gemini and ElevenLabs

3. **Audio Format**: Input audio should be WebM format from browser MediaRecorder
