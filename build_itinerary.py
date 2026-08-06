#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ATMBKK 2026 race-tour itinerary PDF (A4, tasteful Thai-inspired palette)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- palette ----
CREAM   = HexColor("#f7f4ef")
INK     = HexColor("#2b2a26")
GREEN   = HexColor("#3e5c4b")
GREEN_S = HexColor("#5b7a67")
TERRA   = HexColor("#c05f3c")
GOLD    = HexColor("#c9a35a")
LINE    = HexColor("#ddd5c7")

# ---- fonts ----
pdfmetrics.registerFont(TTFont("wqy", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"))
pdfmetrics.registerFont(TTFont("wqyB", "/usr/share/fonts/truetype/arphic/ukai.ttc"))

OUT = os.path.join(HERE, "downloads", "itinerary.pdf")

def para(txt, size=10.5, color=INK, font="wqy", leading=None, align=0, space=4):
    return Paragraph(txt, ParagraphStyle("p", fontName=font, fontSize=size,
                                         textColor=color, leading=leading or size*1.6,
                                         alignment=align, spaceAfter=space))

def h1(txt):
    return Paragraph(txt, ParagraphStyle("h1", fontName="wqyB", fontSize=22,
                                         textColor=GREEN, leading=30, spaceAfter=6))

def h2(txt, color=GREEN):
    return Paragraph(txt, ParagraphStyle("h2", fontName="wqyB", fontSize=14,
                                         textColor=color, leading=22, spaceBefore=12, spaceAfter=6))

def spacer(h=6):
    return Spacer(1, h)

def rule(color=LINE, w=0.8):
    return HRFlowable(width="100%", thickness=w, color=color, spaceBefore=6, spaceAfter=6)

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=18*mm, rightMargin=18*mm,
                        topMargin=16*mm, bottomMargin=16*mm,
                        title="曼谷快閃雙馬 2026 行程", author="ATMBKK 跑旅企劃")

S = []
# ---- cover ----
S.append(Spacer(1, 6*mm))
S.append(h1("Amazing Thailand Marathon Bangkok 2026"))
S.append(para("「曼谷快閃雙馬」跑旅企劃 · 4日3夜", size=13, color=TERRA, font="wqyB", space=14))
S.append(rule(TERRA, 1.4))
S.append(para("<b>一個週末，兩場馬拉松</b> — 星期六 21K 半馬（04:00）+ 星期日 42K 全馬（02:00）", font="wqyB", size=11.5, color=GREEN))
S.append(para("日期：2026年11月27日（五）– 11月30日（一）　·　模式：星期五晚放工後飛，星期一晚返港，只請 1 日假", size=10))
S.append(para("曼谷比香港慢 1 小時（BKK UTC+7 / HKT UTC+8）", size=9, color=GREEN_S))
S.append(spacer(4))

# ---- trip summary table ----
S.append(h2("基本資料"))
summary = [
    ["項目", "資料"],
    ["賽事", "Amazing Thailand Marathon Bangkok 2026（ATMBKK）第9屆 · 世界田徑認證"],
    ["日期", "11/28（六）21K @04:00 ／ 11/29（日）42K @02:00・10K・4.5K"],
    ["起終點", "Sanam Luang 皇家田廣場（21K 起點：MBK 中心）"],
    ["去程航班", "UO734  HKG→BKK  21:40→23:40  （HK$879）"],
    ["返程航班", "UO703  BKK→HKG  19:45→23:40  （HK$935）"],
    ["住宿", "Phra Nakhon / Khao San 一帶（步行 10–15 分鐘到起點）"],
]
t = Table(summary, colWidths=[30*mm, 134*mm])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),GREEN),
    ("TEXTCOLOR",(0,0),(-1,0),HexColor("#ffffff")),
    ("FONTNAME",(0,0),(-1,0),"wqyB"),
    ("FONTSIZE",(0,0),(-1,0),9.5),
    ("FONTNAME",(0,1),(-1,-1),"wqy"),
    ("FONTSIZE",(0,1),(-1,-1),9),
    ("TEXTCOLOR",(0,1),(0,-1),GREEN),
    ("TEXTCOLOR",(1,1),(1,-1),INK),
    ("GRID",(0,0),(-1,-1),0.5,LINE),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),8),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[HexColor("#ffffff"), CREAM]),
]))
S.append(t)

# ---- day by day ----
S.append(h2("每日行程"))

def day_block(title, color, rows):
    block = [Paragraph(title, ParagraphStyle("dt", fontName="wqyB", fontSize=11.5,
                                             textColor=color, leading=18, spaceBefore=8, spaceAfter=4))]
    tt = Table([[r[0], r[1]] for r in rows], colWidths=[26*mm, 138*mm])
    tt.setStyle(TableStyle([
        ("FONTNAME",(0,0),(-1,-1),"wqy"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("TEXTCOLOR",(0,0),(0,-1),TERRA),
        ("TEXTCOLOR",(1,0),(1,-1),INK),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LINEBELOW",(0,-1),(-1,-1),0.3,LINE),
    ]))
    block.append(tt)
    return block

S += day_block("星期五 27/11 — 放工快閃出發", GOLD, [
    ["18:30","香港收工，直接去機場（建議 19:30 前到 HKG）"],
    ["21:40","UO734 起飛（直航 2 小時）"],
    ["23:40","抵曼谷素萬那普機場 → 通關 → 酒店"],
    ["01:00","抵酒店・宵夜・早抖（聽日 04:00 起步）"],
])
S += day_block("星期六 28/11 — 半馬日 + 慢活", TERRA, [
    ["02:00","起身・輕量早餐・整裝"],
    ["03:00","步行去 MBK 中心起點（Phaya Thai 路）"],
    ["04:00","21K 半馬起步（時限 3.5 小時）"],
    ["08:00","完賽（終點 Sanam Luang）→ 泰式完賽早餐"],
    ["09:30","回酒店沖涼休息"],
    ["11:00","輕遊：大皇宮一帶 / 河畔（量力而行）"],
    ["14:00","泰式按摩放鬆"],
    ["16:00","Expo 領取/補領物品・買紀念品"],
    ["19:00","夜市晚餐（考山路）"],
    ["21:00","早睡備戰（聽日 02:00 起步）"],
])
S += day_block("星期日 29/11 — 全馬日（主菜）", GREEN, [
    ["00:30","起身・食碳水面・整裝"],
    ["01:00","步行去 Sanam Luang 起點（最高法院對出）"],
    ["02:00","42K 全馬起步（時限 7 小時）"],
    ["09:00","完賽（目標）→ 泰式盛宴慶功"],
    ["10:30","回酒店好好休息"],
    ["14:00","賽後慶功午餐（泰菜）"],
    ["16:00","輕鬆遊覽 / 購物（河畔夜市 / CentralWorld）"],
    ["20:00","晚餐・早抖"],
])
S += day_block("星期一 30/11 — 輕鬆半日 + 返港", GOLD, [
    ["08:30","早餐・check-out 寄存行李"],
    ["09:30","大皇宮 / 玉佛寺打卡"],
    ["12:00","午餐 + 最後購物（手信）"],
    ["16:00","回酒店取行李 → 去機場"],
    ["17:00","抵素萬那普機場（國際線 3 小時前到）"],
    ["19:45","UO703 起飛"],
    ["23:40","返抵香港"],
])

# ---- cost ----
S.append(h2("成本預算（每人・雙馬連報）"))
cost = [
    ["項目", "金額"],
    ["機票來回（UO734 + UO703 直航）", "~HK$1,814"],
    ["住宿 3 晚（近起點經濟之選）", "~HK$180–210"],
    ["報名費 42K 全馬（Regular）", "฿1,600 ≈ HK$350"],
    ["報名費 21K 半馬（Regular）", "฿1,400 ≈ HK$308"],
    ["交通 / 膳食 / 按摩 / 雜費", "~HK$1,100"],
    ["總計", "~HK$3,700"],
]
ct = Table(cost, colWidths=[100*mm, 64*mm])
ct.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),GREEN),
    ("TEXTCOLOR",(0,0),(-1,0),HexColor("#ffffff")),
    ("FONTNAME",(0,0),(-1,0),"wqyB"),
    ("FONTSIZE",(0,0),(-1,0),9.5),
    ("FONTNAME",(0,1),(-1,-1),"wqy"),
    ("FONTSIZE",(0,1),(-1,-1),9),
    ("TEXTCOLOR",(0,1),(0,-1),INK),
    ("TEXTCOLOR",(1,1),(1,-1),INK),
    ("ALIGN",(1,1),(1,-1),"RIGHT"),
    ("GRID",(0,0),(-1,-1),0.5,LINE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[HexColor("#ffffff"), CREAM]),
    ("BACKGROUND",(0,-1),(-1,-1),CREAM),
    ("FONTNAME",(0,-1),(-1,-1),"wqyB"),
    ("TOPPADDING",(0,0),(-1,-1),5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
S.append(ct)
S.append(para("※ 泰銖兌港元約 ฿1 ≈ HK$0.22。價錢會浮動，建議提早 booking + 早鳥報名慳更多。", size=8.5, color=GREEN_S))

# ---- notes ----
S.append(h2("報名貼士"))
S += [para("• 報名：amazingthailandmarathon.com，2026年7月3日–10月31日，早鳥最抵。"),
      para("• 一個 email 只可報一個距離 — 要報 21K + 42K 雙馬，要用兩個不同 email。"),
      para("• BIB 必須親身（或授權）到 Expo 領取（11/26–28 @ 詩麗吉皇后國家會議中心），不設郵寄。"),
      para("• 香港護照免簽證；泰銖現金 + 信用卡並用。"),
      para("• 11月底曼谷乾季開始，凌晨約 24–27°C，賽事凌晨起步相對涼爽。")]

doc.build(S)
print("PDF written:", OUT, os.path.getsize(OUT), "bytes")
