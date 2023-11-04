from enum import Enum

import whisper


class WhisperModels(Enum):
    BASE = "base"
    MEDIUM = "medium"
    LARGE = "large"


class WhisperTranslator:
    def __init__(self, model_size: WhisperModels):
        self.model = whisper.load_model(model_size.value)
        self.language = "English"
        
    def get_text_from_speech(self, audio_file_path: str) -> str:
        # Load the audio file for transcription
        audio_data = whisper.load_audio(audio_file_path)

        # Transcribe the speech from the audio file
        transcription = self.model.transcribe(audio=audio_data, language=self.language)

        return transcription["text"]
    