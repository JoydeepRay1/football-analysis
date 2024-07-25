#!/bin/bash

VIDEO_PATH=$1
OUTPUT_FOLDER=$2
KNOWN_FACE_EMBEDDINGS=$3
KNOWN_FACE_NAMES=$4

# Create necessary directories
mkdir -p $OUTPUT_FOLDER/{frames,detected,faces,heatmaps,actions,reports}

# Step 1: Extract frames
python3 scripts/extract_frames.py $VIDEO_PATH $OUTPUT_FOLDER/frames

# Step 2: Detect players in each frame
for frame in $OUTPUT_FOLDER/frames/*.jpg; do
    python3 scripts/detect_players.py $frame $OUTPUT_FOLDER/detected/$(basename $frame)
done

# Step 3: Recognize faces in each detected frame
for frame in $OUTPUT_FOLDER/detected/*.jpg; do
    python3 scripts/recognize_faces.py $frame $KNOWN_FACE_EMBEDDINGS $KNOWN_FACE_NAMES > $OUTPUT_FOLDER/faces/$(basename $frame .jpg).txt
done

# Step 4: Action recognition
for frame in $OUTPUT_FOLDER/detected/*.jpg; do
    python3 scripts/recognize_actions.py $frame $OUTPUT_FOLDER/actions/$(basename $frame .jpg).txt
done

# Step 5: Generate heatmaps
python3 scripts/generate_heatmaps.py $OUTPUT_FOLDER/frames $OUTPUT_FOLDER/heatmaps

# Step 6: Generate report
python3 scripts/generate_report.py $OUTPUT_FOLDER > $OUTPUT_FOLDER/reports/match_report.txt

