#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

global CYCLE, AMP, SAMPLING, NOISE, PHASE, VERT_SHIFT

CYCLE = 1.0
AMP = 127.0
SAMPLING = 1000
NOISE = 0.0
PHASE = 0.0
VERT_SHIFT = 127.0


def create_sinus_wave_image(cycle, amp, sampling, noise_level, phase, vert_shift):
    """
    Generate a sinusoidal wave image considering cycle, amplitude, sampling, noise,
    phase shift, and vertical shift.

    :param cycle: Frequency of the sine wave
    :param amp: Amplitude of the sine wave
    :param sampling: Number of samples (resolution)
    :param noise_level: Level of noise to add to the sine wave
    :param phase: Phase shift of the sine wave
    :param vert_shift: Vertical shift of the sine wave
    :return: Generated image as a 2D numpy array
    """
    x = np.linspace(0, 1000, sampling)
    noise = np.random.normal(0, noise_level, sampling)

    # À MODIFIER: La ligne suivante sera la ligne de calcul des valeurs de sinus
    y = amp * np.sin(2*np.pi*cycle*(1/x.max())*x+phase) + noise + vert_shift
    # Rien d'autre devrait être modifié après cette ligne

    y = np.clip(y, 0, 255)

    image = np.zeros((sampling, sampling), dtype=np.uint8)
    for idx, y_val in enumerate(y):
        image[:, idx] = y_val

    return image


def update_cycle(val):
    global CYCLE
    CYCLE = float(val)
    update_plot()


def update_amp(val):
    global AMP
    AMP = float(val)
    update_plot()


def update_sampling(val):
    global SAMPLING
    SAMPLING = int(val)
    update_plot()


def update_noise(val):
    global NOISE
    NOISE = float(val)
    update_plot()


def update_phase(val):
    global PHASE
    PHASE = float(val) * np.pi / 180  # Convert degrees to radians
    update_plot()


def update_vert_shift(val):
    global VERT_SHIFT
    VERT_SHIFT = float(val)
    update_plot()


def update_plot():
    image = create_sinus_wave_image(CYCLE, AMP, SAMPLING, NOISE, PHASE, VERT_SHIFT)
    ax.clear()
    ax.imshow(image, cmap='gray', origin='lower', aspect='auto',
              extent=[0, 1000, 0, 1000], vmin=0, vmax=255)
    canvas.draw()


root = tk.Tk()

fig, ax = plt.subplots()
image = create_sinus_wave_image(CYCLE, AMP, SAMPLING, NOISE, PHASE, VERT_SHIFT)
ax.imshow(image, cmap='gray', origin='lower', aspect='auto',
          extent=[0, 1000, 0, 1000], vmin=0, vmax=255)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Frequency slider
cycle_label = tk.Label(root, text="Frequency (1-100):")
cycle_label.pack()
cycle_scale = tk.Scale(root, from_=1, to=100,
                      orient=tk.HORIZONTAL, resolution=1, command=update_cycle)
cycle_scale.set(CYCLE)
cycle_scale.pack()

# Amplitude slider
amp_label = tk.Label(root, text="Amplitude (1-127):")
amp_label.pack()
amp_scale = tk.Scale(root, from_=1, to=127,
                     orient=tk.HORIZONTAL, resolution=1, command=update_amp)
amp_scale.set(AMP)
amp_scale.pack()

# Sampling slider
sampling_label = tk.Label(root, text="Sampling (10-1000):")
sampling_label.pack()
sampling_scale = tk.Scale(root, from_=10, to=1000,
                          orient=tk.HORIZONTAL, resolution=10, command=update_sampling)
sampling_scale.set(SAMPLING)
sampling_scale.pack()

# Noise slider
noise_level_label = tk.Label(root, text="Noise Level (0-50):")
noise_level_label.pack()
noise_level_scale = tk.Scale(
    root, from_=0, to=50, orient=tk.HORIZONTAL, resolution=1, command=update_noise)
noise_level_scale.set(NOISE)
noise_level_scale.pack()

# Phase slider (in degrees for user convenience)
phase_label = tk.Label(root, text="Phase Shift (0-360 degrees):")
phase_label.pack()
phase_scale = tk.Scale(root, from_=0, to=360,
                       orient=tk.HORIZONTAL, resolution=1, command=update_phase)
phase_scale.set(0)
phase_scale.pack()

# Vertical shift slider
vert_shift_label = tk.Label(root, text="Vertical Shift (0-255):")
vert_shift_label.pack()
vert_shift_scale = tk.Scale(
    root, from_=0, to=255, orient=tk.HORIZONTAL, resolution=1, command=update_vert_shift)
vert_shift_scale.set(127)
vert_shift_scale.pack()

# Quit button
quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack()

root.mainloop()
