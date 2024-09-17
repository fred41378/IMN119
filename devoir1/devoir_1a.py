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


def plot_sinus_wave(cycle, amp, sampling, noise_level, phase, vert_shift):
    """
    Generate x and y values for a sinusoidal wave considering cycleuency, amplitude, sampling, noise,
    phase shift, and vertical shift.

    :param cycle: Number of cycle in the period
    :param amp: Amplitude of the sine wave
    :param sampling: Number of samples (resolution)
    :param noise_level: Level of noise to add to the sine wave
    :param phase: Phase shift of the sine wave
    :param vert_shift: Vertical shift of the sine wave
    :return: x and y values of the wave
    """
    x = np.linspace(0, 1000, sampling)
    noise = np.random.normal(0, noise_level, sampling)

    # À MODIFIER: La ligne suivante sera la ligne de calcul des valeurs de sinus
    y = amp * np.sin(2*np.pi*cycle*(1/x.max())*x+phase) + noise + vert_shift
    # Rien d'autre devrait être modifié après cette ligne

    y = np.clip(y, 0, 255)

    return x, y


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
    x, y = plot_sinus_wave(CYCLE, AMP, SAMPLING, NOISE, PHASE, VERT_SHIFT)
    line.set_data(x, y)
    ax.relim()
    ax.autoscale_view()
    canvas.draw()


# Create the main window
root = tk.Tk()

# Create the initial plot
fig, ax = plt.subplots()
x, y = plot_sinus_wave(CYCLE, AMP, SAMPLING, NOISE, PHASE, VERT_SHIFT)
line, = ax.plot(x, y)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 255)

# Set up the canvas for embedding in Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Cycle slider
cycle_label = tk.Label(root, text="Cycle (1-100):")
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
sampling_label = tk.Label(root, text="Sampling (5-500):")
sampling_label.pack()
sampling_scale = tk.Scale(root, from_=5, to=1000, orient=tk.HORIZONTAL, resolution=5, command=update_sampling)
sampling_scale.set(SAMPLING)
sampling_scale.pack()

# Noise level slider
noise_level_label = tk.Label(root, text="Noise Level (0-50):")
noise_level_label.pack()
noise_level_scale = tk.Scale(root, from_=0, to=50, orient=tk.HORIZONTAL, resolution=1, command=update_noise)
noise_level_scale.set(NOISE)
noise_level_scale.pack()

# Phase shift slider (0 to 360 degrees)
phase_label = tk.Label(root, text="Phase Shift (0-360 degrees):")
phase_label.pack()
phase_scale = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, resolution=1, command=update_phase)
phase_scale.set(0)  # Set initial phase to 0
phase_scale.pack()

# Vertical shift slider (0 to 255)
vert_shift_label = tk.Label(root, text="Vertical Shift (0-255):")
vert_shift_label.pack()
vert_shift_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, resolution=1, command=update_vert_shift)
vert_shift_scale.set(127)  # Set initial vertical shift to 127
vert_shift_scale.pack()

# Quit button
quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack()

# Start the Tkinter event loop
root.mainloop()
