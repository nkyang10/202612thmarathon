#!/usr/bin/env bash
# Build ATMBKK 2026 CM — 9-scene Hollywood-transition xfade + captions + narration mix.
# Prereq: video/scenes/s1..s9.mp4 (H3 I2V), video/captions/cap01..09.png, video/voice/{whoosh,n1..n6}.mp3
set -euo pipefail
cd "$(dirname "$0")"

DUR=3.2          # per-scene trim (s)  [H3 clips 81f@24fps=3.375s]
FD=0.55          # xfade duration (s)
STEP=$(python3 -c "print($DUR-$FD)")
FPS=24; W=832; H=480
mkdir -p build

# 1) normalize clips
for i in 1 2 3 4 5 6 7 8 9; do
  ffmpeg -y -i scenes/s$i.mp4 -vf "trim=duration=$DUR,scale=$W:$H,setsar=1" \
         -r $FPS -an -c:v libx264 -crf 18 -pix_fmt yuv420p build/s$i.mp4
done

# 2) Hollywood transitions (powerful, cinematic, all implemented in this ffmpeg build)
TRANS=(circlecrop wipeleft radial hblur smoothup diagtr squeezeh fadegrays)
OFFS=()
for i in 1 2 3 4 5 6 7 8; do OFFS+=("$(python3 -c "print($i*$STEP)")"); done

FG="[0:v][1:v]xfade=transition=${TRANS[0]}:duration=$FD:offset=${OFFS[0]}[x1]"
PREV=x1
for i in 2 3 4 5 6 7 8; do
  idx=$((i-1))
  FG="$FG;[${PREV}][$i:v]xfade=transition=${TRANS[$idx]}:duration=$FD:offset=${OFFS[$idx]}[x$i]"
  PREV="x$i"
done
FG="$FG;[${PREV}]format=yuv420p[vout]"

# 3) caption overlays (scene captions cap01-08 + endcard cap09)
# caption timing follows scene windows (DUR=3.2, STEP=2.7):
#   s1:0-3.2 s2:2.7-5.9 s3:5.4-8.6 s4:8.1-11.3 s5:10.8-14 s6:13.5-16.7 s7:16.2-19.4 s8:18.9-22.1 s9:21.6-24.8
CAPS=("0.3,3.0" "3.0,5.6" "5.7,8.3" "8.4,11.0" "11.1,13.7" "13.8,16.4" "16.5,19.1" "19.2,21.8" "21.9,24.8")
# inputs: 0-8 = scenes; 9-17 = captions (cap01..cap09)
OVL="$FG;[vout][9:v]overlay=0:0:enable='between(t,${CAPS[0]})'[c1]"
for i in 2 3 4 5 6 7 8 9; do
  ci=$((i+8))   # caption input index (10..17)
  prev="c$((i-1))"
  OVL="$OVL;[${prev}][${ci}:v]overlay=0:0:enable='between(t,${CAPS[$((i-1))]})'[c$i]"
done
OVL="${OVL};[c9]format=yuv420p[vcap]"

ffmpeg -y -i build/s1.mp4 -i build/s2.mp4 -i build/s3.mp4 -i build/s4.mp4 -i build/s5.mp4 \
       -i build/s6.mp4 -i build/s7.mp4 -i build/s8.mp4 -i build/s9.mp4 \
       -i captions/cap01.png -i captions/cap02.png -i captions/cap03.png -i captions/cap04.png \
       -i captions/cap05.png -i captions/cap06.png -i captions/cap07.png -i captions/cap08.png \
       -i captions/cap09.png \
       -filter_complex "$OVL" -map "[vcap]" -c:v libx264 -crf 18 -r $FPS \
       -aspect 16:9 build/video_captioned.mp4
echo "captioned video built: $(ffprobe -v error -show_entries format=duration -of csv=p=0 build/video_captioned.mp4)s"

# 4) narration + whoosh mix
ffmpeg -y -i build/video_captioned.mp4 \
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
