from moviepy import VideoFileClip

class VideoConverter:
    def __init__(self, file):
        self.file = file

    def convert_to_wav(self):
        if self.file.endswith(".wav"):
            return
        if not self.file.endswith(".mp4"):
            raise ValueError("Input file must have a .mp4 extension.")
        output_file = self.file.replace(".mp4", ".wav")
        with VideoFileClip(self.file) as video:
            audio = video.audio
            audio.write_audiofile(output_file)