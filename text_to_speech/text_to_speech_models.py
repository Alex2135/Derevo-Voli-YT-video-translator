import os
from abc import ABC

from ukrainian_tts.tts import TTS, Voices, Stress


class TtsModel(ABC):
    tts_voices: dict[str, any] = {}
    
    def run_tts(self, ukrainian_stressified_text: str, voice: str) -> str:
        pass
    

class UkrainianTtsEspnet:
    tts_voices: dict[str, any] = {
        "Tetiana": Voices.Tetiana.value,
        "Mykyta": Voices.Mykyta.value,
        "Lada": Voices.Lada.value,
        "Dmytro": Voices.Dmytro.value,
        "Oleksa": Voices.Oleksa.value,
    }
    
    def run_tts(self, ukrainian_stressified_text: str, voice: str) -> str:
        tts = TTS(device="cpu")  # can try gpu, mps
        if not os.path.exists("/tmp/audio"):
            os.mkdir("/tmp/audio")
        with open("/tmp/audio/test.wav", mode="wb") as file:
            _, output_text = tts.tts(
                ukrainian_stressified_text, 
                self.tts_voices[voice], 
                Stress.Dictionary.value, 
                file
            )
        return "/tmp/audio/test.wav"