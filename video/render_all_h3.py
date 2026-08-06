#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render all 9 ATMBKK scenes via H3 I2V (landscape 832x480, 81f, native audio), sequential."""
import os, subprocess, sys, time, glob

H3 = os.path.expanduser("~/.hermes/scripts/h3_i2v.py")
FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes_frames")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
os.makedirs(OUT_DIR, exist_ok=True)

# H3 motion prompts (with light ambience for native audio; narration added later)
H3P = {
 1:"slow warm push toward a happy family stretching at dawn in Bangkok, city skyline glowing, gentle golden light, joyful mood, soft morning ambience, no text",
 2:"families with kids at a colorful fun run start line, balloons and ribbons, cheerful festive morning, gentle camera move, joyful crowd ambience, no text",
 3:"family running together past golden Grand Palace spires, kids running happily, spectators cheering, warm golden light, light tracking shot, cheering ambience, no text",
 4:"family crossing the finish line together, confetti falling, celebrating with medals, joyful smiles, bright warm tones, celebration crowd cheers, no text",
 5:"family enjoying Thai food celebration after the run, mango sticky rice, happy together, warm inviting light, gentle camera, soft happy music, no text",
 6:"family sightseeing at Grand Palace and river, relaxed holiday, golden afternoon, light bokeh, gentle camera, calm ambient, no text",
 7:"family strolling through a lively Bangkok night market, colorful food stalls, warm lantern light, joyful evening, slow push, lively market ambience, no text",
 8:"group of families posing together at the race, smiling, holding medals, sunset glow, joyful candid, gentle camera, warm ambience, no text",
 9:"family silhouette running toward golden finish arch, red and gold ribbons, cinematic hero shot, warm celebratory, uplifting, triumphant ambience, no text",
}

def run(n):
    img = os.path.join(FRAMES_DIR, f"s{n}.png")
    # prefix must be a PLAIN filename (no path) — SaveVideo node rejects paths on Windows server.
    prefix = f"s{n}"
    prompt = H3P[n]
    cmd = ["python3", H3, img, prefix, "-", "--width", "832", "--height", "480", "--frames", "81", "--steps", "20", "--sampler", "res_multistep"]
    print(f"\n=== Scene {n} === ({time.strftime('%H:%M:%S')})", flush=True)
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True)
    print(p.stdout, flush=True)
    if p.stderr: print("ERR:", p.stderr[-1500:], flush=True)
    if p.returncode != 0:
        print(f"Scene {n} FAILED rc={p.returncode}", flush=True)
        return False
    # h3_i2v.py saves to ~/{prefix}.mp4 — move it into OUT_DIR
    src = os.path.expanduser(f"~/{prefix}.mp4")
    dst = os.path.join(OUT_DIR, f"s{n}.mp4")
    if os.path.exists(src):
        os.replace(src, dst)
    return True

def main():
    t0 = time.time()
    ok = 0
    for n in sorted(H3P):
        if run(n): ok += 1
    print(f"\nDONE: {ok}/9 scenes rendered in {(time.time()-t0)/60:.1f} min", flush=True)
    # list outputs
    for f in sorted(glob.glob(os.path.join(OUT_DIR, "*.mp4"))):
        print("  ", os.path.basename(f), f"{os.path.getsize(f)/1e6:.1f} MB", flush=True)

if __name__ == "__main__":
    main()
