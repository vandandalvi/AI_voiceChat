# 🎙️ Voice Customization Guide

Your AI interviewer voice has been upgraded! The voice is now **15% faster** and uses a **more natural US accent**.

## Current Settings

Your `.env` file now has these voice controls:

```env
USE_GTTS_FALLBACK=true          # Use free Google TTS
VOICE_SPEED=1.15                # 15% faster than normal
GTTS_TLD=com                    # US English accent
```

---

## 🎚️ Adjust Voice Speed

Change `VOICE_SPEED` in `backend\.env`:

| Speed | Value | Description |
|-------|-------|-------------|
| **Normal** | `1.0` | Original gTTS speed (slower) |
| **Natural** | `1.15` | ✅ **Current** - Natural conversation pace |
| **Quick** | `1.25` | Fast-paced, energetic |
| **Very Fast** | `1.35` | Very quick (may sound rushed) |
| **Slower** | `0.9` | Slower, more deliberate |

**Example:**
```env
VOICE_SPEED=1.25  # For faster, more energetic voice
```

---

## 🌍 Change Accent

Change `GTTS_TLD` in `backend\.env`:

| Accent | Value | Description |
|--------|-------|-------------|
| **US English** | `com` | ✅ **Current** - Most natural |
| **British** | `co.uk` | British accent |
| **Australian** | `com.au` | Australian accent |
| **Indian** | `co.in` | Indian English accent |
| **Canadian** | `ca` | Canadian accent |
| **Irish** | `ie` | Irish accent |

**Example:**
```env
GTTS_TLD=co.uk  # For British accent
```

---

## 🎭 Voice Personality Combinations

### Professional & Clear
```env
VOICE_SPEED=1.10
GTTS_TLD=com
```

### Energetic & Fast
```env
VOICE_SPEED=1.30
GTTS_TLD=com
```

### British & Sophisticated
```env
VOICE_SPEED=1.15
GTTS_TLD=co.uk
```

### Friendly & Relaxed
```env
VOICE_SPEED=1.05
GTTS_TLD=com.au
```

---

## 🔄 How to Apply Changes

1. **Edit** `backend\.env` file
2. **Change** `VOICE_SPEED` or `GTTS_TLD` values
3. **Save** the file
4. **Restart** the backend server:
   ```powershell
   Get-Process python | Stop-Process -Force
   python c:\projects\talkitoP1\backend\app.py
   ```

The Flask server will auto-restart when you save `.env` in some cases, but manual restart is more reliable.

---

## 🎯 Recommended Settings

### For Interviews (Current)
```env
VOICE_SPEED=1.15
GTTS_TLD=com
```
**Why:** Natural pace, clear US accent

### For Quick Demos
```env
VOICE_SPEED=1.30
GTTS_TLD=com
```
**Why:** Fast-paced, keeps energy high

### For International Audience
```env
VOICE_SPEED=1.10
GTTS_TLD=com
```
**Why:** Slightly slower for clarity

---

## ⚡ Pro Tips

1. **Test different speeds**: Everyone perceives speed differently
2. **Match your pace**: If you speak fast, use 1.25-1.35x
3. **Background noise**: Slower speeds (1.0-1.1) are clearer in noisy environments
4. **Long conversations**: Faster speeds prevent monotony
5. **Non-native speakers**: Use 1.0-1.1 for better comprehension

---

## 🔍 Troubleshooting

### Voice sounds choppy
- **Solution**: Lower VOICE_SPEED to 1.10 or 1.05
- FFmpeg might be having trouble with higher speeds

### Voice sounds too robotic
- **Solution**: This is a limitation of free gTTS
- For more natural voice, consider:
  - Getting a new ElevenLabs account
  - Using OpenAI TTS (paid)
  - Using Azure Speech Services

### Changes not applying
- **Solution**: 
  1. Stop Python completely: `Get-Process python | Stop-Process -Force`
  2. Wait 2 seconds
  3. Restart: `python c:\projects\talkitoP1\backend\app.py`

### Want even more control?
Edit `backend\app.py` directly:
- Line ~35: Voice configuration
- Line ~221: `speed_up_audio()` function
- Line ~264: gTTS settings

---

## 🆙 Upgrade to Better Voice (Optional)

If you want truly human-like voice:

### Option 1: ElevenLabs (Paid)
- Get a new account or paid plan
- Set `USE_GTTS_FALLBACK=false` in `.env`
- Cost: $5-22/month

### Option 2: OpenAI TTS
- Very natural voice
- Install: `pip install openai`
- Cost: $15 per 1M characters

### Option 3: Azure Speech
- Microsoft's TTS
- Multiple voices
- Cost: Free tier available

---

## 📝 Current Configuration

Check your settings:
```powershell
cd c:\projects\talkitoP1\backend
Get-Content .env | Select-String "VOICE_SPEED|GTTS_TLD"
```

---

**Your current voice is already improved! Test it now:**
1. Go to http://localhost:5173
2. Click "Start Interview"
3. Listen to the faster, more natural voice!

Want different? Just edit `.env` and restart! 🎙️✨
