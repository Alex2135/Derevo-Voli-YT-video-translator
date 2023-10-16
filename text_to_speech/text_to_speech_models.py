import os
from abc import ABC

import torch
from ukrainian_tts.tts import TTS, Voices, Stress


class TtsModel(ABC):
    tts_voices: dict = {}
    
    def run_tts(self, ukrainian_stressified_text: str, voice: str) -> str:
        pass
    

class UkrainianTtsEspnet:
    tts_voices: dict = {
        "Tetiana": Voices.Tetiana.value,
        "Mykyta": Voices.Mykyta.value,
        "Lada": Voices.Lada.value,
        "Dmytro": Voices.Dmytro.value,
        "Oleksa": Voices.Oleksa.value,
    }
    
    def __init__(self) -> None:
        device = "gpu" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(device=device)  # can try gpu, mps
    
    def run_tts(self, ukrainian_stressified_text: str, voice: str) -> str:
        if not os.path.exists("/tmp/audio"):
            os.mkdir("/tmp/audio")
        with open("/tmp/audio/test.wav", mode="wb") as file:
            _, output_text = self.tts.tts(
                ukrainian_stressified_text, 
                self.tts_voices[voice], 
                Stress.Dictionary.value, 
                file
            )
        return "/tmp/audio/test.wav"
    
