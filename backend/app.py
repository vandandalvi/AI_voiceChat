from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import tempfile
from pathlib import Path
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import io

# Try to import gTTS, fallback if not available
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️  gTTS not installed. Install with: pip install gTTS")

# Try to import speech_recognition for STT
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    print("⚠️  SpeechRecognition not installed. Install with: pip install SpeechRecognition")

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL')
USE_GTTS_FALLBACK = os.getenv('USE_GTTS_FALLBACK', 'true').lower() == 'true'
VOICE_SPEED = float(os.getenv('VOICE_SPEED', '1.15'))
GTTS_TLD = os.getenv('GTTS_TLD', 'com')
ELEVENLABS_MODEL = os.getenv('ELEVENLABS_MODEL', 'eleven_turbo_v2_5')  # Latest model

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Conversation history
conversation_history = []

# FFmpeg path
FFMPEG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                           'ffmpeg-8.0-essentials_build', 'bin', 'ffmpeg.exe')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    """Initialize interview and return the first greeting"""
    global conversation_history
    conversation_history = []
    
    greeting = "Hello, Myself Talkito Technician Assistant at ElevenLabs California. So tell me about your web development journey."
    
    # Add to conversation history
    conversation_history.append({
        'role': 'assistant',
        'content': greeting
    })
    
    # Generate audio using ElevenLabs or gTTS fallback
    audio_data = text_to_speech(greeting)
    
    if audio_data:
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/mpeg',
            as_attachment=False
        )
    else:
        return jsonify({'error': 'Failed to generate speech'}), 500

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    """Process user audio: speech-to-text -> Gemini -> text-to-speech"""
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
        audio_file.save(temp_audio.name)
        temp_audio_path = temp_audio.name
    
    try:
        # Convert audio to text
        user_text = speech_to_text(temp_audio_path)
        
        if not user_text:
            return jsonify({'error': 'Failed to transcribe audio'}), 500
        
        # Add user message to conversation history
        conversation_history.append({
            'role': 'user',
            'content': user_text
        })
        
        # Get AI response from Gemini
        ai_response = get_gemini_response(user_text)
        
        if not ai_response:
            return jsonify({'error': 'Failed to get AI response'}), 500
        
        # Add AI response to conversation history
        conversation_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        # Convert AI response to speech
        audio_data = text_to_speech(ai_response)
        
        if audio_data:
            return jsonify({
                'user_text': user_text,
                'ai_response': ai_response,
                'audio_url': '/api/get-latest-audio'
            })
        else:
            return jsonify({'error': 'Failed to generate speech'}), 500
            
    finally:
        # Cleanup
        if os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech_endpoint():
    """Convert text to speech and return audio"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    audio_data = text_to_speech(text)
    
    if audio_data:
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/mpeg',
            as_attachment=False
        )
    else:
        return jsonify({'error': 'Failed to generate speech'}), 500

def speech_to_text(audio_path):
    """Convert audio to text using Google Speech Recognition (free)"""
    # Convert to WAV format using FFmpeg
    output_path = audio_path.replace('.webm', '.wav')
    
    try:
        # Convert audio format
        subprocess.run([
            FFMPEG_PATH,
            '-i', audio_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            output_path,
            '-y'
        ], check=True, capture_output=True)
        
        # Use Google Speech Recognition (free)
        if SR_AVAILABLE:
            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(output_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    print(f"✓ Transcribed: {text}")
                    return text
            except sr.UnknownValueError:
                print("⚠️  Could not understand audio")
                return "[Could not understand audio - please speak clearly]"
            except sr.RequestError as e:
                print(f"⚠️  Speech recognition error: {e}")
                return "[Speech recognition service error]"
            except Exception as e:
                print(f"⚠️  Transcription error: {e}")
                return "[Transcription failed]"
        else:
            print("⚠️  SpeechRecognition not available - using placeholder")
            return "[Audio transcription placeholder - install SpeechRecognition]"
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        return None
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)

def get_gemini_response(user_message):
    """Get response from Gemini AI"""
    try:
        # Create context for the interview
        context = """You are Talkito, a friendly technical assistant at ElevenLabs California. 
        You are conducting a technical interview focused on web development. 
        Ask relevant follow-up questions, provide encouragement, and maintain a professional yet warm tone.
        Keep responses concise and conversational (2-3 sentences max)."""
        
        # Build conversation context
        full_prompt = f"{context}\n\nConversation history:\n"
        for msg in conversation_history[-6:]:  # Last 3 exchanges
            role = "Interviewer" if msg['role'] == 'assistant' else "Candidate"
            full_prompt += f"{role}: {msg['content']}\n"
        
        full_prompt += f"\nCandidate: {user_message}\nInterviewer:"
        
        # Generate response
        response = model.generate_content(full_prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None

def speed_up_audio(audio_data, speed=1.15):
    """Speed up audio using FFmpeg to make it sound more natural"""
    try:
        # Save input audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_input:
            temp_input.write(audio_data)
            temp_input_path = temp_input.name
        
        # Create output temp file
        temp_output_path = temp_input_path.replace('.mp3', '_fast.mp3')
        
        # Use FFmpeg to speed up audio
        # atempo filter: 1.0 = normal, 1.35 = 35% faster (more natural speaking pace)
        subprocess.run([
            FFMPEG_PATH,
            '-i', temp_input_path,
            '-filter:a', f'atempo={speed}',
            '-vn',  # No video
            temp_output_path,
            '-y'
        ], check=True, stderr=subprocess.DEVNULL)
        
        # Read the sped-up audio
        with open(temp_output_path, 'rb') as f:
            fast_audio = f.read()
        
        # Cleanup
        os.unlink(temp_input_path)
        os.unlink(temp_output_path)
        
        return fast_audio
        
    except Exception as e:
        print(f"Speed adjustment failed: {e}")
        return audio_data  # Return original if speed adjustment fails

def text_to_speech(text):
    """Convert text to speech using ElevenLabs or gTTS fallback"""
    
    # Try ElevenLabs first if not using fallback mode
    if not USE_GTTS_FALLBACK and ELEVENLABS_API_KEY:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            
            # Using official ElevenLabs API structure with optimized settings for natural speech
            data = {
                "text": text,
                "model_id": ELEVENLABS_MODEL,  # eleven_turbo_v2_5 for fastest, most natural speech
                "voice_settings": {
                    "stability": 0.3,           # 0-1: Lower = MORE expressive and dynamic (0.3-0.5 for conversational)
                    "similarity_boost": 0.8,    # 0-1: Higher = closer to original voice character
                    "style": 0.3,               # 0-1: Style exaggeration for more personality (0.2-0.4 recommended)
                    "use_speaker_boost": True   # Enhance clarity and presence
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                print(f"✓ Using ElevenLabs TTS (Voice: {ELEVENLABS_VOICE_ID}, Model: {ELEVENLABS_MODEL})")
                return response.content
            else:
                print(f"⚠️  ElevenLabs API error: {response.status_code}")
                print(f"   Falling back to gTTS...")
        except Exception as e:
            print(f"⚠️  ElevenLabs error: {e}")
            print(f"   Falling back to gTTS...")
    
    # Use gTTS as fallback
    if GTTS_AVAILABLE:
        try:
            print("✓ Using gTTS (Google Text-to-Speech) - Free")
            
            # Use different accents/domains for more natural voice
            # Options: 'com' (US), 'co.uk' (UK), 'com.au' (AU), 'co.in' (India)
            tts = gTTS(text=text, lang='en', slow=False, tld=GTTS_TLD)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            audio_data = audio_buffer.read()
            
            # Speed up the audio using FFmpeg for more natural pace
            try:
                audio_data = speed_up_audio(audio_data, speed=VOICE_SPEED)
                print(f"  → Voice speed: {VOICE_SPEED}x, Accent: {GTTS_TLD}")
            except Exception as e:
                print(f"⚠️  Could not speed up audio: {e}")
            
            return audio_data
            
        except Exception as e:
            print(f"❌ gTTS error: {e}")
            return None
    else:
        print("❌ No TTS service available")
        return None

@app.route('/api/conversation-history', methods=['GET'])
def get_conversation_history():
    """Get the conversation history"""
    return jsonify({'history': conversation_history})

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation"""
    global conversation_history
    conversation_history = []
    return jsonify({'message': 'Conversation reset'})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎙️  Talkito AI Interview Backend")
    print("="*50)
    print(f"✓ Gemini API: {'Configured' if GEMINI_API_KEY else '❌ NOT CONFIGURED'}")
    print(f"✓ ElevenLabs: {'Configured' if ELEVENLABS_API_KEY else '❌ NOT CONFIGURED'}")
    if USE_GTTS_FALLBACK:
        print(f"✓ TTS Mode: gTTS (Free Google TTS)")
    else:
        print(f"✓ TTS Mode: ElevenLabs")
    print(f"✓ gTTS Available: {'Yes' if GTTS_AVAILABLE else '❌ No (run: pip install gTTS)'}")
    print(f"✓ Speech Recognition: {'Yes' if SR_AVAILABLE else '❌ No (run: pip install SpeechRecognition)'}")
    print(f"✓ FFmpeg: {'Found' if os.path.exists(FFMPEG_PATH) else '❌ NOT FOUND'}")
    print("="*50)
    print("Server starting on http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
