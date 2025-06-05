import streamlit as st
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from optimized_audio_processor import OptimizedAudioProcessor  
from tts_voicevox import TtsQuestV3Voicevox
import hashlib

# Configure page for minimal design
st.set_page_config(
    # page_title="Voice Chat",
    # page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimal design with green background
st.markdown("""
<style>
    .main {
        background-color: #F0F5F0;
    }
    
    .stApp {
        background-color: #F0F5F0;
    }
    
    .main-container {
        background-color: #F0F5F0;
        padding: 20px;
        border-radius: 15px;
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .processing-indicator {
        background: linear-gradient(90deg, #4CAF50, #81C784);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        animation: pulse 1.5s infinite;
        margin: 20px 0;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .audio-response {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid #4CAF50;
        box-shadow: 0 2px 10px rgba(76, 175, 80, 0.1);
    }
    
    .chat-history {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }
    
    .user-message {
        background: #E8F5E8;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 5px 0;
        font-size: 0.9em;
    }
    
    .ai-message {
        background: #F5F5F5;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 5px 0;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services (cached for performance)
@st.cache_resource
def get_audio_processor():
    return OptimizedAudioProcessor()

@st.cache_resource  
def get_tts_service():
    return TtsQuestV3Voicevox(speaker_id=59, tts_quest_api_key='e848r8298352275')

@st.cache_resource
def get_thread_executor():
    return ThreadPoolExecutor(max_workers=3)

# Initialize services
audio_processor = get_audio_processor()
tts_service = get_tts_service()
executor = get_thread_executor()

# Session state initialization
if 'chat_context' not in st.session_state:
    st.session_state.chat_context = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'last_audio_hash' not in st.session_state:
    st.session_state.last_audio_hash = None
if 'latest_audio_url' not in st.session_state:
    st.session_state.latest_audio_url = None
if 'latest_ai_response' not in st.session_state:
    st.session_state.latest_ai_response = None

def get_audio_hash(audio_bytes):
    """Generate hash for audio deduplication"""
    return hashlib.md5(audio_bytes).hexdigest()

def process_ai_inference(messages):
    """Process OpenAI inference in thread"""
    return audio_processor.infer(messages)

def process_tts_generation(text):
    """Process TTS synthesis in thread"""
    return tts_service.synthesize_speech(text)

def create_audio_player(mp3_url, ai_response):
    """Create immediate streaming audio player"""
    audio_id = f"streaming_audio_{int(time.time() * 1000)}"
    
    return f"""
    <div class="audio-response">
        <div style="margin-bottom: 15px;">
            <strong>AI:</strong> {ai_response}
        </div>
        <audio id="{audio_id}" controls autoplay preload="auto" style="width: 100%;">
            <source src="{mp3_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>
    <script>
        (function() {{
            const audio = document.getElementById('{audio_id}');
            if (audio) {{
                audio.volume = 0.9;
                
                // Try to play immediately
                const playPromise = audio.play();
                
                if (playPromise !== undefined) {{
                    playPromise.then(() => {{
                        console.log('🔊 Audio started playing automatically');
                        audio.style.border = '2px solid #4CAF50';
                    }}).catch(error => {{
                        console.log('⚠️ Autoplay prevented by browser:', error);
                        audio.style.border = '2px solid #FF9800';
                        
                        // Add click listener to start on user interaction
                        document.addEventListener('click', function() {{
                            audio.play().then(() => {{
                                console.log('🔊 Audio started after user interaction');
                                audio.style.border = '2px solid #4CAF50';
                            }});
                        }}, {{ once: true }});
                    }});
                }}
                
                // Show loading state
                audio.addEventListener('loadstart', function() {{
                    console.log('🔄 Audio loading started');
                }});
                
                audio.addEventListener('canplay', function() {{
                    console.log('✅ Audio ready to play');
                }});
                
                audio.addEventListener('error', function(e) {{
                    console.error('❌ Audio error:', e);
                    audio.style.border = '2px solid #f44336';
                }});
            }}
        }})();
    </script>
    """

def process_voice_message(audio_bytes):
    """Process voice message and generate response"""
    try:
        # Convert audio and add to context
        user_audio_unit = audio_processor.user_audio_unit_from_bytes(audio_bytes, "wav")
        st.session_state.chat_context.append(user_audio_unit)
        
        # Prepare messages and get AI response
        messages = audio_processor.get_messages(st.session_state.chat_context)
        ai_future = executor.submit(process_ai_inference, messages)
        ai_response = ai_future.result()
        
        # Add AI response to context
        ai_chat_unit = {"role": "assistant", "content": ai_response}
        st.session_state.chat_context.append(ai_chat_unit)
        
        # Store the latest AI response for immediate display
        st.session_state.latest_ai_response = ai_response
        
        # Generate TTS
        tts_future = executor.submit(process_tts_generation, ai_response)
        mp3_url = tts_future.result()
        
        # Store the latest audio URL for immediate streaming
        st.session_state.latest_audio_url = mp3_url
        
        return ai_response, mp3_url
        
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")
        return None, None

# Main UI
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Company logo
st.markdown("""
<div class="logo-container">
    <img src="https://storage.googleapis.com/studio-design-asset-files/projects/9YWyz0PXOM/s-425x96_webp_357a7abf-eccc-4142-b7d3-f4574577e50a.webp" 
         style="max-width: 300px; height: auto;" alt="Company Logo">
</div>
""", unsafe_allow_html=True)

# Title
st.markdown("<h2 style='text-align: center; color: #2E7D32; margin-bottom: 30px;'>Demo</h2>", unsafe_allow_html=True)

# Voice input section
st.markdown("### Record Your Message")
audio_data = st.audio_input("Click to record:", key="voice_input")

# Process audio when available
if audio_data is not None:
    audio_bytes = audio_data.read()
    current_hash = get_audio_hash(audio_bytes)
    
    if current_hash != st.session_state.last_audio_hash and not st.session_state.processing:
        st.session_state.last_audio_hash = current_hash
        st.session_state.processing = True
        
        # Show processing indicator
        processing_placeholder = st.empty()
        processing_placeholder.markdown(
            '<div class="processing-indicator">🎤 Processing your message...</div>', 
            unsafe_allow_html=True
        )
        
        # Process the voice message
        ai_response, mp3_url = process_voice_message(audio_bytes)
        
        # Clear processing indicator
        processing_placeholder.empty()
        
        # Show response immediately
        if ai_response and mp3_url:
            st.success("✅ Response ready!")
            
            # Create placeholders for immediate response display
            audio_placeholder = st.empty()
            
            # IMMEDIATE AUDIO STREAMING
            st.markdown("### 🔊 AI Response - Playing Now!")
            audio_html = create_audio_player(mp3_url, ai_response)
            audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
        
        st.session_state.processing = False
        
        # Small delay to ensure audio starts, then refresh to update chat history
        time.sleep(1.0)
        st.rerun()

# Show latest audio if available (for persistence across reruns)
if st.session_state.latest_audio_url and st.session_state.latest_ai_response and not st.session_state.processing:
    st.markdown("### 🎵 Latest AI Response")
    latest_audio_html = create_audio_player(
        st.session_state.latest_audio_url, 
        st.session_state.latest_ai_response
    )
    st.markdown(latest_audio_html, unsafe_allow_html=True)

# Chat history (minimized/collapsible)
if st.session_state.chat_context:
    with st.expander("💬 Conversation History", expanded=False):
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        
        # Show recent exchanges
        recent_context = st.session_state.chat_context[-6:]  # Last 6 messages
        
        for unit in recent_context:
            if unit["role"] == "user":
                st.markdown('<div class="user-message">🎤 You: [Voice message]</div>', unsafe_allow_html=True)
            elif unit["role"] == "assistant":
                st.markdown(f'<div class="ai-message">🤖 AI: {unit["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear button
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.chat_context = []
            st.session_state.last_audio_hash = None
            st.session_state.latest_audio_url = None
            st.session_state.latest_ai_response = None
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Simple footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.8em;'>Voice Chat Application by Aditya Khadilkar</div>", 
    unsafe_allow_html=True
) 