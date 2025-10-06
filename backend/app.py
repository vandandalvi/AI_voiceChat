import asyncio
import aiohttp
import concurrent.futures
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
import time
import threading

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
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'kHhWB9Fw3aF6ly7JvltC')
USE_GTTS_FALLBACK = os.getenv('USE_GTTS_FALLBACK', 'true').lower() == 'true'
VOICE_SPEED = float(os.getenv('VOICE_SPEED', '1.15'))
GTTS_TLD = os.getenv('GTTS_TLD', 'com')
ELEVENLABS_MODEL = os.getenv('ELEVENLABS_MODEL', 'eleven_turbo_v2_5')  # Latest model

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Conversation history
conversation_history = []

# FFmpeg path - automatically find FFmpeg folder
def find_ffmpeg_path():
    """Find FFmpeg executable in the project directory"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Look for ffmpeg folders (different versions users might download)
    possible_folders = [
        'ffmpeg-8.0-essentials_build',
        'ffmpeg-7.0-essentials_build', 
        'ffmpeg-6.1-essentials_build',
        'ffmpeg-release-essentials',
        'ffmpeg-essentials'
    ]
    
    for folder in possible_folders:
        ffmpeg_path = os.path.join(project_root, folder, 'bin', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path
    
    # Try to find any folder starting with 'ffmpeg'
    for item in os.listdir(project_root):
        if item.startswith('ffmpeg') and os.path.isdir(os.path.join(project_root, item)):
            ffmpeg_path = os.path.join(project_root, item, 'bin', 'ffmpeg.exe')
            if os.path.exists(ffmpeg_path):
                return ffmpeg_path
    
    return None

FFMPEG_PATH = find_ffmpeg_path()

# Optimization: Thread pool for concurrent processing
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

# Optimization: Gemini session for faster responses
chat_session = None

def initialize_gemini_chat():
    """Initialize persistent chat session for faster responses"""
    global chat_session
    try:
        # Use faster Gemini model configuration
        generation_config = {
            "temperature": 0.8,  # Slightly higher for more varied questions
            "top_p": 0.85,
            "max_output_tokens": 200,  # Allow longer, more detailed questions
        }
        
        model_fast = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            generation_config=generation_config
        )
        
        context = """You are Talkito, an advanced AI interview assistant specialized in technical assessments. 
        You conduct RIGOROUS, IN-DEPTH interviews with high professional standards. Your interview style:

        PERSONALITY:
        - Professional and direct approach
        - Drill down when answers lack technical depth
        - Ask challenging follow-up questions that test real understanding
        - Challenge candidates respectfully but firmly with scenario-based questions
        - Focus on technical depth, problem-solving methodology, and practical experience

        QUESTION TYPES:
        - Start with experience, then dive deep into technical specifics
        - Ask "How would you handle..." complex scenarios
        - Request concrete examples: "Tell me about a specific time when..."
        - Challenge with "What if..." hypothetical situations
        - Test edge cases and error handling knowledge
        - Probe architecture and scalability decisions

        RESPONSE STYLE:
        - Keep responses to 2-3 sentences max
        - Always ask ONE specific, challenging follow-up question
        - Don't accept vague answers - dig deeper
        - Use phrases like: "Can you be more specific?", "Walk me through...", "How exactly did you..."
        
        Remember: You're evaluating for a senior technical role. Set high standards."""
        
        chat_session = model_fast.start_chat(history=[
            {"role": "user", "parts": [context]},
            {"role": "model", "parts": ["Understood. I'm Talkito, and I'll conduct a rigorous technical interview with high standards. I'll ask in-depth questions and expect detailed, specific answers. Ready to begin the evaluation."]}
        ])
        print("✓ Strict interviewer chat session initialized")
    except Exception as e:
        print(f"⚠️ Could not initialize Gemini chat: {e}")

# Initialize chat session on startup
initialize_gemini_chat()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    """Initialize interview and return the first greeting"""
    global conversation_history
    conversation_history = []
    
    greeting = "Hello! I'm Talkito, your AI interview assistant. I'll be conducting a comprehensive technical assessment today to evaluate your skills thoroughly. Let's dive deep into your experience - tell me about your most challenging project and walk me through the specific technical decisions you made and why you chose those approaches."
    
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
    """OPTIMIZED: Process user audio with parallel processing"""
    start_time = time.time()
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
        audio_file.save(temp_audio.name)
        temp_audio_path = temp_audio.name
    
    try:
        print(f"🔄 Starting audio processing...")
        
        # OPTIMIZATION 1: Fast audio conversion (optimized FFmpeg settings)
        user_text = speech_to_text_fast(temp_audio_path)
        print(f"⏱️ STT completed in {time.time() - start_time:.2f}s")
        
        if not user_text:
            return jsonify({'error': 'Failed to transcribe audio'}), 500
        
        # Add user message to conversation history
        conversation_history.append({
            'role': 'user', 
            'content': user_text
        })
        
        # OPTIMIZATION 2: Fast AI response with chat session
        ai_start = time.time()
        ai_response = get_gemini_response_fast(user_text)
        print(f"⏱️ AI response in {time.time() - ai_start:.2f}s")
        
        if not ai_response:
            return jsonify({'error': 'Failed to get AI response'}), 500
        
        # Add AI response to conversation history
        conversation_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        # OPTIMIZATION 3: Start TTS in background while returning response
        def generate_audio_async():
            return text_to_speech_fast(ai_response)
        
        # Submit TTS task to thread pool
        future = executor.submit(generate_audio_async)
        
        print(f"🚀 Total processing time: {time.time() - start_time:.2f}s")
        
        return jsonify({
            'user_text': user_text,
            'ai_response': ai_response,
            'processing_time': round(time.time() - start_time, 2)
        })
            
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
    
    audio_data = text_to_speech_fast(text)
    
    if audio_data:
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/mpeg',
            as_attachment=False
        )
    else:
        return jsonify({'error': 'Failed to generate speech'}), 500

@app.route('/api/get-latest-audio', methods=['GET'])
def get_latest_audio():
    """Get the latest generated audio (for compatibility)"""
    # This endpoint is for backward compatibility
    # The frontend should use the direct audio from text-to-speech
    return jsonify({'message': 'Use /api/text-to-speech endpoint instead'})

def speech_to_text_fast(audio_path):
    """OPTIMIZED: Convert audio to text with faster FFmpeg settings"""
    # Convert to WAV format using optimized FFmpeg settings
    output_path = audio_path.replace('.webm', '.wav')
    
    try:
        # OPTIMIZATION: Faster FFmpeg conversion with reduced quality for speed
        subprocess.run([
            FFMPEG_PATH,
            '-i', audio_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',  # Lower sample rate for faster processing
            '-ac', '1',
            '-compression_level', '1',  # Fast compression
            output_path,
            '-y'
        ], check=True, capture_output=True, timeout=3)  # 3 second timeout
        
        # Use Google Speech Recognition (free)
        if SR_AVAILABLE:
            try:
                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 300  # Faster voice detection
                recognizer.dynamic_energy_threshold = False
                
                with sr.AudioFile(output_path) as source:
                    # OPTIMIZATION: Shorter audio duration for faster processing
                    audio_data = recognizer.record(source, duration=10)  # Max 10 seconds
                    text = recognizer.recognize_google(audio_data, language='en-US')
                    print(f"✓ Fast transcription: {text}")
                    return text
            except sr.UnknownValueError:
                return "[Could not understand audio - please speak clearly]"
            except sr.RequestError as e:
                print(f"⚠️ Speech recognition error: {e}")
                return "[Speech recognition service error]"
            except Exception as e:
                print(f"⚠️ Fast transcription error: {e}")
                return "[Transcription failed]"
        else:
            return "[SpeechRecognition not available]"
        
    except subprocess.TimeoutExpired:
        print("⚠️ FFmpeg timeout - audio too long")
        return "[Audio too long - please keep responses under 30 seconds]"
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        return None
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)

def get_gemini_response_fast(user_message):
    """OPTIMIZED: Get response from Gemini AI using persistent chat session"""
    global chat_session
    
    try:
        if chat_session:
            # Add context for strict interviewing based on conversation stage
            conversation_length = len(conversation_history)
            
            # Add coaching prompts based on interview progression
            enhanced_message = user_message
            
            if conversation_length <= 4:  # Early stage - establish competency
                enhanced_message += "\n\n[INTERVIEWER NOTE: This is early stage. Probe for technical depth and ask for specific examples. Challenge surface-level answers.]"
            elif conversation_length <= 8:  # Mid stage - dive deep into problem-solving
                enhanced_message += "\n\n[INTERVIEWER NOTE: Mid-stage interview. Ask challenging 'what-if' scenarios. Test edge cases and system design thinking.]"
            else:  # Late stage - cultural fit and advanced topics
                enhanced_message += "\n\n[INTERVIEWER NOTE: Advanced stage. Ask about leadership, mentoring, or complex architectural decisions. Be more demanding.]"
            
            # Use existing chat session for faster responses
            response = chat_session.send_message(enhanced_message)
            result = response.text.strip()
            
            # Ensure response maintains strict interviewer tone
            if len(result) > 350:
                result = result[:350] + "..."
            
            print(f"✓ Strict interviewer response: {result[:50]}...")
            return result
        else:
            # Fallback to original method
            return get_gemini_response(user_message)
            
    except Exception as e:
        print(f"Fast Gemini error: {e}")
        # Fallback to original method
        return get_gemini_response(user_message)

def text_to_speech_fast(text):
    """OPTIMIZED: Convert text to speech with optimizations for speed"""
    
    # OPTIMIZATION: Limit text length for faster TTS
    if len(text) > 200:
        text = text[:200] + "..."
    
    # Try ElevenLabs first with optimized settings
    if not USE_GTTS_FALLBACK and ELEVENLABS_API_KEY:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            
            # OPTIMIZED: Faster ElevenLabs settings
            data = {
                "text": text,
                "model_id": "eleven_turbo_v2",  # Fastest model
                "voice_settings": {
                    "stability": 0.4,           # Slightly higher for speed
                    "similarity_boost": 0.6,    # Lower for faster processing
                    "style": 0.2,               # Reduced style for speed
                    "use_speaker_boost": False  # Disable for speed
                },
                "optimize_streaming_latency": 4  # Maximum optimization
            }
            
            # OPTIMIZATION: Shorter timeout for faster failure detection
            response = requests.post(url, json=data, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"✓ Fast ElevenLabs TTS completed")
                return response.content
            else:
                print(f"⚠️ ElevenLabs error: {response.status_code} - falling back to gTTS")
        except Exception as e:
            print(f"⚠️ Fast ElevenLabs error: {e} - falling back to gTTS")
    
    # OPTIMIZED gTTS fallback
    if GTTS_AVAILABLE:
        try:
            # OPTIMIZATION: Shorter text and minimal settings for speed
            tts = gTTS(text=text, lang='en', slow=False, tld='com')
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            audio_data = audio_buffer.read()
            
            # OPTIMIZATION: Skip speed adjustment for faster response
            # If speed adjustment is needed, use simpler processing
            if VOICE_SPEED != 1.0:
                try:
                    audio_data = speed_up_audio_fast(audio_data, speed=VOICE_SPEED)
                except Exception as e:
                    print(f"⚠️ Skipping speed adjustment for faster response: {e}")
            
            print(f"✓ Fast gTTS completed")
            return audio_data
            
        except Exception as e:
            print(f"❌ Fast gTTS error: {e}")
            return None
    else:
        print("❌ No TTS service available")
        return None

def speed_up_audio_fast(audio_data, speed=1.15):
    """OPTIMIZED: Speed up audio with minimal processing"""
    try:
        # Save input audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_input:
            temp_input.write(audio_data)
            temp_input_path = temp_input.name
        
        # Create output temp file
        temp_output_path = temp_input_path.replace('.mp3', '_fast.mp3')
        
        # OPTIMIZATION: Faster FFmpeg processing with reduced quality
        subprocess.run([
            FFMPEG_PATH,
            '-i', temp_input_path,
            '-filter:a', f'atempo={speed}',
            '-b:a', '64k',  # Lower bitrate for speed
            '-vn',
            temp_output_path,
            '-y'
        ], check=True, stderr=subprocess.DEVNULL, timeout=2)  # 2 second timeout
        
        # Read the sped-up audio
        with open(temp_output_path, 'rb') as f:
            fast_audio = f.read()
        
        # Cleanup
        os.unlink(temp_input_path)
        os.unlink(temp_output_path)
        
        return fast_audio
        
    except Exception as e:
        print(f"Fast speed adjustment failed: {e}")
        return audio_data  # Return original if speed adjustment fails
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
    """Get response from Gemini AI (fallback method)"""
    try:
        # Create context for strict interviewing
        context = """You are Talkito, a senior technical recruiter at ElevenLabs with 8+ years of experience. 
        You conduct STRICT, PROFESSIONAL interviews with high standards. 
        
        INTERVIEW STYLE:
        - Ask in-depth, challenging questions that test real understanding
        - Don't accept vague answers - always probe deeper
        - Use follow-ups like: "Can you be more specific?", "Walk me through the exact implementation", "What challenges did you face?"
        - Challenge the candidate respectfully but firmly
        - Focus on technical depth, problem-solving, and real-world scenarios
        
        Keep responses professional but demanding. Always end with ONE specific, challenging follow-up question."""
        
        # Build conversation context with stricter tone
        full_prompt = f"{context}\n\nInterview Conversation:\n"
        for msg in conversation_history[-6:]:  # Last 3 exchanges
            role = "Talkito (Interviewer)" if msg['role'] == 'assistant' else "Candidate"
            full_prompt += f"{role}: {msg['content']}\n"
        
        full_prompt += f"\nCandidate: {user_message}\nTalkito (Interviewer):"
        
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
    
    if FFMPEG_PATH and os.path.exists(FFMPEG_PATH):
        print(f"✓ FFmpeg: Found at {os.path.dirname(FFMPEG_PATH)}")
    else:
        print("❌ FFmpeg: NOT FOUND")
        print("   Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
        print("   Extract to project root folder")
    
    print("="*50)
    print("Server starting on http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
