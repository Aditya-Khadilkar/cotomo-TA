

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key** (if not using the default one in the code)

## 🎯 Usage

### Option 1: Use the Launcher (Recommended)
```bash
python run_voice_chat.py
```
This will show you a menu to choose between the different app versions.

### Option 2: Run Individual Apps
```bash
# Basic version
streamlit run voice_chat_app.py

# Optimized version  
streamlit run voice_chat_optimized.py

# Ultra-fast version
streamlit run voice_chat_ultra_optimized.py
```

## 🔧 How It Works

### Workflow
1. **Record Audio**: Click the microphone button to record your voice
2. **Audio Processing**: Convert audio to base64 format for OpenAI API
3. **AI Inference**: Send audio to GPT-4 Audio Preview for response
4. **TTS Synthesis**: Convert AI text response to speech using VoiceVox
5. **Auto-play**: Stream and play the AI's voice response automatically
6. **Context Management**: Store conversation history for continuity

### Performance Optimizations
- **Direct byte processing**: No temporary files in ultra-optimized version
- **Concurrent execution**: AI inference and TTS run in parallel where possible
- **Session caching**: Reuse audio processor and TTS service instances
- **UI optimization**: Minimal refreshes and efficient state management
- **Performance tracking**: Real-time latency monitoring

## ⚙️ Configuration

### Character Configuration
The AI character is configured in `audio_processor.py` and `optimized_audio_processor.py`:
```python
character_desc = "Aya is a Japanese girl, she is bold and confident, she is a student and likes to tease others"
```

### TTS Configuration
VoiceVox TTS settings in the apps:
```python
TtsQuestV3Voicevox(
    speaker_id=1,  # ずんだもん（あまあま）
    tts_quest_api_key='your-api-key'
)
```
