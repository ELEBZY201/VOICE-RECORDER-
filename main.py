# It is necessary to import this library (including os, wave, time,
#threading, tkinterGUI, and pyaudio)
import os
import wave
import time
import threading
import tkinter as tk
import pyaudio

#It defines a class voice recorder that encapsulates the functionality of
#the voice recorder
class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(text="🎙", font=("Arial", 120, "bold"),
                                command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()

# The voice recorder class initializes a tkinter window with a large
#button () to start and stop recording and a label to display the
#recording duration


#Clicking the button, the recording triggers on or off

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="red")
        else:
            self.recording = True
            self.button.config(fg="blue")
            threading.Thread(target=self.record).start()



#When recording is initiated, it starts a new thread to handle the
#recording process


    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                            input=True, frames_per_buffer=1024)

        frames = []

#The recording method continuously reads audio data from the
#microphone using Pyaduio also updating the recording duration
#while on play

        start = time.time()
        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            sec = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(sec):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()



 #When recording is stopped, it stops the audio stream, closes
    #pyaudio, and saves the recorded audio in a WAV file
        exists = True
        i = 1
        while exists:
            if os.path.exists(f"recording{i}.wav"):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f"recording{i}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()


VoiceRecorder()
