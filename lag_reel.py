#!/usr/bin/env python3
"""Lager reelen med tekst over bildet. Krever ffmpeg med zscale, drawtext og libx264.

Bruk: python3 lag_reel.py kilde.mov reel.mp4
Tidene i `items` er sekunder etter at første sekund er klippet bort.
"""
import subprocess
import sys
import tempfile
import os

SRC, OUT = sys.argv[1], sys.argv[2]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
S = 92  # lik størrelse på all tekst
TOP = 185

# (start, slutt, y, [(tekst, skriftstørrelse)])
items = [
    (0.0, 3.8, TOP, [("4 behandlinger.", S), ("Hatt effekt?", S)]),
    (4.0, 7.8, TOP, [("Merket du", S), ("noe effekt?", S)]),
    (8.0, 11.8, TOP, [("Ja, mye", S)]),
    (12.4, 15.2, TOP, [("Og hva har", S), ("endret seg?", S)]),
    (15.5, 19.2, TOP, [("Mer positiv", S), ("og arbeidsvillig", S)]),
    (20.2, 24.7, TOP, [("Verdt", S), ("investeringen?", S)]),
    (25.0, 26.6, TOP, [("Ja!", 190)]),
    (26.6, 29.6, 110, [("Passer det for", 88), ("din hest?", 88),
                       ("Send DM eller ring", 80), ("906 51 256", 120)]),
]

tmp = tempfile.mkdtemp()
parts = []
n = 0
for start, end, y, lines in items:
    for text, size in lines:
        n += 1
        path = os.path.join(tmp, f"t{n}.txt")
        with open(path, "w") as f:
            f.write(text)
        parts.append(
            f"drawtext=fontfile={FONT}:textfile={path}:fontsize={size}:fontcolor=white:"
            f"borderw=5:bordercolor=black@0.85:shadowx=2:shadowy=3:shadowcolor=black@0.5:"
            f"x=(w-text_w)/2:y={y}:enable='between(t,{start},{end})':"
            f"alpha='if(lt(t,{start + 0.25}),(t-{start})/0.25,1)'"
        )
        y += int(size * 1.3)

vf = (
    "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
    "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,tpad=stop_mode=clone:stop_duration=3,"
    + ",".join(parts)
)
subprocess.run(
    ["ffmpeg", "-y", "-ss", "1.0", "-i", SRC, "-vf", vf, "-af", "apad=pad_dur=3", "-t", "29.6",
     "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
     "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
     "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", OUT],
    check=True,
)
