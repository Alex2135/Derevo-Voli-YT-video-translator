from abc import ABC


class SpeechOverlap(ABC):
    # Step 1
    def convert_srt_to_subtitles(youtube_subs_srt_file: str) -> List[dict]:
        """Method returns youtube subtitles with timecodes, content, etc"""
        pass

    # Step 2
    def split_subtitles_by_sentences(youtube_subtitles_list: List[dict]) -> List[dict]:
        """ """
        pass
    
    # Step 3
    def translate_subtitles(translator_object, sentences_list: List[dict]) ->  List[dict]:
        pass
    
    # Step 4
    def accent_subtitles():
        pass

    # Step 5
    def make_audio_for_every_sentence(sentences_list: List[dict], speed_settings: List[dict]) -> List[dict]:
        # TODO: Remove "+" signe before calculating speed
        """
        """
        pass
    
    # Step 6
    def combine_audio(audio_sentences: List[dict]) -> str:
        pass
    
    # Step 7
    def overlap_audio_on_video(video_path, audio_path):
        pass

