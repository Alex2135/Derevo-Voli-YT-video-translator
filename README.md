# DerevoVoli YouTube Video Translator

## Setup

To start working with the project you need `Linux` system, or `Windows` system with implemented `WSL` via `VisualCode` or similar. The repository using `python v3.10`

Create the environment
```bash
python3 -m venv venv
```

Activate environment
```bash
source venv/bin/activate
```

Install dependencies
```bash
pip3 install -r requirements.txt
```

## How to run the code

The demo is available as a gradio app. To launch the app in your local machine you need to execute the next command:
```bash
python3 demo.py 
```

If you want to share the app like explicit resource by URL you need to run a command:
```bash
python3 demo.py --share
```

The you will get a link for the app that you could share for `72 hours` while the *running machine is working*.

## Build Docker image

To build docker image use the next command:
```bash
docker build . -t derevo-voli-ytvt
```

To run a docker container with next command make sure that you are located in the repo directory:
```bash
cd Derevo-Voli-YT-video-translator
docker run -it -v ./:/app -p 7860:7860 derevo-voli-ytvt
```