# 曼谷快閃雙馬 2026 — Amazing Thailand Marathon Bangkok 跑旅企劃

**一個週末，兩場馬拉松。請1日假，快閃4日。**

Amazing Thailand Marathon Bangkok 2026（ATMBKK）第 9 屆跑旅企劃。2026年11月28日（六）21K 半馬 + 11月29日（日）42K 全馬。星期五晚放工後飛，星期一晚返港，只請 1 日假。

## 企劃內容
| 檔案 | 說明 |
|------|------|
| `index.html` | Landing page（GitHub Pages，休閑專業編輯風） |
| `info.html` | 賽事資訊頁（報名/距離/起步時間/天氣/成本） |
| `docs/itinerary.md` | 4日3夜行程詳情 + 成本預算 |
| `downloads/itinerary.pdf` | 行程 PDF（ReportLab 生成） |
| `promo/CM-storyboard.md` | CM 影片分鏡（9幕） |
| `promo/cards/*.png` | 社交宣傳卡片（PIL 生成） |
| `research/promo-strategy.md` | 套票賣點、口號、競品基準 |
| `video/` | CM 場景提示詞 + build 腳本（下一階段 H3 I2V 生成） |

## 已核實數據
- **賽事**：ATMBKK 2026 第9屆，World Athletics 世界田徑認證，48,000跑手，大使 Eliud Kipchoge，起終點 Sanam Luang 皇家田廣場，全賽道 Fast & Flat。
- **報名費**（Regular）：42K ฿1,600 / 21K ฿1,400 / 10K ฿900 / 4.5K ฿700（+฿50 服務費）。報名 2026/7/3–10/31。
- **機票**（trvl 實時，HK Express 直航）：去 UO734 21:40→23:40 HK$879；返 UO703 19:45→23:40 HK$935。
- **住宿**（近起點 Khao San）：HK$59–74/晚。

## 生成/重跑
```bash
python3 build_itinerary.py        # 行程 PDF → downloads/itinerary.pdf
python3 promo/cards/generate_cards.py  # 社交卡片 → promo/cards/
```

## 誠實守則
- 報名係公開第一身攞，唔虛構「保證名額」。
- 所有價錢用實時來源核實（amazingthailandmarathon.com + trvl）。
- 雙馬連賽對體能有要求，如實提示「勁人限定」，唔硬銷。

*賽事資料來源：amazingthailandmarathon.com（2026-08 查證）· 機票/住宿：trvl 實時數據。*
