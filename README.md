# 🎤 Voice to Voice Chat Applications

A collection of optimized Streamlit applications for real-time voice-to-voice conversations with AI using OpenAI's GPT-4 Audio Preview and VoiceVox TTS.

## 🚀 Features

- **Real-time voice recording** via Streamlit's audio input
- **AI conversation** using OpenAI's GPT-4 Audio Preview model
- **Text-to-Speech synthesis** using VoiceVox TTS Quest V3 API
- **Automatic audio playback** with browser autoplay
- **Chat context management** for conversation continuity
- **Performance optimizations** for minimal latency

## 📦 Applications

### 1. 🎤 Basic Voice Chat (`voice_chat_app.py`)
- Standard implementation with core features
- Sequential processing pipeline
- Good for learning and basic use cases

### 2. ⚡ Optimized Voice Chat (`voice_chat_optimized.py`)
- Enhanced performance with concurrent processing
- Reduced UI refresh overhead
- Performance timing metrics
- Better error handling

### 3. 🚀 Ultra-Fast Voice Chat (`voice_chat_ultra_optimized.py`)
- Maximum performance optimization
- No temporary files (direct byte processing)
- Concurrent AI inference and TTS synthesis
- Real-time performance analytics
- Enhanced UI with CSS styling

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

## 📊 Performance Metrics

The optimized versions track performance metrics:
- **Audio Conversion Time**: Time to process audio input
- **AI Inference Time**: Time for OpenAI API response
- **TTS Synthesis Time**: Time to generate speech audio
- **Total Response Time**: End-to-end processing time

## 🎨 UI Features

### Ultra-Fast Version Features
- **Real-time dashboard**: Shows conversation count, status, and average response time
- **Performance analytics**: Detailed timing breakdowns
- **Enhanced audio player**: Better autoplay handling and fallbacks
- **Styled chat bubbles**: Improved visual conversation display
- **Direct audio links**: Manual playback options if autoplay fails

## 🔍 Technical Details

### Audio Processing
- **Input Format**: WAV (from Streamlit audio input)
- **Base64 Encoding**: For OpenAI API compatibility
- **Direct Processing**: No temporary files in optimized versions

### AI Model
- **Model**: GPT-4 Audio Preview (`gpt-4o-audio-preview`)
- **Modalities**: Text output
- **Context**: Maintains conversation history

### TTS Service
- **Service**: VoiceVox via TTS Quest V3 API
- **Output**: MP3 streaming URLs
- **Speaker**: Japanese voice (configurable speaker ID)

## 🚨 Troubleshooting

### Audio Autoplay Issues
- **Enable autoplay** in your browser settings
- **Use Chrome or Edge** for better audio support
- **Check browser console** for autoplay prevention messages
- **Manual playback**: Use the direct audio links if autoplay fails

### Performance Issues
- **Check internet connection** for stable API calls
- **Monitor performance metrics** in the optimized versions
- **Clear chat history** if context becomes too large
- **Restart the app** if experiencing memory issues

### API Issues
- **Verify OpenAI API key** is valid and has audio model access
- **Check TTS API key** for VoiceVox service
- **Monitor API rate limits** and quotas

## 🤝 Contributing

Feel free to contribute improvements:
- Performance optimizations
- UI/UX enhancements  
- Additional TTS services
- Error handling improvements
- Documentation updates

## 📝 License

This project is for educational and personal use. Please ensure you comply with:
- OpenAI API Terms of Service
- VoiceVox TTS Quest API Terms
- Streamlit usage guidelines

## 🔗 Dependencies

- **streamlit**: Web app framework
- **openai**: OpenAI API client
- **requests**: HTTP requests for TTS API
- **hashlib**: Audio deduplication (built-in)
- **concurrent.futures**: Concurrent processing (built-in)

---

🎤 **Happy voice chatting!** 🚀 