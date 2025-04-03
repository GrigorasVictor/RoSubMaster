from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QProgressBar, QLabel, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import time

from audio_converter import AudioConverter
from video_converter import VideoConverter

# ======== THREAD HANDLER (Runs Any Function in a Separate Thread) ========
class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, function, *args, **kwargs):
        """Accepts a function and its arguments to run in a separate thread."""
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs, progress_callback=self.progress.emit)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(f"Error: {e}")

# ======== MAIN UI CLASS ========
class FileProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Processor")
        self.setGeometry(100, 100, 500, 300)
        self.file_path = None
        self.initUI()

    # ======== UI DESIGN ========
    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        self.label = QLabel("🔍 Select a file to process")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # File Selection Button
        self.button = QPushButton("📂 Choose File", self)
        self.button.setStyleSheet("padding: 10px; font-size: 14px;")
        self.button.clicked.connect(self.choose_file)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Progress Bar
        self.progress = QProgressBar(self)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #aaa;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 14px; color: #555;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    # ======== FILE SELECTION ========
    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "Video/Audio (*.mp4 *.wav)")
        if file_path:
            confirmation = QMessageBox.question(
                self, "Confirm Action", f"Do you want to process this file?\n{file_path}",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if confirmation == QMessageBox.Yes:
                self.file_path = file_path
                self.label.setText(f"Processing: {file_path}")
                self.start_processing()
            else:
                self.label.setText("File selection canceled.")

    # ======== PROCESSING LOGIC ========
    def start_processing(self):
        if not self.file_path:
            return

        self.progress.setValue(0)
        self.status_label.setText("🔄 Processing...")

        self.thread = WorkerThread(self.process_file_logic, self.file_path)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_processing_finished)
        self.thread.start()

    def update_progress(self, value):
        """Update progress bar incrementally."""
        new_value = self.progress.value() + value
        self.progress.setValue(min(new_value, 100))

    def process_file_logic(self, file_path, progress_callback):
        audio_convert = AudioConverter(model_size="small", file=file_path)
        video_convert = VideoConverter(file_path)
        tasks = {
            "Converting to WAV": lambda: video_convert.convert_to_wav(),
            "Transcribing Audio": lambda: audio_convert.transcribe_audio(),
            "Saving Subtitles": lambda: audio_convert.save_srt()
        }
        task_progress = 100 // len(tasks)  # Divide progress evenly

        for task, func in tasks.items():
            self.status_label.setText(f"🔄 {task}...")
            func()
            progress_callback(task_progress)

        return f"Processing completed for: {file_path}"

    # ======== FINAL RESULT ========
    def on_processing_finished(self, message):
        self.status_label.setText("✅ Processing completed!")
        QMessageBox.information(self, "Done", message)
        self.progress.setValue(100)

# ======== RUN APPLICATION ========
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileProcessorApp()
    window.show()
    sys.exit(app.exec_())
