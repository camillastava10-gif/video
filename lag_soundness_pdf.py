#!/usr/bin/env python3
"""Lager PDF-en «The 5-Minute Soundness Check» (engelsk tekst, til lead magnet i DM).

Teksten står i CONTENT nederst i denne filen. Endre teksten der og kjør på nytt.

Bruk: python3 lag_soundness_pdf.py ut.pdf
"""
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

OUT = sys.argv[1]
ACCENT = colors.HexColor("#2F5D50")
TEXT = colors.HexColor("#222222")
SOFT = colors.HexColor("#EEF3F0")
LINK = "#1F5FAE"

base = ParagraphStyle("base", fontName="Helvetica", fontSize=11.5, leading=16.5, textColor=TEXT,
                      alignment=TA_LEFT, spaceAfter=6)
title = ParagraphStyle("title", parent=base, fontName="Helvetica-Bold", fontSize=28, leading=32,
                       textColor=ACCENT, spaceAfter=4)
sub = ParagraphStyle("sub", parent=base, fontSize=14, leading=18, spaceAfter=2)
by = ParagraphStyle("by", parent=base, fontSize=11, textColor=colors.HexColor("#555555"), spaceAfter=14)
h = ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=15, leading=19,
                   textColor=ACCENT, spaceBefore=12, spaceAfter=4)
em = ParagraphStyle("em", parent=base, fontName="Helvetica-Oblique", fontSize=10.5, leading=15,
                    textColor=colors.HexColor("#444444"))
small = ParagraphStyle("small", parent=base, fontSize=9.5, leading=13.5, textColor=colors.HexColor("#444444"))
bul = ParagraphStyle("bul", parent=base, spaceAfter=2)


def bullets(items, style=bul):
    return ListFlowable([ListItem(Paragraph(t, style), leftIndent=12) for t in items],
                        bulletType="bullet", start="•", leftIndent=14, bulletFontSize=10)


def box(flowables, bg=SOFT):
    t = Table([[flowables]], colWidths=[A4[0] - 40 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def link(text, url):
    return f'<a href="{url}" color="{LINK}"><u>{text}</u></a>'


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(20 * mm, 12 * mm, "The 5-Minute Soundness Check  |  Camilla Stava, veterinarian")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    s = []
    s += [Paragraph("The 5-Minute Soundness Check", title),
          Paragraph("A simple look at your horse before you ride", sub),
          Paragraph("By Camilla Stava, veterinarian", by),
          Paragraph("You do not need special tools. You need level ground, a phone, and 5 minutes. "
                    "Do the check at the same place and time each week, so you can compare.", base)]

    s.append(KeepTogether([Paragraph("Before you start", h), bullets([
        "Your horse wears <b>only a halter and lead rope</b>. No rug, saddle, pad, bandages or boots. "
        "Anything on the body hides what you need to see.",
        "Use level, firm ground.",
        "Have a helper if you can. Handle your horse calmly, and stop if it becomes tense."])]))

    s.append(KeepTogether([Paragraph("Step 1: Stand and photograph", h),
        Paragraph("Let your horse stand naturally. Do not place its legs. Take a photo of the <b>left side</b>, "
                  "the <b>right side</b> and <b>from behind</b>, from the same distance each time, with the "
                  "whole horse in the picture.", base),
        box([Paragraph("<b>Safety</b>", base), bullets([
            "Stay at least 3 meters (10 feet) behind your horse when you photograph from behind. Never stand "
            "directly behind it within kicking distance.",
            "If you want a higher angle, use a low, stable stool on level ground, away from the horse. "
            "Have a helper hold the horse. If your horse is nervous, skip the stool."])]),
        Spacer(1, 6),
        Paragraph("Look at the photos:", base),
        bullets(["Is the weight on all four feet?",
                 "Are the <b>front legs, the hind legs, or both</b> standing further under the body than normal?",
                 "Does it keep shifting weight or holding one leg forward?"])]))

    s.append(KeepTogether([Paragraph("Step 2: Look at the face", h),
        Paragraph("Take a close-up photo of the face from the side and the front. Do it when your horse is calm "
                  "and not eating. Compare it with the relaxed face and pain face pictures in the guide linked "
                  "at the end of this document.", base),
        Paragraph("Look for:", base),
        bullets(["<b>Ears:</b> lowered, or turned back, with a wider gap between the ears at the base",
                 "<b>Eyes:</b> a tense stare, or tension in the muscle above the eye",
                 "<b>Nostrils:</b> dilated, or pulled out to the sides",
                 "<b>Muzzle:</b> lips pressed together, and a flat or edged chin",
                 "<b>Facial muscles:</b> tense",
                 "From Dr. Sue Dyson's ethogram: the white of the eye showing, eyes closed or half closed, "
                 "or the ears held flat"]),
        Spacer(1, 4),
        Paragraph("These scales were made for trained observers, and the pain face was studied in horses with "
                  "mild to moderate acute pain. One sign on its own does not mean your horse is in pain, and a "
                  "normal face does not rule it out. Compare with photos from other days.", em)]))

    s.append(KeepTogether([Paragraph("Step 3: Use your hands", h),
        Paragraph("Run a flat hand along the neck, back and hindquarters. Compare the left and right side.", base),
        bullets(["Does your horse flinch, pin its ears or swish its tail?",
                 "Do you feel <b>heat, swelling or hard muscles anywhere</b>, on either side?"]),
        Spacer(1, 4),
        Paragraph("Use light pressure. This is only to notice, not to treat.", base)]))

    s.append(KeepTogether([Paragraph("Step 4: Watch it walk", h),
        Paragraph("Lead your horse on a straight line on firm, level ground, <b>away from your helper and "
                  "toward your helper</b>. Your helper films the whole horse while you lead.", base),
        bullets(["<b>From the front:</b> Does the head move up or down more on one side than the other?",
                 "<b>From behind:</b> Does one hip rise or drop more than the other?",
                 "Are the steps the same length on both sides?",
                 "Does the rhythm sound and look even, with the same beat on each foot?"]),
        Spacer(1, 4),
        Paragraph("Lameness is often very subtle. Many owners cannot see it until it is bad. Film from the same "
                  "spot each time. You can watch the video several times, also in slow motion.", base)]))

    s.append(KeepTogether([Paragraph("Step 5: Turn and bend", h),
        Paragraph("Turn your horse in a small circle each way, and ask it to follow a treat toward each shoulder.", base),
        bullets(["Is one side stiffer than the other?", "Does it resist or step away?"]),
        Spacer(1, 4),
        Paragraph("If possible, ask your helper to film this step too. Never force it. If your horse resists, "
                  "stop and note it.", base)]))

    s.append(KeepTogether([Paragraph("Keep a journal", h),
        Paragraph("Write down the date, what you saw, and which side. A single odd day tells you very little. Patterns over "
                  "several weeks tell you more.", base)]))

    s.append(KeepTogether([Paragraph("When to call your veterinarian", h), bullets([
        "You see <b>any</b> difference between the left and right side, even a small one",
        "Your horse is stiffer one way, shorter in the stride, or does not want to bend to one side",
        "Heat or swelling in a leg",
        "A sudden change in behavior",
        "The same difference shows up again and again",
        "<b>You are unsure.</b> If something feels off in general, but you cannot say why, contact your "
        "local horse vet."])]))

    s.append(KeepTogether([Paragraph("Learn more about reading your horse's face", h), bullets([
        link("The Equine Pain Face, illustrated guide by Karina Bech Gleerup (Horses and People)",
             "https://horsesandpeople.com.au/the-equine-pain-face/"),
        "Gleerup KB, Forkman B, Lindegaard C, Andersen PH. " +
        link("An equine pain face", "https://pmc.ncbi.nlm.nih.gov/articles/PMC4312484") +
        ". Veterinary Anaesthesia and Analgesia, 2015.",
        "Dyson S, Berger JM, Ellis AD, Mullard J. " +
        link("Development of an ethogram for a pain scoring system in ridden horses",
             "https://doi.org/10.1016/j.jveb.2017.10.008") + ". Journal of Veterinary Behavior, 2018."])]))

    s.append(Spacer(1, 10))
    s.append(KeepTogether([box([
        Paragraph("<b>Important: please read</b>", base),
        Paragraph("This guide is for education and observation only. It is <b>not veterinary advice, diagnosis "
                  "or treatment</b>, and it does not create a veterinarian and client relationship. It cannot "
                  "replace a physical examination by a licensed veterinarian in your country. I cannot see your horse, and "
                  "horses can be in pain without showing it, so seeing nothing does not mean your horse is "
                  "healthy.", small),
        Paragraph("Lameness can be very subtle, and many owners cannot see it. This check cannot rule out "
                  "lameness or pain, so seeing nothing does not mean your horse is sound.", small),
        Paragraph("Complementary methods are a supplement to conventional veterinary medicine, never a "
                  "replacement. No result is promised or guaranteed.", small),
        Paragraph("If your horse is lame, injured, or you are worried, contact your own veterinarian at once. "
                  "You carry out this check at your own risk. Horses are large animals and can be "
                  "unpredictable, so use caution and ask for help. To the extent permitted by law, Camilla "
                  "Stava is not responsible for injury, loss or damage resulting from use of this guide.",
                  small)]), Spacer(1, 10),
        Paragraph("<b>Questions? Reply here.</b>", base)]))
    return s


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                        bottomMargin=20 * mm, title="The 5-Minute Soundness Check", author="Camilla Stava")
doc.build(build(), onFirstPage=footer, onLaterPages=footer)
print("Ferdig:", OUT)
