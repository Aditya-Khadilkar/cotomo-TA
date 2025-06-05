import requests
import time
import subprocess
import sys
from urllib.parse import urlencode

class TtsQuestV3Voicevox:
    def __init__(self, speaker_id=1, tts_quest_api_key=''):
        """
        Initialize TTS Quest V3 Voicevox client
        
        Args:
            speaker_id (int): Speaker ID (default: 1 for ずんだもん（あまあま）)
            tts_quest_api_key (str): Optional API key for better performance
        """
        self.api_url = 'https://api.tts.quest/v3/voicevox/synthesis'
        self.speaker_id = speaker_id
        self.api_key = tts_quest_api_key
    
    def synthesize_speech(self, text):
        """
        Synthesize speech from text and return the MP3 streaming URL
        
        Args:
            text (str): Text to synthesize
            
        Returns:
            str: MP3 streaming URL
        """
        params = {
            'speaker': self.speaker_id,
            'text': text
        }
        
        if self.api_key:
            params['key'] = self.api_key
        
        return self._make_request(params)
    
    def _make_request(self, params):
        """
        Make request to TTS API with retry logic
        
        Args:
            params (dict): Request parameters
            
        Returns:
            str: MP3 streaming URL
        """
        query_string = urlencode(params)
        url = f"{self.api_url}?{query_string}"
        
        while True:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                if 'retryAfter' in data:
                    retry_after = data['retryAfter']
                    print(f"Rate limited. Waiting {retry_after + 1} seconds...")
                    time.sleep(1 + retry_after)
                    continue
                    
                elif 'mp3StreamingUrl' in data:
                    return data['mp3StreamingUrl']
                    
                elif 'errorMessage' in data:
                    raise Exception(f"API Error: {data['errorMessage']}")
                    
                else:
                    raise Exception("Server Error: Unexpected response format")
                    
            except requests.exceptions.RequestException as e:
                raise Exception(f"Request failed: {e}")
    
    def download_audio(self, text, filename='output.mp3'):
        """
        Download synthesized audio to a file
        
        Args:
            text (str): Text to synthesize
            filename (str): Output filename
            
        Returns:
            str: Path to downloaded file
        """
        mp3_url = self.synthesize_speech(text)
        
        print(f"Downloading audio from: {mp3_url}")
        response = requests.get(mp3_url)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"Audio saved as: {filename}")
        return filename
    
    def play_audio(self, text):
        """
        Synthesize and play audio directly (requires system audio player)
        
        Args:
            text (str): Text to synthesize
        """
        mp3_url = self.synthesize_speech(text)
        print(f"Playing audio from: {mp3_url}")
        
        # Try different system audio players
        players = ['afplay', 'mpg123', 'ffplay', 'vlc']  # macOS, Linux options
        
        for player in players:
            try:
                subprocess.run([player, mp3_url], check=True, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("No suitable audio player found. Downloading file instead...")
        self.download_audio(text)

def main():
    """
    Example usage of TTS Quest V3 Voicevox
    """
    # Initialize TTS client
    tts = TtsQuestV3Voicevox(
        speaker_id=1,  # ずんだもん（あまあま）
        tts_quest_api_key='e848r8298352275'  # Add your API key here if you have one
    )
    
    # Example usage
    text = "こんにちは、これはテストです。"
    
    print("TTS Quest V3 Voicevox - Python Client")
    print("=====================================")
    
    try:
        # Option 1: Get streaming URL only
        print(f"Synthesizing: {text}")
        mp3_url = tts.synthesize_speech(text)
        print(f"MP3 Streaming URL: {mp3_url}")
        
        # Option 2: Download to file
        print("\nDownloading audio file...")
        filename = tts.download_audio(text, 'test_output.mp3')
        
        # Option 3: Try to play directly (works on macOS with afplay)
        print("\nAttempting to play audio...")
        tts.play_audio(text)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 