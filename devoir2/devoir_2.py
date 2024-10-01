#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import sys

from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pydub
import pygame.mixer
from scipy import signal
from scipy.io import wavfile
import tkinter as tk
from tkinter import filedialog


global SOUND_DATA, SOUND_RATE, SOUND
SOUND_DATA = None
SOUND_RATE = None
SOUND = None


def play_sound():
    global SOUND_DATA, SOUND_RATE, SOUND

    if SOUND_DATA is not None:
        sampling_freq = float(sampling_slider.get())
        noise_level = float(noise_slider.get())
        amplitude = float(amplitude_slider.get())
        speed = float(speed_slider.get())

        noise_data = np.random.normal(0, noise_level, len(SOUND_DATA))
        noisy_data = SOUND_DATA + noise_data
        scaled_data = (amplitude * noisy_data).astype(np.int16)

        # Resampling
        t = np.linspace(0, 1, len(scaled_data))
        t_new = np.linspace(0, 1 / speed, int(len(scaled_data) * sampling_freq/speed))
        print(len(t), len(t_new))
        sampled_data, t = signal.resample(scaled_data, len(t_new), t=t)
        sampled_data = sampled_data.astype(scaled_data.dtype)
        wavfile.write('output.wav', int(sampling_freq * SOUND_RATE * 2), sampled_data)

        pygame.mixer.init()
        pygame.mixer.music.load("output.wav")
        pygame.mixer.music.play()
        update_signal_plot(sampled_data, t_new)

def stop_sound():
    pygame.mixer.music.stop()


def quit_program():
    pygame.mixer.quit()
    root.quit()


def update_signal_plot(x, t):
    if x is not None:
        fig.clear()
        plt.plot(t, x, alpha=0.5)
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title("Signal")
        plt.show()
        fig.canvas.draw()


root = tk.Tk()

fig = plt.Figure(figsize=(5, 3), dpi=100)
signal_plot = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

sampling_label = tk.Label(root, text="Sampling frequency (0.1-10):")
sampling_label.pack()
sampling_slider = tk.Scale(root, from_=0.1, to=10,
                           resolution=0.1, orient=tk.HORIZONTAL)
sampling_slider.set(1)
sampling_slider.pack()

noise_label = tk.Label(root, text="Noise level (0-1000):")
noise_label.pack()
noise_slider = tk.Scale(root, from_=0, to=1000,
                        resolution=10, orient=tk.HORIZONTAL)
noise_slider.set(0)
noise_slider.pack()

amplitude_label = tk.Label(root, text="Amplitude (0.1-2):")
amplitude_label.pack()
amplitude_slider = tk.Scale(root, from_=0.1, to=2,
                            resolution=0.01, orient=tk.HORIZONTAL)
amplitude_slider.set(1)
amplitude_slider.pack()

speed_label = tk.Label(root, text="Speed (0.5-2):")
speed_label.pack()
speed_slider = tk.Scale(root, from_=0.5, to=2,
                            resolution=0.1, orient=tk.HORIZONTAL)
speed_slider.set(1)
speed_slider.pack()

play_button = tk.Button(root, text="Play sound", command=play_sound)
play_button.pack()

stop_button = tk.Button(root, text="Stop sound", command=stop_sound)
stop_button.pack()

quit_button = tk.Button(root, text="Quit", command=quit_program)
quit_button.pack()

SOUND = pydub.AudioSegment.from_mp3("manhattan.wav")
SOUND_DATA = np.array(SOUND.get_array_of_samples())
SOUND_RATE = SOUND.frame_rate
update_signal_plot(SOUND_DATA, np.linspace(0, 1, len(SOUND_DATA)))

root.mainloop()
