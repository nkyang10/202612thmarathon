#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate promo social cards for ATMBKK 2026 race-tour campaign (1080x1350 IG portrait)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
CREAM   = (247, 244, 239, 255)
INK     = (43, 42, 38, 255)
GREEN   = (62, 92, 75, 255)
GREEN_S = (91, 122, 103, 255)
TERRA   = (192, 95, 60, 255)
GOLD    = (201, 163, 90, 255)
WHITE   = (255, 253, 248, 255)
LINE    = (221, 213, 199, 255)

F_SERIF = "/usr/share/fonts/truetype/arphic/ukai.ttc"
F_SANS  = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def font(path, size):
    return ImageFont.truetype(path, size)

def text_center(draw, cx, y, s, f, fill):
    bbox = draw.textbbox((0, 0), s, font=f)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2, y), s, font=f, fill=fill)

def text_left(draw, x, y, s, f, fill):
    draw.text((x, y), s, font=f, fill=fill)

def divider(draw, cx, y, half=70, color=GOLD, w=4):
    draw.line([(cx - half, y), (cx + half, y)], fill=color, width=w)

def rounded(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def make_card(name, image_path, kicker, title, body, accent=TERRA, img_h=520):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # top image band
    try:
        top = Image.open(image_path).convert("RGB")
        top = top.resize((W, img_h))
        img.paste(top, (0, 0))
        # dark overlay for text legibility over image band
        ov = Image.new("RGBA", (W, img_h), (0, 0, 0, 90))
        img.paste(Image.alpha_composite(top.convert("RGBA"), ov).convert("RGB"), (0, 0))
    except Exception:
        pass
    d = ImageDraw.Draw(img)
    # accent underline below image
    d.rectangle([0, img_h, W, img_h + 10], fill=accent)
    # kicker
    fk = font(F_SANS, 34)
    d.text((70, img_h + 56), kicker, font=fk, fill=accent)
    # title
    ft = font(F_SERIF, 92)
    text_left(d, 70, img_h + 112, title, ft, INK)
    divider(d, 70 + 90, img_h + 112 + 150, half=60, color=GOLD)
    # body lines
    fb = font(F_SANS, 40)
    y = img_h + 300
    for line in body:
        d.text((70, y), line, font=fb, fill=INK)
        y += 62
    # footer strip
    ff = font(F_SANS, 30)
    d.rectangle([0, H - 120, W, H], fill=GREEN)
    d.text((70, H - 92), "AMAZING THAILAND MARATHON BANGKOK 2026", font=ff, fill=WHITE)
    d.text((70, H - 52), "11.28（六）21K ・ 11.29（日）42K ・ 曼谷快閃雙馬跑旅", font=font(F_SANS, 28), fill=(222, 231, 224, 255))
    img.save(os.path.join(OUT, name))
    print("saved", name)

# --- cards ---
make_card("card-announce.png", "assets/hero_cover.jpg", "SAVE THE DATE",
          "曼谷親子快閃跑", ["4.5K 親子跑，人人都做到", "大人細路一齊衝線", "請1日假，快閃4日"],
          accent=TERRA)

make_card("card-races.png", "assets/save1.jpg", "FAMILY RUN",
          "4.5K 親子跑", ["11/29（日）06:45 起步", "唔計時・行+跑都得", "一家人齊齊玩"],
          accent=GREEN, img_h=500)

make_card("card-leave.png", "assets/save6.jpg", "請1放4",
          "快閃4日", ["星期五晚放工飛", "星期六玩足一日", "星期一晚返港・只請 1 日假"],
          accent=GOLD, img_h=500)

make_card("card-value.png", "assets/header.jpg", "抵玩之旅",
          "約HK$3,300", ["機票來回直航 ~HK$1,814", "住宿3晚近起點 ~HK$200", "4.5K報名費 ~HK$154"],
          accent=TERRA, img_h=480)

make_card("card-friends.png", "assets/hero_cover.jpg", "RUN TOGETHER",
          "約埋屋企人", ["爸爸媽媽細路一齊跑", "首都馬拉松週末氛圍", "衝線即刻泰式盛宴慶功"],
          accent=GREEN, img_h=500)

print("done ->", OUT)
