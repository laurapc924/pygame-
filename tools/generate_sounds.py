"""Gera os 4 arquivos de som do Fox Crossing usando só a stdlib."""

import math
import random
import struct
import wave
from pathlib import Path

SOUNDS = Path(__file__).resolve().parent.parent / "assets" / "sounds"
SAMPLE_RATE = 22050


def write_wav(path, samples):
    n = len(samples)
    data = struct.pack(
        f"<{n}h",
        *(int(max(-1.0, min(1.0, s)) * 32767) for s in samples),
    )
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(data)


def sine(freq, t):
    return math.sin(2 * math.pi * freq * t)


def envelope(t, duration, attack, release):
    if t < attack:
        return t / attack
    if t > duration - release:
        return max(0.0, (duration - t) / release)
    return 1.0


def gen_collision():
    duration = 0.35
    n = int(SAMPLE_RATE * duration)
    out = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 12)
        freq = 200 - (200 - 60) * (t / duration)
        body = sine(freq, t)
        noise = random.uniform(-1, 1)
        out.append((0.5 * body + 0.5 * noise) * env * 0.7)
    return out


def gen_victory():
    notes = [(523.25, 0.15), (659.25, 0.15), (783.99, 0.15), (1046.50, 0.45)]
    out = []
    for freq, dur in notes:
        n = int(SAMPLE_RATE * dur)
        for i in range(n):
            t = i / SAMPLE_RATE
            env = envelope(t, dur, 0.005, 0.05)
            s = sine(freq, t) * 0.6 + sine(freq * 2, t) * 0.2
            out.append(s * env * 0.4)
    return out


def gen_menu():
    # Progressão I-vi-IV-V em Dó: C, Am, F, G. Loop de 8s.
    chords = [
        [261.63, 329.63, 392.00],  # C E G
        [220.00, 261.63, 329.63],  # A C E
        [174.61, 261.63, 349.23],  # F C F
        [196.00, 246.94, 293.66],  # G B D
    ]
    chord_dur = 2.0
    out = []
    for chord in chords:
        n = int(SAMPLE_RATE * chord_dur)
        for i in range(n):
            t = i / SAMPLE_RATE
            env = envelope(t, chord_dur, 0.3, 0.3)
            s = sum(sine(f, t) for f in chord) / len(chord)
            out.append(s * env * 0.25)
    return out


def gen_game():
    # Bass pulsado + arpejo de Lá menor. Loop de 4s.
    duration = 4.0
    arp = [220.00, 261.63, 329.63, 261.63]  # A C E C
    note_dur = 0.25
    n = int(SAMPLE_RATE * duration)
    out = []
    for i in range(n):
        t = i / SAMPLE_RATE
        pulse_t = t % 0.5
        pulse_env = max(0.0, 1.0 - pulse_t * 4)
        bass = sine(110, t) * pulse_env * 0.35
        note_idx = int(t / note_dur) % len(arp)
        note_t = t % note_dur
        note_env = max(0.0, 1.0 - note_t * 5)
        melody = sine(arp[note_idx], t) * note_env * 0.2
        out.append(bass + melody)
    return out


def main():
    SOUNDS.mkdir(parents=True, exist_ok=True)
    write_wav(SOUNDS / "collision.wav", gen_collision())
    write_wav(SOUNDS / "victory.wav", gen_victory())
    write_wav(SOUNDS / "menu.wav", gen_menu())
    write_wav(SOUNDS / "game.wav", gen_game())
    for name in ("collision.wav", "victory.wav", "menu.wav", "game.wav"):
        path = SOUNDS / name
        print(f"{name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
