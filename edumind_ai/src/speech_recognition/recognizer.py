"""
Speech recognition functionality.
"""
import logging
import speech_recognition as sr
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SpeechRecognizer:
    """Handles speech recognition for student questions."""
    
    def __init__(self):
        """Initialize the speech recognizer."""
        logger.info("Initializing Speech Recognizer")
        self.recognizer = sr.Recognizer()
    
    def recognize_from_microphone(self, timeout: int = 5) -> Dict[str, Any]:
        """
        Recognize speech from the microphone.
        
        Args:
            timeout: Maximum number of seconds to listen for
            
        Returns:
            Dictionary containing the recognized text and metadata
        """
        logger.info(f"Listening for speech (timeout: {timeout}s)")
        
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                
                # Listen for audio
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
                # Recognize speech using Google Speech Recognition
                logger.info("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                
                logger.info(f"Recognized: {text}")
                return {
                    "success": True,
                    "text": text,
                    "confidence": 0.9  # Placeholder confidence score
                }
                
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out")
            return {
                "success": False,
                "error": "timeout",
                "message": "Listening timed out. No speech detected."
            }
            
        except sr.UnknownValueError:
            logger.warning("Speech not understood")
            return {
                "success": False,
                "error": "not_understood",
                "message": "Sorry, I could not understand what you said."
            }
            
        except sr.RequestError as e:
            logger.error(f"Error with speech recognition service: {e}")
            return {
                "success": False,
                "error": "service_error",
                "message": f"Speech recognition service error: {e}"
            }
            
        except Exception as e:
            logger.error(f"Unexpected error during speech recognition: {e}")
            return {
                "success": False,
                "error": "unknown",
                "message": f"Unexpected error: {e}"
            }
    
    def recognize_from_file(self, audio_file: str) -> Dict[str, Any]:
        """
        Recognize speech from an audio file.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Dictionary containing the recognized text and metadata
        """
        logger.info(f"Recognizing speech from file: {audio_file}")
        
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                
                logger.info(f"Recognized: {text}")
                return {
                    "success": True,
                    "text": text,
                    "confidence": 0.9  # Placeholder confidence score
                }
                
        except Exception as e:
            logger.error(f"Error recognizing speech from file: {e}")
            return {
                "success": False,
                "error": "file_error",
                "message": f"Error recognizing speech from file: {e}"
            }
