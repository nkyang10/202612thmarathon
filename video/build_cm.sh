#!/usr/bin/env bash
# Build ATMBKK 2026 CM — 9-scene xfade + narration mix (4.5K family run).
# Prereq: video/scenes/s1..s9.mp4 (H3 I2V, ~3.375s each), video/voice/n1..n6.mp3, whoosh.mp3
set -euo pipefail
cd "$(dirname "$0")"

DUR=3.2          # per-scene trim duration (s)  [H3 clips are 81f@24fps=3.375s]
FD=0.5           # xfade duration (s)
STEP=$(python3 -c "print($DUR-$FD)")            # 2.7
FPS=24
W=832; H=480
mkdir -p build

# 1) normalize each clip to 832x480, 16:9, trim to DUR
for i in 1 2 3 4 5 6 7 8 9; do
  ffmpeg -y -i scenes/s$i.mp4 -vf "trim=duration=$DUR,scale=$W:$H,setsar=1" \
         -r $FPS -an -c:v libx264 -crf 18 -pix_fmt yuv420p build/s$i.mp4
done

# 2) xfade chain (explicit offsets)
OFFS=()
for i in 1 2 3 4 5 6 7 8; do OFFS+=("$(python3 -c "print($i*$STEP)")"); done
TRANS=(fadeblack slideleft dissolve circleopen fadeblack slideleft dissolve circleopen)

FG="[0:v][1:v]xfade=transition=${TRANS[0]}:duration=$FD:offset=${OFFS[0]}[x1]"
PREV=x1
for i in 2 3 4 5 6 7 8; do
  idx=$((i-1))
  FG="$FG;[${PREV}][$i:v]xfade=transition=${TRANS[$idx]}:duration=$FD:offset=${OFFS[$idx]}[x$i]"
  PREV="x$i"
done
FG="${FG};[${PREV}]format=yuv420p[vout]"

ffmpeg -y -i build/s1.mp4 -i build/s2.mp4 -i build/s3.mp4 -i build/s4.mp4 -i build/s5.mp4 \
       -i build/s6.mp4 -i build/s7.mp4 -i build/s8.mp4 -i build/s9.mp4 \
       -filter_complex "$FG" -map "[vout]" -c:v libx264 -crf 18 -r $FPS \
       -aspect 16:9 build/video_silent.mp4
echo "video base built: build/video_silent.mp4 ($(ffprobe -v error -show_entries format=duration -of csv=p=0 build/video_silent.mp4)s)"

# 3) narration + whoosh mix (input-level rate conversion; keep filtergraph simple)
ffmpeg -y -i build/video_silent.mp4 \
       -i voice/whoosh.mp3 -i voice/n1.mp3 -i voice/n2.mp3 -i voice/n3.mp3 \
       -i voice/n4.mp3 -i voice/n5.mp3 -i voice/n6.mp3 \
       -filter_complex "\
[1:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=0|0,afade=t=in:d=0.3,afade=t=out:st=0.9:d=0.3[w];\
[2:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=300|300[n1];\
[3:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=3000|3000[n2];\
[4:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=5500|5500[n3];\
[5:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=8500|8500[n4];\
[6:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=15000|15000[n5];\
[7:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=20000|20000[n6];\
[w][n1][n2][n3][n4][n5][n6]amix=inputs=7:normalize=0,atrim=0:25,afade=t=out:st=24:d=1[aout]" \
       -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k \
       -aspect 16:9 "CM-曼谷親子快閃跑2026.mp4"
echo "CM built: CM-曼谷親子快閃跑2026.mp4"
