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
S.append(para("「曼谷親子快閃跑」跑旅企劃 · 3日3夜", size=13, color=TERRA, font="wqyB", space=14))
S.append(rule(TERRA, 1.4))
S.append(para("<b>4.5K 親子跑</b> — 星期日 06:45 起步，唔計時、行+跑都得，一家大細一齊玩", font="wqyB", size=11.5, color=GREEN))
S.append(para("日期：2026年11月27日（五）– 11月30日（一）　·　模式：星期五晚放工後飛，星期一晚返港，只請 1 日假", size=10))
S.append(para("曼谷比香港慢 1 小時（BKK UTC+7 / HKT UTC+8）", size=9, color=GREEN_S))
S.append(spacer(4))

# ---- trip summary table ----
S.append(h2("基本資料"))
summary = [
    ["項目", "資料"],
    ["賽事", "Amazing Thailand Marathon Bangkok 2026（ATMBKK）第9屆 · 世界田徑認證"],
    ["主賽事", "4.5K 親子跑 — 11/29（日）06:45 @ Sanam Luang（1小時時限・唔計時）"],
    ["起終點", "Sanam Luang 皇家田廣場"],
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
    ["01:00","抵酒店・宵夜・早抖"],
])
S += day_block("星期六 28/11 — 玩樂日", TERRA, [
    ["09:00","慢活起身・早餐"],
    ["10:00","大皇宮 / 玉佛寺（曼谷必去打卡）"],
    ["13:00","午餐（泰菜）"],
    ["14:30","河畔散步 / 乘船遊昭披耶河"],
    ["16:00","Expo 領取 BIB・買紀念品"],
    ["18:00","泰式按摩放鬆"],
    ["19:30","夜市晚餐（考山路）"],
    ["21:30","早抖（聽日 06:45 起步）"],
])
S += day_block("星期日 29/11 — 4.5K 親子跑日", GREEN, [
    ["05:00","起身・輕量早餐・整裝"],
    ["05:45","步行去 Sanam Luang 起點"],
    ["06:45","4.5K 親子跑起步（時限 1 小時・行+跑）"],
    ["08:00","一家衝線 → 泰式完賽盛宴"],
    ["09:30","回酒店沖涼休息"],
    ["11:00","輕鬆遊覽：河畔 / 寺廟 / 購物"],
    ["14:00","賽後慶功午餐（泰菜）"],
    ["16:00","自由時間：按摩 / 購物 / 河畔夜市"],
    ["20:00","晚餐・早抖"],
])
S += day_block("星期一 30/11 — 輕鬆半日 + 返港", GOLD, [
    ["08:30","早餐・check-out 寄存行李"],
    ["09:30","最後購物（手信）"],
    ["12:00","午餐 + 最後景點"],
    ["16:00","回酒店取行李 → 去機場"],
    ["17:00","抵素萬那普機場（國際線 3 小時前到）"],
    ["19:45","UO703 起飛"],
    ["23:40","返抵香港"],
])

# ---- cost ----
S.append(h2("成本預算（每人・4.5K）"))
cost = [
    ["項目", "金額"],
    ["機票來回（UO734 + UO703 直航）", "~HK$1,814"],
    ["住宿 3 晚（近起點經濟之選）", "~HK$180–210"],
    ["報名費 4.5K 親子跑（Regular）", "฿700 ≈ HK$154"],
    ["交通 / 膳食 / 按摩 / 雜費", "~HK$1,100"],
    ["總計", "~HK$3,300"],
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
      para("• 4.5K 親子跑 Regular ฿700（另 +฿50 服務費）；早鳥 ฿650。"),
      para("• 一個 email 只可報一個距離 — 大人想加報 42K / 10K，要用另一個 email。"),
      para("• BIB 必須親身（或授權）到 Expo 領取（11/26–28 @ 詩麗吉皇后國家會議中心），不設郵寄。"),
      para("• 香港護照免簽證；泰銖現金 + 信用卡並用。"),
      para("• 11月底曼谷乾季開始，日間約 29–33°C，清晨約 24–27°C，4.5K 06:45 起步尚算涼爽。")]

doc.build(S)
print("PDF written:", OUT, os.path.getsize(OUT), "bytes")
