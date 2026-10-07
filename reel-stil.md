# Slik vil Camilla ha reelene (Instagram og TikTok)

Sist oppdatert 2026-10-06. Basert på reelen med intervju om leddbehandling (IMG_4008).

## Format
- Stående 1080x1920, ca. 30 sek, H.264 med lyd, SDR (iPhone-video er HDR og må tonemappes).
- Klipp bort første sekund. Legg 3 sek stillbilde på slutten for kontaktinfo.
- Skriptet `lag_reel.py` lager hele reelen på nytt.

## Tekst på video
- **Alle tekstene like store**, ca. 92 punkt (DejaVu Sans Bold), hvit med svart kant og skygge.
- Lange setninger deles på to linjer så de kan være store: «Merket du / noe effekt?».
- Teksten ligger **øverst i bildet** (y ≈ 185), over ørene til hesten, med myk innfading (0,25 sek).
- «Ja!» er større (ca. 190).
- Siste side er større og flyttet **helt opp mot taket** (y ≈ 110): oppfordring, «Send DM eller ring» og telefonnummer i størst skrift.
- Åpning: «4 behandlinger. Hatt effekt?»
- Intervjuspørsmål og svar vises som tekst; svaret om endring: «Mer positiv og arbeidsvillig».

## Innhold og regler
- **Ikke nevn preparatnavn** (det er ikke lov å markedsføre medisiner i Norge). Snakk om behandlingen og hva den gjør.
- **Ikke oppgi pris i posten.** Pris og preparatnavn sendes i DM etterpå (hurtigsvar). Pris oppgis inkl. mva mot privatkunder.
- Kunden må godkjenne video og tekster før posting. Camilla sender den selv.
- Oppfordring til handling: «Passer det for din hest? Send DM eller ring», med telefon 906 51 256.
- **Bildetekst (godkjent av Camilla, bruk akkurat denne):**

```
Passer det for din hest? 🐴

Fire behandlinger senere merker Katelyn stor forskjell på Après du Seigneur. Hun forteller selv hvordan han forandret seg. Se videoen!

Send meg en DM eller ring 906 51 256 hvis du vil vite mer.

#hestehelse #leddhelse #hest #hestevelferd #hesteliv
```

  Bildeteksten har aldri preparatnavn eller pris. Gjelder Instagram, TikTok og Facebook.
- **Første melding i DM (automatisk svar i Meta Business Suite, «Automatisk svar»; godkjent av Camilla, bruk akkurat denne):**

```
Hei! Så gøy at du er interessert! 😊 Behandlingen heter Osteopen: fire injeksjoner med 5–7 dagers mellomrom. Den beskytter leddbrusken, forbedrer leddvæsken og demper betennelsen i leddene. Pris: 1 875 kr per injeksjon, 7 500 kr for hele serien (inkl. mva). Hesten må være nylig undersøkt av veterinær først så andre årsaker er utelukket. Ring meg gjerne: 906 51 256
```

  Den har navn og pris, og er kortet ned (ca. 360 tegn) fordi feltet har tegnbegrensning. Camilla har valgt dette selv.

## Oppfølging av kunder som ikke har svart (Camilla sin tone)
- Camilla følger opp **én gang**, kort og vennlig. Ikke press, ikke rabatt, ikke «fikk du lest meldingen?» når kunden har sett den.
- Spør om hesten, ikke om meldingen, og tilby spørsmål her eller på telefon.
- Ikke legg til «si fra hvis du vil jeg skal komme og se på henne» eller lignende salgspress. Camilla synes det er for pushy og ikke hennes tone.
- Godkjent eksempel (brukt til Monica, Sveio):

```
Hei Monica! 😊 Jeg tenkte jeg skulle høre hvordan det går med hoppa. Har du spørsmål om behandlingen eller noe du lurer på, svarer jeg gjerne her eller på telefon, 906 51 256 🐴
```

## Annet
- Camilla har lite lagringsplass på telefonen: ikke send mange mellomversjoner, rydd gamle filer.

## Reels med «Hvordan jeg ...»-hook (Sofie-vinkel, godbiter/strekk)
- Eget skript: `lag_reel_hook.py` (ikke `lag_reel.py`, som kun er for intervjureelen om leddbehandling).
- Hooken står på skjermen hele klippet, øverst, samme stil som over. Alle linjer er like store (maks 92 pt, krymper automatisk hvis hooken er lang). Parentesen kommer på egen linje nederst i blokken.
- Kontaktsiden (3 sek stillbilde) legges til etter klippet, helt oppe mot taket med 906 51 256.
- Bruk: `python3 lag_reel_hook.py kilde.mov reel.mp4 --hook "Hvordan jeg frister hesten til å bli mer smidig" --undertekst "(Med en godbit)"`
- Ordvalg: «frister» eller «lokker» (positivt og lekent). Ikke «bestikker».
- Flere klipp i én reel (intro + strekk): `python3 lag_reel_hook.py --kilde a.mov --trim 0.4-7.4 --kilde b.mov --trim 0.5-10.5 --ut reel.mp4 --hook "..." --undertekst "(...)"`. Klippene settes sammen i rekkefølge, lyden følger med.
- Komprimering er crf 27 (ca. 17 MB for 30 sek), fordi Camilla har lite lagringsplass.
- Første reel laget med dette: «Hvordan jeg lokker hesten til å bli mer smidig (Med en godbit)», intro + «out to left» + «to left but».
- Tekst nederst (Camilla vil ikke ha den over ansikt og hest): `--hook-y 1290 --cta-y 1240 --maks-size 84`. `--stum 3` tar bort lyden i klipp nummer 3. Siste utgave av første reel: intro + «out to left» + «to left but» (0.5-6.2, uten lyd fordi mannen snakker), 25,7 sek.
