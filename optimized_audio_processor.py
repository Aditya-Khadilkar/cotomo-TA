import base64
import io
from openai import OpenAI
import re
import streamlit as st


class OptimizedAudioProcessor:
    def __init__(self, api_key=None, character_desc=None):
        """
        Initialize the OptimizedAudioProcessor with OpenAI client and character description.
        
        Args:
            api_key (str): OpenAI API key. If None, uses the default key.
            character_desc (str): Character description for response generation.
        """
        default_api_key = st.secrets["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=api_key or default_api_key)
        
        self.character_desc = character_desc or """Aya is a Japanese girl, she is bold and confident, she is a student and likes to tease others"""
        
        self.response_format = """Respond with Aya's response in japanese. Stricly only respond with Aya's line and nothing else."""

        self.system_prompt = f"""Generate a appropriate response for the audio in this charachter style: {self.character_desc}

Response format: 
{self.response_format}"""
    
    def user_audio_unit_from_bytes(self, audio_bytes, format="wav"):
        """
        Convert audio bytes directly to base64 encoded chat unit.
        This avoids the need for temporary files and improves latency.
        
        Args:
            audio_bytes (bytes): Raw audio data bytes.
            format (str): Audio format (wav, mp3, etc.)
            
        Returns:
            dict: Chat unit formatted for OpenAI API.
        """
        # Convert audio bytes to base64
        encoded_string = base64.b64encode(audio_bytes).decode('utf-8')

        chat_unit = {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_string,
                        "format": format.lower()
                    }
                }
            ]
        }
        return chat_unit
    
    def user_audio_unit(self, audio_file_path):
        """
        Convert audio file to base64 encoded string.
        Kept for backward compatibility.
        
        Args:
            audio_file_path (str): Path to the audio file.
            
        Returns:
            dict: Chat unit formatted for OpenAI API.
        """
        with open(audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        
        # Determine format from file extension
        format = "mp3" if audio_file_path.lower().endswith('.mp3') else "wav"
        
        return self.user_audio_unit_from_bytes(audio_bytes, format)
    
    def get_messages(self, chat_context):
        """
        Prepare messages for OpenAI API call.
        
        Args:
            chat_context (list): List of chat units.
            
        Returns:
            list: Formatted messages for OpenAI API.
        """
        messages = [
            {
                "role": "developer",
                "content": self.system_prompt
            },
        ]
        
        if chat_context:
            messages.extend(chat_context)
        return messages
    
    def infer(self, messages):
        """
        Generate response for the audio using OpenAI API.
        
        Args:
            messages (list): Formatted messages for OpenAI API.
            
        Returns:
            str: AI generated response content.
        """
        completion = self.client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text"],
            messages=messages
        )
        return completion.choices[0].message.content
    
    async def infer_async(self, messages):
        """
        Async version of inference for better concurrent processing.
        
        Args:
            messages (list): Formatted messages for OpenAI API.
            
        Returns:
            str: AI generated response content.
        """
        # Note: OpenAI Python client doesn't support async for audio yet
        # This is a placeholder for future async implementation
        return self.infer(messages)


# Example usage:
if __name__ == "__main__":
    processor = OptimizedAudioProcessor()
    import time

    # Test with bytes directly
    with open("input_audio.mp3", "rb") as f:
        audio_bytes = f.read()
    
    start_time = time.time()
    
    # Using optimized bytes method
    input_audio_unit = processor.user_audio_unit_from_bytes(audio_bytes, "mp3")
    messages = processor.get_messages([input_audio_unit])
    response = processor.infer(messages)
    
    end_time = time.time()
    
    print(f"Response: {response}")
    print(f"Total processing time: {end_time - start_time:.2f} seconds") 
