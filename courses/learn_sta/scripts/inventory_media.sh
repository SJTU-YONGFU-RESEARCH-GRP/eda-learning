#!/usr/bin/env bash
cd /mnt/d/proj/designs/eda_learning/courses/learn_sta
for m in module*; do
  flags=""
  test -f "$m/slides.pptx" && flags="$flags pptx"
  test -f "$m/slides.pdf" && flags="$flags pdf"
  test -f "$m/audio/full.mp3" && flags="$flags mp3"
  test -f "$m/video.mp4" && flags="$flags mp4"
  echo "$m:$flags"
done
