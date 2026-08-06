#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate on-screen caption overlays for the 4.5K family-run CM.
cap01..cap08 = per-scene captions (bottom-center, box+shadow).
cap09 = endcard with full event info (event name, dates, 4.5K, 癡LS Group, CTA).
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 832, 480
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captions")
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
f = ImageFont.truetype(FONT, 26) if os.path.exists(FONT) else ImageFont.load_default()
fb = ImageFont.truetype(FONT, 34) if os.path.exists(FONT) else ImageFont.load_default()   # endcard title

def make_caption(name, text, font=f, box=True):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = 24
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    x = (W - tw)//2; y = H - pad - th
    if box:
        d.rectangle([x-16, y-12, x+tw+16, y+th+14], fill=(15,15,12,150))
    for dx,dy in [(-1,-1),(-1,1),(1,-1),(1,1),(0,-2),(0,2),(2,0),(-2,0)]:
        d.text((x+dx,y+dy), text, font=font, fill=(0,0,0,210))
    d.text((x,y), text, font=font, fill=(255,255,255,255))
    img.save(os.path.join(OUT, name))
    print(name, ":", text)

# ---- scene captions ----
make_caption("cap01.png", "一家大細・跑入曼谷")
make_caption("cap02.png", "4.5K 親子跑・11.29 06:45")
make_caption("cap03.png", "跑入曼谷心臟")
make_caption("cap04.png", "一家一齊衝線")
make_caption("cap05.png", "衝線即刻泰式大餐")
make_caption("cap06.png", "請1日假・快閃3日")
make_caption("cap07.png", "夜市・美食・親子時光")
make_caption("cap08.png", "大人細路・全家同樂")

# ---- endcard (cap09) — full event info over hero finish scene ----
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# dark backdrop strip across bottom
d.rectangle([0, H-190, W, H], fill=(12,10,8,178))
d.line([0, H-190, W, H-190], fill=(214,163,90,255), width=2)
lines = [
    ("Amazing Thailand Marathon Bangkok 2026", 30, (240,214,178,255)),
    ("4.5K 親子跑・11.29（日）", 30, (255,255,255,255)),
    ("一家大細一齊衝線｜請1日假快閃3日", 22, (225,225,218,255)),
    ("癡LS Group 主辦", 26, (214,163,90,255)),
    ("報名趁早鳥｜amazingthailandmarathon.com", 22, (255,255,255,255)),
]
y = H-182
for text, size, color in lines:
    fsize = ImageFont.truetype(FONT, size) if os.path.exists(FONT) else f
    bbox = d.textbbox((0,0), text, font=fsize)
    tw = bbox[2]-bbox[0]
    x = (W-tw)//2
    for dx,dy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        d.text((x+dx,y+dy), text, font=fsize, fill=(0,0,0,210))
    d.text((x,y), text, font=fsize, fill=color)
    y += size + 8
img.save(os.path.join(OUT, "cap09.png"))
print("cap09.png : endcard (event info)")
print("done")
