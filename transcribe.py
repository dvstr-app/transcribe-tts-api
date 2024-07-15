"""
pip install transformers
pip install torch 
pip install pytube
"""

import torch
from youtube import download_audio
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

def extract_text(video_url: str):
    """
    Extracts text with time segments from an audiofile given the path
    return: {
        language: str,
        text: str,
        chunks: {
            text: str,
            start: float,
            end: float,
        }
    }
    """
    # load audio and pad/trim it to fit 30 seconds
    out_path = "/home/"
    audio_path = download_audio("video_url", out_path)
    result = pipe(audio_path, generate_kwargs={"task": "translate"})
    return result

