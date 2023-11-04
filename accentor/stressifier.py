import os
import textwrap
from abc import ABC

import ukrainian_accentor as accentor
from ukrainian_word_stress import Stressifier, StressSymbol, OnAmbiguity


DEFAULT_UNSTRESSED_TEXT = """Привіт. Це перевірка можливих неправильних наголосів:
«Десь чув, що той фраєр привіз їхньому царю грильяж та класну шубу з пір'я ґави.» .
«Жебракують філософи при ґанку церкви в Гадячі, ще й шатро їхнє п'яне знаємо.».
«Протягом цієї п'ятирічки в ґрунт було висаджено гарбуз, шпинат та цілющий фенхель.»."""


class StressifierModel(ABC):
    def __init__(self):
        self.init_model()
    
    def init_model(self):
        pass
    
    def stressify(self, text: str) -> str:
        pass
    

class UkrainianWordStressifierModel(StressifierModel):
    def init_model(self):
        self.model = Stressifier(stress_symbol="+", on_ambiguity=OnAmbiguity.All)
    
    def stressify(self, text: str) -> str:
        ukr_text_stressed = self.model(text)
        new_stressed = ""
        start = 0
        last = 0

        # shift stress symbol by one "при+віт" -> "пр+ивіт"
        while True:
            plus_position = ukr_text_stressed.find("+", start)
            if plus_position != -1:
                new_stressed += (
                    ukr_text_stressed[last : plus_position - 1] + "+" + ukr_text_stressed[plus_position - 1]
                )
                start = plus_position + 1
                last = start
            else:
                new_stressed += ukr_text_stressed[last:]
                break
        return new_stressed


class UkrainianAccentorStressifierModel(StressifierModel):
    def init_model(self):
        self.model = accentor
    
    def stressify(self, text: str) -> str:
        return self.model.process(text, mode='plus')


class StressifierRunner:
    models = {
        "Ukrainian Word Stressifier": UkrainianWordStressifierModel(), 
        "Ukrainian Accentor": UkrainianAccentorStressifierModel(),
    }
    
    def stressify(self, text: str, model_name: str="Ukrainian Word Stressifier") -> str:
        return self.models[model_name].stressify(text)


def make_pretty_text(text):
    for line in textwrap.wrap(text, width=100):
        print(line)

if __name__ == "__main__":

    stressifier_runner = StressifierRunner()
    for stressifier_model_name in ["Ukrainian Word Stressifier", "Ukrainian Accentor"]:
        stressed_text = stressifier_runner.stressify(DEFAULT_UNSTRESSED_TEXT, stressifier_model_name)
        print(f"The model `{stressifier_model_name}`")
        # make_pretty_text(stressed_text)
        print(stressed_text)
        print("\n")