import os

import whisper
import srt
from datetime import timedelta
import torch
from tqdm import tqdm
from transformers import MarianMTModel, MarianTokenizer

class AudioConverter:
    def __init__(self, model_size="small", file=None):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        whisper.DISABLE_TRITON = True
        self.model = whisper.load_model(model_size).to(self.device)

        self.file = file
        self.subtitles = None
        print(self.file)

        model_name = "Helsinki-NLP/opus-mt-en-ro"
        self.translator = MarianMTModel.from_pretrained(model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)

    def transcribe_audio(self):
        print("🔄 Transcriem audio...")
        result = self.model.transcribe(self.file, language="en", word_timestamps=True, verbose=True)

        subtitles = []
        for i, segment in enumerate(tqdm(result["segments"], desc="Progress: ")):
            start = timedelta(seconds=segment["start"])
            end = timedelta(seconds=segment["end"])
            text = segment["text"]

            translated_text = self.translate_text(text)
            subtitles.append(srt.Subtitle(i+1, start, end, translated_text))

        print("✅ Transcriere și traducere finalizată!")
        self.subtitles = subtitles

    def translate_text(self, text: str) -> str:
        tokens = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = self.translator.generate(**tokens)
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)

    def save_srt(self):
        output_srt = self.file.rsplit(".", 1)[0] + ".srt"
        if self.subtitles is None:
            raise ValueError("Subtitrările nu au fost generate. Rulează transcribe_audio() mai întâi.")
        with open(output_srt, "w", encoding="utf-8") as f:
            f.write(srt.compose(self.subtitles))

        print(f"✅ Subtitrările traduse au fost salvate: {output_srt}")

    def process_audio_to_srt(self):
        self.transcribe_audio()
        self.save_srt()