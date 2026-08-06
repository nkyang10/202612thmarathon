# CM 影片分鏡 — 「曼谷親子快閃跑」2026（4.5K 親子跑版本）

**目標**：15–20 秒短 CM，親子跑旅宣傳。MiniMax H3 I2V（native 音效）+ ffmpeg xfade 接駁 + 旁白。

**風格基調**：溫暖親子 + 泰式紅金、都市→晨光過渡、運動感、繽紛歡樂。主角係一家大細。

**統一意象**：紅色/金色調、曼谷天際線 + 大皇宮剪影、一家大細跑步剪影、泰式美食。全程用全新生成素材（唔重用舊 CM）。

---

## 分鏡（9 幕 · 每幕 ~2.2s）

### S1 — 開場：曼谷親子週末覺醒
- **畫面**：曼谷天際線日出，一家大細喺前景熱身、開心準備親子跑
- **Motion (EN)**：slow warm push toward a happy family stretching at dawn in Bangkok, city skyline glowing, gentle golden light, joyful mood
- **Audio**：whoosh + 清晨鳥鳴環境
- **字幕**：一家大細・跑入曼谷

### S2 — 4.5K 親子跑起步（週日 06:45）
- **畫面**：Sanam Luang 前繽紛親子起步線，氣球彩帶，大人細路一齊
- **Motion**：families with kids at a colorful fun run start line, balloons and ribbons, cheerful festive morning
- **Audio**：歡呼 + 彩帶聲
- **字幕**：4.5K 親子跑・06:45

### S3 — 親子沿途・曼谷地標
- **畫面**：一家大細跑過大皇宮金頂，細路開心跳住跑，旁觀打氣
- **Motion**：family running together past golden Grand Palace spires, kids running happily, spectators cheering
- **Audio**：腳步聲 + 打氣聲
- **字幕**：跑入曼谷心臟

### S4 — 一家衝線
- **畫面**：一家大細一齊衝過終點線，彩帶，拎住獎牌慶祝
- **Motion**：family crossing the finish line together, confetti falling, celebrating with medals, joyful smiles
- **Audio**：慶祝歡呼
- **字幕**：一家一齊衝線

### S5 — 完賽泰式盛宴
- **畫面**：一家人食泰式完賽盛宴（芒果糯米飯/冬陰功）
- **Motion**：family enjoying Thai food celebration after the run, mango sticky rice, happy together
- **Audio**：輕快泰式音樂
- **字幕**：衝線即刻泰式大餐

### S6 — 請1放4・快閃曼谷
- **畫面**：週一輕鬆，一家喺大皇宮/河畔打卡、購物
- **Motion**：family sightseeing at Grand Palace and river, relaxed holiday, golden afternoon
- **Audio**：輕快悠閒音樂
- **字幕**：請1日假・快閃4日

### S7 — 曼谷夜市親子時光
- **畫面**：一家行夜市，繽紛攤檔、暖燈、街頭小食
- **Motion**：family strolling through a lively Bangkok night market, colorful food stalls, warm lantern light
- **Audio**：夜市人聲 + 音樂
- **字幕**：夜市・美食・親子時光

### S8 — 家庭同樂
- **畫面**：幾組家庭一齊影相，拎住獎牌，夕陽暖光
- **Motion**：group of families posing together at the race, smiling, holding medals, sunset glow
- **Audio**：笑聲 + 溫馨音樂
- **字幕**：大人細路・全家同樂

### S9 — 收尾 CTA
- **畫面**：一家大細剪影跑向金色終點拱門，紅金彩帶，戲劇性背光
- **Motion**：family silhouette running toward golden finish arch, red and gold ribbons, cinematic hero shot
- **Audio**：振奮鼓點 + 彩帶聲
- **字幕**：Amazing Thailand Marathon Bangkok 2026・11.29・報名趁早鳥

---

## 旁白（edge-tts zh-HK-WanLungNeural，粵語 CTA）
```
一家大細，跑入曼谷。
四點五公里親子跑，人人都做到。
首都馬拉松週末，唔使練跑，一齊衝線。
衝線即刻泰式盛宴，請一日假，快閃四日。
Amazing Thailand Marathon Bangkok 2026，
十一月二十九日，報名趁早鳥！
```
*(逐句分段 TTS，記錄 ffprobe 時長，累加做 SRT 字幕 — 沿用 golden sync pattern)*

## 音效層
- 開場 whoosh：`anoisesrc=color=pink → highpass=300,lowpass=5000 + afade`
- 混合注意：旁白 edge-tts 係 24kHz mono；whoosh 32kHz — 喺 input level 用 `-ar 32000 -ac 2` 轉換，filtergraph 內唔好混 rate

## 接駁（ffmpeg xfade chain）
- 每幕 `trim=DUR → scale=832:480 → setsar=1`，`setsar=1` + `-aspect 16:9` 防 DAR 誤讀 4:3
- `xfade=transition=T:duration=FD:offset=i*STEP`，STEP=DUR-FD
- 轉場：fadeblack / slideleft / dissolve / circleopen 交替
- 場景檔：`video/scenes/s1..s9.mp4`（H3 I2V 已含 native audio）

## 待完成
- H3 I2V 9 幕渲染（`video/render_all_h3.py`）→ `video/scenes/s*.mp4`
- edge-tts 旁白分段 + whoosh → `video/voice/`
- `video/build_cm.sh` → `video/CM-曼谷親子快閃跑2026.mp4`
