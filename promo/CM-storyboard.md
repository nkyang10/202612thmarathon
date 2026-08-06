# CM 影片分鏡 — 「曼谷快閃雙馬」2026

**目標**：15–20 秒短 CM，跑旅宣傳。MiniMax H3 I2V（native 音效）+ ffmpeg xfade 接駁 + 旁白。

**風格基調**：鮮活熱情（泰式紅金）+ 運動感。都市夜景燈光 + 凌晨晨光過渡，呈現「快閃雙馬」既兩日兩場 + 凌晨起步嘅獨特感。

**統一意象**：紅色/金色調、曼谷天際線 + 大皇宮剪影、跑者剪影、凌晨涼風、泰式美食。全程用全新生成素材（唔重用舊 CM）。

---

## 分鏡（9 幕 · 每幕 ~2.2s）

### S1 — 開場：凌晨曼谷都市覺醒
- **畫面**：曼谷天際線日出前，深藍到橙紅漸變，城市燈光未熄，跑者剪影喺前景熱身
- **Motion (EN)**：slow aerial push toward Bangkok skyline at dawn, runners silhouetted in foreground stretching, city lights glowing, warm red-orange sunrise breaking, no text
- **Audio 線**：whoosh + 鳥鳴/城市漸醒環境聲
- **字幕**：一個週末，兩場馬拉松

### S2 — 星期六 21K 半馬起步（凌晨4點）
- **畫面**：凌晨街道，起跑線人群，號碼布跑手整裝，路燈下涼爽晨霧
- **Motion**：runners at start line at night, steam rising in cool air, race lights, energetic crowd energy, forward tracking behind runners
- **Audio**：起跑槍聲 + 人群歡呼
- **字幕**：星期六 21K・凌晨4點

### S3 — 半馬沿途：曼谷地標
- **畫面**：跑手跑過大皇宮金頂 / 民主紀念碑，紅金建築燈光
- **Motion**：runner passing golden Grand Palace spires at dawn, warm golden light on ornate Thai architecture, camera glides alongside
- **Audio**：腳步聲 + 城市風聲
- **字幕**：跑入曼谷心臟

### S4 — 星期日 42K 全馬（凌晨2點）
- **畫面**：更早凌晨，皇家田廣場前，42K 起步，數千跑手燈海
- **Motion**：huge pack of runners surging under floodlights at 2am, sea of headlamps, monumental scale, low dramatic angle
- **Audio**：低沉心跳節拍 + 人群
- **字幕**：星期日 42K・凌晨2點

### S5 — 平坦快路・破PB
- **畫面**：清晨直路，跑手大步快跑，地平線平直，涼風
- **Motion**：long flat road, runner striding fast in cool morning light, flags and barriers, speed lines, confident pace
- **Audio**：輕快跑步節奏 + 風
- **字幕**：世界田徑認證・平坦快路

### S6 — 衝線・泰式盛宴
- **畫面**：Sanam Luang 終點，衝線帶，然後切泰式美食（冬陰功/芒果糯米飯）盛宴，跑手開心食
- **Motion**：runner crossing finish line, confetti, then a spread of Thai food, joyful celebration, bright warm tones
- **Audio**：歡呼聲 + 泰式音樂
- **字幕**：衝線即刻泰式大餐

### S7 — 放假快閃（請1放4）
- **畫面**：週一輕鬆半日：大皇宮打卡、河畔、購物手信，悠閒
- **Motion**：tourist moments at Grand Palace and river, relaxed sightseeing, golden afternoon, light bokeh
- **Audio**：輕快悠閒音樂
- **字幕**：請1日假・快閃4日

### S8 — 與跑友同行 / 家庭
- **畫面**：跑友群一齊影相、小朋友親子跑，笑容
- **Motion**：group of runner friends celebrating together, family kids running, warm candid shots, sunset glow
- **Audio**：笑聲 + 溫馨音樂
- **字幕**：大人全馬・小朋友親子跑

### S9 — 收尾 CTA
- **畫面**：Kipchoge 式跑手剪影奔向終點線，紅金煙花/彩帶，站標語
- **Motion**：runner silhouette running toward golden finish arch, celebratory ribbons in red and gold, cinematic hero shot, slow motion
- **Audio**：振奮鼓點 + 彩帶聲
- **字幕**：Amazing Thailand Marathon Bangkok 2026・11.28–29・報名趁早鳥

---

## 旁白（edge-tts zh-HK-WanLungNeural，粵語 CTA）
```
一個週末，兩場馬拉松。
星期六半馬，星期日全馬。
世界田徑認證，平坦快路，凌晨起步涼爽破 PB。
衝線即刻泰式盛宴，請一日假，快閃四日。
Amazing Thailand Marathon Bangkok 2026，
十一月二十八、二十九日，報名趁早鳥！
```
*(逐句分段 TTS，記錄 ffprobe 時長，累加做 SRT 字幕 — 沿用 golden sync pattern)*

## 音效層
- 開場 whoosh：`anoisesrc=color=pink → highpass=300,lowpass=5000 + afade`
- 混合注意：旁白 edge-tts 係 24kHz mono；whoosh 32kHz — 喺 input level 用 `-ar 32000 -ac 2` 轉換，filtergraph 內唔好混 rate

## 接駁（ffmpeg xfade chain）
- 每幕 `trim=DUR → scale=832:480 → setsar=1`，`setsar=1` + `-aspect 16:9` 防 DAR 誤讀 4:3
- `xfade=transition=T:duration=FD:offset=i*STEP`，STEP=DUR-FD
- 轉場：fadeblack / slideleft / dissolve / circleopen 交替

## 待生成（下一階段）
- ComfyUI z_image_turbo：9 張 1280×720 場景圖（`video/prompts/s*.txt`）
- MiniMax H3 I2V：9 段 832×480 24fps，每段 ~50-65 frames，native audio
- ffmpeg 接駁 + 旁白 + 字幕 → `video/CM-曼谷快閃雙馬2026.mp4`
