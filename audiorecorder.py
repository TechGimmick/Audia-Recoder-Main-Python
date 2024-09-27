import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        self.frames = []
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)
        self.is_recording = True
        self.record_thread = Thread(target=self.record)
        self.record_thread.start()

    def record(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        self.record_thread.join()
        self.stream.stop_stream()
        self.stream.close()

    def save_recording(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def close(self):
        self.audio.terminate()


class App:
    def __init__(self, root):
        self.recorder = AudioRecorder()
        self.is_recording = False

        self.root = root
        self.root.title("Audio Recorder")

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Recording", command=self.save_recording)
        self.save_button.pack(pady=10)

    def start_recording(self):
        if not self.is_recording:
            self.recorder.start_recording()
            self.is_recording = True
            messagebox.showinfo("Info", "Recording started")

    def stop_recording(self):
        if self.is_recording:
            self.recorder.stop_recording()
            self.is_recording = False
            messagebox.showinfo("Info", "Recording stopped")

    def save_recording(self):
        if not self.is_recording and self.recorder.frames:
            filename = "recording.wav"
            self.recorder.save_recording(filename)
            messagebox.showinfo("Info", f"Recording saved as {filename}")
        else:
            messagebox.showwarning("Warning", "No recording to save or still recording")

    def on_closing(self):
        if self.is_recording:
            self.recorder.stop_recording()
        self.recorder.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
