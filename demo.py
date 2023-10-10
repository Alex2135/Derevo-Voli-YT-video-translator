import os
import wave
import argparse

import gradio as gr

from accentor.stressifier import StressifierRunner, default_unstressed_text
from text_to_speech.text_to_speech_models import UkrainianTtsEspnet


parser = argparse.ArgumentParser(description="")
parser.add_argument('--share', action='store_true')
parsed_args = parser.parse_args()


stressifier_runner = StressifierRunner()
tts_model = UkrainianTtsEspnet()


def accentor(ukrainian_text: str, stressifier_model_name: str) -> str:
    # ["Ukrainian Word Stressifier", "Ukrainian Accentor"]
    stressed_text = stressifier_runner.stressify(ukrainian_text, stressifier_model_name)
    return stressed_text


def text_to_speech(ukrainian_stressefied_text: str, stressifier_model_name: str):
    return tts_model.run_tts(ukrainian_stressefied_text, stressifier_model_name)
    
    
def create_dummy_wav_file(file_name):
    # Define the WAV file parameters
    num_channels = 1  # Mono audio
    sample_width = 2  # 2 bytes per sample for 16-bit audio
    frame_rate = 44100  # Sample rate (samples per second)
    num_frames = 0  # You can set this to the number of audio frames you have
    comptype = "NONE"
    compname = "not compressed"
    with wave.open(file_name, "wb") as wav_file:
        wav_file.setparams((num_channels, sample_width, frame_rate, num_frames, comptype, compname))


if __name__ == "__main__":
    with gr.Blocks() as demo:
        # Stressifier model
        with gr.Row():
            gr.Label("Stressifier model 📙")
        with gr.Row():
            with gr.Column(scale=2):
                unstressified_text = gr.Textbox(label="Unstressefied text", value=default_unstressed_text)
                stressifier_models_names = list(StressifierRunner.models.keys())
                stressifier_picker = gr.Dropdown(
                    choices=stressifier_models_names,
                    value=stressifier_models_names[0],
                    label="Choice stressifier model"
                )
            with gr.Column(scale=2):
                stressified_text = gr.Textbox(label="Stressefied text")
        with gr.Row():
            run_stress = gr.Button("Run stressifier")
            run_stress.click(
                fn=accentor, 
                inputs=[
                    unstressified_text, 
                    stressifier_picker
                ], 
                outputs=stressified_text,
            )
            
        # TTS model
        with gr.Row():
            gr.Label("Text-To-Speech 🗣️")
        with gr.Row():
            with gr.Column(scale=2):
                tts_stressified_text = gr.Textbox(label="Stressefied text")
                tts_paste_btn = gr.Button("Paste stressefied text")
                tts_voices_list = list(UkrainianTtsEspnet.tts_voices.keys())
                voices_picker = gr.Dropdown(
                    choices=tts_voices_list,
                    value=tts_voices_list[0],
                    label="Actor voice"
                )
            with gr.Column(scale=2):            
                # Create a new WAV file
                if not os.path.exists("/tmp/audio"):
                    os.mkdir("/tmp/audio")
                audio_file_path = "/tmp/audio/test.wav"
                create_dummy_wav_file("/tmp/audio/test.wav")
                tts_output = gr.Audio(label="Stressefied text", value=audio_file_path)
        with gr.Row():
            run_tts_btn = gr.Button("Run text-to-speech")
            run_tts_btn.click(
                fn=text_to_speech, 
                inputs=[
                    tts_stressified_text, 
                    voices_picker
                ], 
                outputs=tts_output,
            )
            tts_paste_btn.click(
                fn=lambda text: text,
                inputs=stressified_text,
                outputs=tts_stressified_text
            )
    if parsed_args.share:
        launch_args = {
            "share": True
        }
    else:
        launch_args = {
            "server_name": "0.0.0.0",
            "server_port": 7860
        }
    demo.launch(**launch_args)

