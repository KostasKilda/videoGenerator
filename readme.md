# Project Name: Video generator

## Overview

This Python-based project heavily relies on APIs and libraries to create captivating audio-visual content. It leverages GPT Whisper to generate scripts, converts them to .mp3 files using ElevenLabs Voice Over service, downloads appropriate images from Unsplash.com via HTTP requests, and finally merges everything using the MoviePy library in Python to create a collage of images with a voice-over narration.

## Requirements

- Python 3.10.11
- OpenAi 1.12.0
- Requests 2.25.1
- beautifulsoup4 4.11.1
- MoviePy 1.0.3
- ElevenLabs API


## Installation

1. Clone the repository:

```bash
git clone https://github.com/KostasKilda/videoGenerator.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environmental variables:

    - **elevenLabsKey**: Your ElevenLabs API key
    - **elevenLabsVoice**: ElevenLabs voice ID
    - **WhisperPrompt**: GPT Whisper prompt

## Usage

1. Run the Python script:

```bash
python main.py
```


## Environmental Variables

Ensure you have the following environmental variables set:

- `elevenLabsKey`: Your API key for ElevenLabs
- `elevenLabsVoice`: Your ElevenLabs voice ID
- `WhisperPrompt`: Your GTP Whisper prompt
<Br> Documentation for <b>Whisper</b>: https://github.com/openai/openai-python

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
