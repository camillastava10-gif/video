#!/usr/bin/env python3
"""Lager en reel der hooken står på skjermen hele klippet, med kontaktside på slutten.

Eget skript for «Hvordan jeg ... (Med ...)»-reels. Skriptet `lag_reel.py` er laget for
intervjureelen og brukes ikke her. Stil og farger er de samme som i reel-stil.md.

Bruk:
  python3 lag_reel_hook.py kilde.mov reel.mp4 \
      --hook "Hvordan jeg frister hesten til å bli mer smidig" \
      --undertekst "(Med en godbit)" \
      [--start 1.0] [--lengde 27]

Hooken brytes automatisk i linjer, og alle linjene får lik skriftstørrelse (maks 92).
Undertekst skrives på egen linje nederst i samme blokk. Kontaktsiden (3 sek stillbilde)
legges til etter klippet. iPhone-HDR tonemappes til SDR automatisk.
"""
import argparse
import json
import os
import subprocess
import tempfile

from PIL import ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H = 1080, 1920
MAX_TEXT_W = 960      # marg på ca. 60 px på hver side
MAX_SIZE = 92         # samme størrelse som øvrige reels
MIN_SIZE = 64
TOP = 185             # hooken ligger over ørene til hesten
CTA_TOP = 110         # kontaktsiden helt opp mot taket
ENDCARD_SEK = 3
FADE = 0.25

CTA_LINJER = [("Passer det for", 88), ("din hest?", 88),
              ("Send DM eller ring", 80), ("906 51 256", 120)]


def bredde(tekst, size):
    return ImageFont.truetype(FONT, size).getlength(tekst)


def bryt(tekst, size):
    """Bryter teksten i linjer som er smalere enn MAX_TEXT_W."""
    linjer, naa = [], ""
    for ord_ in tekst.split():
        kandidat = f"{naa} {ord_}".strip()
        if bredde(kandidat, size) <= MAX_TEXT_W or not naa:
            naa = kandidat
        else:
            linjer.append(naa)
            naa = ord_
    if naa:
        linjer.append(naa)
    return linjer


def tilpass(hook, undertekst):
    """Største lik størrelse der alt får plass i maks 5 linjer og hvert ord er innenfor bredden."""
    for size in range(MAX_SIZE, MIN_SIZE - 1, -2):
        linjer = bryt(hook, size)
        if undertekst:
            linjer += bryt(undertekst, size)
        if len(linjer) <= 5 and all(bredde(l, size) <= MAX_TEXT_W for l in linjer):
            return size, linjer
    raise SystemExit("Hooken er for lang. Kort den ned.")


def hent_info(kilde):
    ut = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=color_transfer,duration:format=duration",
         "-of", "json", kilde],
        check=True, capture_output=True, text=True).stdout
    d = json.loads(ut)
    stream = d["streams"][0]
    varighet = float(stream.get("duration") or d["format"]["duration"])
    hdr = stream.get("color_transfer") in ("arib-std-b67", "smpte2084")
    return varighet, hdr


def drawtext(path, size, y, start, slutt):
    return (
        f"drawtext=fontfile={FONT}:textfile={path}:fontsize={size}:fontcolor=white:"
        f"borderw=5:bordercolor=black@0.85:shadowx=2:shadowy=3:shadowcolor=black@0.5:"
        f"x=(w-text_w)/2:y={y}:enable='between(t,{start},{slutt})':"
        f"alpha='if(lt(t,{start + FADE}),(t-{start})/{FADE},1)'"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("kilde")
    p.add_argument("ut")
    p.add_argument("--hook", required=True, help="Hovedsetningen, f.eks. «Hvordan jeg frister hesten ...»")
    p.add_argument("--undertekst", default="", help="Parentesen, f.eks. «(Med en godbit)»")
    p.add_argument("--start", type=float, default=1.0, help="Sekunder som klippes bort først (standard 1.0)")
    p.add_argument("--lengde", type=float, default=27.0, help="Maks lengde på selve klippet (standard 27)")
    a = p.parse_args()

    varighet, hdr = hent_info(a.kilde)
    klipp = min(a.lengde, varighet - a.start)
    if klipp <= 0:
        raise SystemExit("Videoen er kortere enn --start.")
    klipp = round(klipp, 2)

    size, linjer = tilpass(a.hook, a.undertekst)
    tmp = tempfile.mkdtemp()
    deler, n = [], 0

    def tekstfil(tekst):
        nonlocal n
        n += 1
        path = os.path.join(tmp, f"t{n}.txt")
        with open(path, "w") as f:
            f.write(tekst)
        return path

    # Hooken står på skjermen hele klippet
    y = TOP
    for linje in linjer:
        deler.append(drawtext(tekstfil(linje), size, y, 0.0, klipp))
        y += int(size * 1.3)

    # Kontaktsiden kommer på stillbildet etter klippet
    y = CTA_TOP
    for linje, s in CTA_LINJER:
        deler.append(drawtext(tekstfil(linje), s, y, klipp, klipp + ENDCARD_SEK))
        y += int(s * 1.3)

    tone = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
            "zscale=t=bt709:m=bt709:r=tv,format=yuv420p," if hdr else "")
    vf = (
        f"{tone}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
        f"format=yuv420p,tpad=stop_mode=clone:stop_duration={ENDCARD_SEK},"
        + ",".join(deler)
    )
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(a.start), "-i", a.kilde, "-vf", vf,
         "-af", f"apad=pad_dur={ENDCARD_SEK}", "-t", str(klipp + ENDCARD_SEK),
         "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", a.ut],
        check=True,
    )
    print(f"Ferdig: {a.ut} ({klipp + ENDCARD_SEK:.1f} sek, tekst {size} pt, HDR={hdr})")


if __name__ == "__main__":
    main()
