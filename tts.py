"""
git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip install -e .
python -m unidic download
pip install audiostretchy
pip install pydub
apt install ffmpeg
"""

from audiostretchy.stretch import stretch_audio, AudioStretch
from pydub import AudioSegment
from melo.api import TTS
import torch


speed = 1.0
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id


def get_audio_duration(audio_path):
    audio_stretch = AudioStretch()
    audio_stretch.open(audio_path)
    return round(audio_stretch.nframes / audio_stretch.framerate, 2)


def get_tts_audio_bytes(segment):
    """
    synthesises speech and stretches it to match segment duration

    params: segment: {
        "text": str
        "start": float
        "end": float
    }
    return: audio bytes
    """
    text = segment.text
    start = segment.start
    end = segment.end
    duration = end - start

    audio_path = 'output.wav'
    stretched_path = 'stretched.wav'
    model.tts_to_file(text, speaker_ids['EN-US'], audio_path, speed=speed)

    # stretch to match the time segment
    ratio = duration / get_audio_duration(audio_path)
    stretch_audio(audio_path, stretched_path, ratio=ratio)
    # trim the length
    audio = AudioSegment.from_wav(stretched_path)
    # trim in ms
    audio[:duration*1000].export(stretched_path, format="wav")
    # return wav audio bytes
    with open(stretch_audio, "rb") as audio_bytes:
        return audio_bytes.read()
