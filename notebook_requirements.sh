pip3 install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
pip3 install git+https://github.com/openai/whisper.git
pip3 install deep-translator tqdm
pip3 install TTS==0.13.3
pip3 install git+https://github.com/egorsmkv/ukrainian-accentor.git
pip install ukrainian-word-stress
pip install git+https://github.com/huggingface/transformers
pip install transformers[sentencepiece]
pip3 install sentencepiece
pip uninstall protobuf -y
pip install protobuf==4.21

python3 -c "import os; os.kill(os.getpid(), 9)"