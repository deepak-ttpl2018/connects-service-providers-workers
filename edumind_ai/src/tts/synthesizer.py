"""
Text-to-Speech synthesis functionality.
"""
import logging
import os
from gtts import gTTS
from typing import Optional

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Provides text-to-speech functionality."""
    
    def __init__(self, cache_dir: str = "speech_cache"):
        """
        Initialize the TTS engine.
        
        Args:
            cache_dir: Directory to cache generated speech files
        """
        logger.info("Initializing Text-to-Speech engine")
        self.cache_dir = cache_dir
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def synthesize(self, text: str, output_file: Optional[str] = None, language: str = 'en') -> str:
        """
        Convert text to speech and save to an audio file.
        
        Args:
            text: Text to convert to speech
            output_file: Path to save the audio file (if None, generates a temporary file)
            language: Language code (default: 'en' for English)
            
        Returns:
            Path to the generated audio file
        """
        logger.info(f"Synthesizing speech for text of length {len(text)}")
        
        # Generate a filename if not provided
        if output_file is None:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            output_file = os.path.join(self.cache_dir, f"{text_hash}.mp3")
        
        # Check if we already have this text cached
        if os.path.exists(output_file):
            logger.info(f"Using cached speech file: {output_file}")
            return output_file
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_file)
        
        logger.info(f"Saved speech to: {output_file}")
        return output_file
    
    def synthesize_chunks(self, chunks: list[str], prefix: str = "chunk") -> list[str]:
        """
        Convert multiple text chunks to speech.
        
        Args:
            chunks: List of text chunks to convert
            prefix: Prefix for the output files
            
        Returns:
            List of paths to the generated audio files
        """
        logger.info(f"Synthesizing speech for {len(chunks)} chunks")
        
        output_files = []
        for i, chunk in enumerate(chunks):
            output_file = os.path.join(self.cache_dir, f"{prefix}_{i}.mp3")
            output_files.append(self.synthesize(chunk, output_file))
        
        return output_files
