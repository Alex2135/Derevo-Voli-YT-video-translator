from abc import ABC
from utils import parse_srt, cuts, translate
from ukrainian_tts.tts import TTS, Voices, Stress
import IPython.display as ipd
from pydub import AudioSegment
import os, json
import torch
from pydub import AudioSegment
from pydub.playback import play
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

class SpeechOverlap(ABC):
    # Step 1

    def convert_srt_to_subtitles(youtube_subs_srt_file: str) -> list[dict]:
        """Method returns youtube subtitles with timecodes, content, etc"""
        srt = open(youtube_subs_srt_file, 'r', encoding="utf-8").read()
        return parse_srt(srt)

    # Step 2
    def split_subtitles_by_sentences(youtube_subtitles_list: list[dict]) -> list[dict]:
        splited = []
        data = youtube_subtitles_list 
        start = data[0]['start']
        end = start
        text = ''
        id = 0
        for i in data:
            parts = cuts(i)
            if len(parts[-1]['content']) == 0:
              end = i['start']
              for part in parts[0: len(parts)-1]:
                text += " " + part['content']
                end += part['time']
                splited.append({
                   'id' : id,
                   'start': start,
                    'end': end,
                   'content': text
                })
                id += 1
                text = ''
                start = end

            else:
              text += " " + parts[0]['content']
              end += parts[0]['time']
              for part in parts[1:]:
                splited.append({
                  'id': id,
                  'start' :start,
                  'end' : end,
                  'content' : text
                })
                id += 1
                text = part['content']
                end += part['time']
        return splited
    
    # Step 3
    def translate_subtitles(translator_object, sentences_list: list[dict]) ->  list[dict]:
        translated = []
        for i in sentences_list:
            translated_text = translate(translator_object, i['content'])
            speed = 2.6897 - ((i['end']-i['start'])/len(translated_text)) * 0.021
            translated.append({"id" : i['id'],
                               "original" : i['content'],
                               "translated":translated_text,
                               "start": i['start'],
                               "end": i['end'],
                               "speed": speed})

    
    # Step 4
    def accent_subtitles():
        pass

    # Step 5
    #this step should be visualized
    def make_audio_for_every_sentence(sentences_list: list[dict]) -> list[dict]:
        if not os.path.exists('records'):
            os.mkdir('records')
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        tts = TTS(device)

        for sentence in sentences_list:
            filename = "records/output{}.wav".format(sentence['id'])
            with open(filename, mode="wb") as file:
                _, output_text = tts.tts(sentence['translated'], Voices.Mykyta.value, Stress.Dictionary.value, file, sentence['speed'])
                sound = AudioSegment.from_wav(filename)
            sentence['audiofile'] = filename
        return sentences_list

    # Step 6
    def combine_audio(audio_sentences: list[dict], original_audio: str, final_audio:str, percent_left: int):
        #TODO add logic for calculating volume percentage 
        original_audio_segment = AudioSegment.from_file(original_audio)- 15#add percentage calculation, reducing sound volume for 15 dB
        audio_segments = [ AudioSegment.from_file("sentence['audiofile'], 'wav') for sentence in audio_sentences]
        end = 0
        playlist = AudioSegment.empty()
        for sentence in audio_sentences:
            playlist += AudioSegment.silent(duration=sentence['start'] - end)
            playlist += sounds[sentence['id']]
            end = sentence['end']
        final_audio = quite_sound.overlay(playlist)
        final_audio.export(final_audio, format=final_audio.split('.')[-1])

        

    # Step 7
    def overlap_audio_on_video(orig_video: str, final_video: str, audio_path:str):
        video_clip = VideoFileClip(orig_video)
        audio_clip = AudioFileClip(audio_path)

        final_clip = video_clip.set_audio(audio_clip)

        final_clip.write_videofile(final_video)
        pass

