#!/usr/bin/env bash
# Build ATMBKK 2026 CM — 9-scene xfade + narration mix + captions.
# Prereq: video/scenes/s1..s9.mp4 (H3 I2V), video/voice/n1..n6.mp3 (edge-tts), whoosh.mp3
set -euo pipefail
cd "$(dirname "$0")"

DUR=2.2          # per-scene duration (s)
FD=0.6           # xfade duration (s)
STEP=$(python3 -c "print($DUR-$FD)")   # xfade offset step
FPS=24
W=832; H=480

mkdir -p build
# 1) normalize each clip to 832x480, 16:9
for i in 1 2 3 4 5 6 7 8 9; do
  ffmpeg -y -i scenes/s$i.mp4 -vf "trim=duration=$DUR,scale=$W:$H,setsar=1" \
         -r $FPS -an -c:v libx264 -crf 18 -pix_fmt yuv420p build/s$i.mp4
done

# 2) xfade chain (explicit offsets, reliable)
OFFS=()
for i in 1 2 3 4 5 6 7 8; do
  OFFS+=("$(python3 -c "print($i*$STEP)")")
done
TRANS=(fadeblack slideleft dissolve circleopen fadeblack slideleft dissolve circleopen)

FG="[0:v][1:v]xfade=transition=${TRANS[0]}:duration=$FD:offset=${OFFS[0]}[x1]"
PREV=x1
for i in 2 3 4 5 6 7 8; do
  j=$((i+1))  # input index
  FG="$FG;[${PREV}][$j:v]xfade=transition=${TRANS[$((i-1))]}:duration=$FD:offset=${OFFS[$((i-1))]}[x$j]"
  PREV="x$j"
done
FG="${FG};[${PREV}]format=yuv420p[vout]"

ffmpeg -y -i build/s1.mp4 -i build/s2.mp4 -i build/s3.mp4 -i build/s4.mp4 -i build/s5.mp4 \
       -i build/s6.mp4 -i build/s7.mp4 -i build/s8.mp4 -i build/s9.mp4 \
       -filter_complex "$FG" -map "[vout]" -c:v libx264 -crf 18 -r $FPS \
       -aspect 16:9 build/video_silent.mp4
echo "video base built: build/video_silent.mp4"

# 3) narration + whoosh mix (input-level rate conversion; keep filtergraph simple)
ffmpeg -y -i build/video_silent.mp4 -i voice/whoosh.mp3 -i voice/n1.mp3 -i voice/n2.mp3 \
       -i voice/n3.mp3 -i voice/n4.mp3 -i voice/n5.mp3 -i voice/n6.mp3 \
       -filter_complex "[1:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=0|0,afade=t=in:d=0.4[w];[2:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=200|200,afade=t=in:d=0.2[n1];[3:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=2300|2300[n2];[4:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=4500|4500[n3];[5:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=6700|6700[n4];[6:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=8900|8900[n5];[7:a]aformat=sample_rates=32000:channel_layouts=stereo,adelay=11100|11100[n6];[w][n1][n2][n3][n4][n5][n6]amix=inputs=7:normalize=0,atrim=0:18,afade=t=out:st=16.5:d=1.5[aout]" \
       -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k \
       -aspect 16:9 "CM-曼谷快閃雙馬2026.mp4"
echo "CM built: CM-曼谷快閃雙馬2026.mp4"
