import os
import wave
import argparse

import gradio as gr

from eng_to_ukr.yt_downloader import download_video_and_audio
from eng_to_ukr.whisper_translator import WhisperTranslator, WhisperModels
from accentor.stressifier import StressifierRunner, DEFAULT_UNSTRESSED_TEXT
from text_to_speech.text_to_speech_models import UkrainianTtsEspnet


parser = argparse.ArgumentParser(description="")
parser.add_argument('--share', action='store_true')
parsed_args = parser.parse_args()


DEFAULT_VIDEO_URL = "https://www.youtube.com/watch?v=Fr_MHKIYBcg"

DOWNLOADED_VIDEO_PATH = ""
DOWNLOADED_AUDIO_PATH = ""


stressifier_runner = StressifierRunner()
tts_model = UkrainianTtsEspnet()


def speech_to_text(video_url: str, model_size_str: str):
    global DOWNLOADED_VIDEO_PATH
    global DOWNLOADED_AUDIO_PATH
    DOWNLOADED_VIDEO_PATH, DOWNLOADED_AUDIO_PATH = download_video_and_audio(video_url=video_url)
    whisper_translator = WhisperTranslator(WhisperModels(model_size_str))
    return whisper_translator.get_text_from_speech(DOWNLOADED_AUDIO_PATH)

    
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
        # Download the video and audio by URL and STT
        with gr.Row():
            gr.Label("🎥➡️📝 Get text from video (Speech-To-Text)")
        with gr.Row():
            with gr.Column(scale=2):
                yt_video_url = gr.Textbox(label="YouTube video url", value=DEFAULT_VIDEO_URL)
                whisper_models_size = [model_size.value for model_size in list(WhisperModels)]
                whisper_models_size_picker = gr.Dropdown(
                    choices=whisper_models_size,
                    value=whisper_models_size[0],
                    label="Choice a size of the STT model (the bigger size -> the better results -> the longer to process)"
                )
            with gr.Column(scale=2):
                spoken_text = gr.Textbox(label="Spoken text")
        with gr.Row():
            run_stt = gr.Button("Run Speech-To-Text")
            run_stt.click(
                fn=speech_to_text, 
                inputs=[
                    yt_video_url, 
                    whisper_models_size_picker
                ], 
                outputs=spoken_text,
            )
                
        # Stressifier model
        with gr.Row():
            gr.Label("📙 Stressifier model")
        with gr.Row():
            with gr.Column(scale=2):
                unstressified_text = gr.Textbox(label="Unstressefied text", value=DEFAULT_UNSTRESSED_TEXT)
                stress_paste_btn = gr.Button("Paste STT text")
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
            stress_paste_btn.click(
                fn=lambda text: text,
                inputs=spoken_text,
                outputs=unstressified_text
            )
            
        # TTS model
        with gr.Row():
            gr.Label("🗣️ Text-To-Speech")
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

