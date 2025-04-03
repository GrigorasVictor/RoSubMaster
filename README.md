# RoSubMaster
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)  
**Automatically Add Romanian Subtitles to MP4 Videos**  

Convert MP4 videos with English audio into Romanian-subtitled MP4 files. Perfect for tutorials, lectures, or personal videos!

---

## Features ✨  
- 🎥 **MP4 Support** - Works exclusively with `.mp4` files  
- 🔊 **Auto Transcription** - Extract audio and transcribe English speech to text  
- 🇷🇴 **Auto Translation** - Translate English text to Romanian subtitles  
- 📁 **Simple Workflow** - Select a file → Process → Get subtitled video in the same folder  

---

## Installation ⚙️  
1. Install **FFmpeg** ([Windows](https://www.gyan.dev/ffmpeg/builds/), [Linux/macOS](https://ffmpeg.org/download.html))  
2. Clone the repo:  
```bash  
git clone https://github.com/yourusername/RoSubMaster.git  
```  
3. Install dependencies:  
```bash  
cd RoSubMaster  
pip install -r requirements.txt  
```  

---

## Usage 🚀  
1. Run the app:  
```bash  
python app.py  
```  
2. Click "Select MP4 File" and choose your video.  
3. Wait for processing (see console for progress).  
4. **Done!** Outputs:  
   - `[original_name]_RO.wav`
   - `Subtitles/[original_name]_RO.srt` (Romanian subtitle file)  

---

## Example 📂  
**Input**:  
`/Videos/tutorial.mp4`  

**Output**:  
```  
/Videos/  
├── tutorial_RO.mp4
├── tutorial_RO.wav    
└── tutorial_RO.srt  
```  

---

## Requirements 📋  
- Python 3.8+  
- FFmpeg installed system-wide  
- **Core Models** (auto-downloaded on first run):  
  - 🎙️ `openai/whisper-small` - Speech-to-text transcription ([Model Card](https://github.com/openai/whisper))  
  - 🇷🇴 `Helsinki-NLP/opus-mt-en-ro` - English→Romanian translation ([Model Card](https://huggingface.co/Helsinki-NLP/opus-mt-en-ro))  
- (Optional) NVIDIA GPU for faster processing  

---

## Notes ⚠️  
- Works best with clear English audio (no background noise).  

--- 

Built for content creators, educators, and movie enthusiasts. 🎬  
