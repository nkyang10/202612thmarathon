# 曼谷親子快閃跑 2026 — Amazing Thailand Marathon Bangkok 4.5K 跑旅企劃

**4.5K 親子跑，人人都做到。請1日假，快閃3日。**

Amazing Thailand Marathon Bangkok 2026（ATMBKK）第 9 屆跑旅企劃。主推 **4.5K 親子跑**（2026年11月29日 06:45，Sanam Luang，唔計時、行+跑都得）。星期五晚放工後飛，星期一晚返港，只請 1 日假。

## 企劃內容
| 檔案 | 說明 |
|------|------|
| `index.html` | Landing page（GitHub Pages，休閑專業編輯風） |
| `info.html` | 賽事資訊頁（報名/距離/起步時間/天氣/成本） |
| `docs/itinerary.md` | 3日3夜行程詳情 + 成本預算 |
| `downloads/itinerary.pdf` | 行程 PDF（ReportLab 生成） |
| `promo/CM-storyboard.md` | CM 影片分鏡（9幕・4.5K 親子版） |
| `promo/cards/*.png` | 社交宣傳卡片（PIL 生成） |
| `research/promo-strategy.md` | 套票賣點、口號、競品基準 |
| `video/` | CM 場景生成 + H3 I2V 渲染 + build 腳本 |

## 已核實數據
- **賽事**：ATMBKK 2026 第9屆，World Athletics 世界田徑認證，48,000跑手，大使 Eliud Kipchoge，起終點 Sanam Luang 皇家田廣場。
- **主推 4.5K 親子跑**：11/29（日）06:45 起步，1小時時限，唔計時，老少咸宜。
- **報名費**（Regular）：4.5K ฿700（≈HK$154）。報名 2026/7/3–10/31。
- **機票**（trvl 實時，HK Express 直航）：去 UO734 21:40→23:40 HK$879；返 UO703 19:45→23:40 HK$935。
- **住宿**（近起點 Khao San）：HK$59–74/晚。

## 生成/重跑
```bash
python3 build_itinerary.py        # 行程 PDF → downloads/itinerary.pdf
python3 promo/cards/generate_cards.py  # 社交卡片 → promo/cards/
python3 video/render_scenes.py    # 9張場景圖 (z_image_turbo) → video/scenes_frames/
python3 video/render_all_h3.py    # 9幕 H3 I2V (native audio) → video/scenes/
bash video/build_cm.sh            # 接駁 CM → video/CM-*.mp4
```

## 誠實守則
- 報名係公開第一身攞，唔虛構「保證名額」。
- 所有價錢用實時來源核實（amazingthailandmarathon.com + trvl）。
- 4.5K 係親子玩樂跑，唔硬銷成競技賽事。

*賽事資料來源：amazingthailandmarathon.com（2026-08 查證）· 機票/住宿：trvl 實時數據。*
