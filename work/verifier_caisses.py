# -*- coding: utf-8 -*-
"""Contrôles automatiques de la plaquette caisses enregistreuses tactiles."""
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "Plaquette HelloLead - Caisses enregistreuses tactiles.pdf"

FORBIDDEN = re.compile(
    r"solaire|photovolta|toiture|kWh|kWc|surplus|autoconsommation|panneaux", re.I)


def main():
    doc = pymupdf.open(PDF)
    errors = []

    if doc.page_count != 9:
        errors.append(f"nombre de pages : {doc.page_count} (attendu 9)")

    for page in doc:
        no = page.number + 1
        if abs(page.rect.width - 1440) > 0.5 or abs(page.rect.height - 810) > 0.5:
            errors.append(f"p.{no} : format {page.rect}")
        if page.get_links():
            errors.append(f"p.{no} : {len(page.get_links())} lien(s) résiduel(s)")
        for m in FORBIDDEN.finditer(page.get_text()):
            ctx = page.get_text()[max(0, m.start() - 30):m.end() + 30]
            errors.append(f"p.{no} : terme solaire « {m.group()} » ({ctx!r})")
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 < -1 or y0 < -1 or x1 > 1441 or y1 > 811:
                        errors.append(f"p.{no} : texte hors page {span['text']!r}")
                    if x0 > 1065 and x1 > 1397:
                        errors.append(f"p.{no} : texte hors panneau droit "
                                      f"{span['text']!r}")

    if "Caisses enregistreuses tactiles" not in doc.metadata.get("title", ""):
        errors.append(f"titre PDF inattendu : {doc.metadata.get('title')!r}")

    for page in doc:
        for font in page.get_fonts():
            if "Poppins" not in font[3] and "OpenSans" not in font[3] \
                    and "DejaVu" not in font[3]:
                errors.append(f"p.{page.number + 1} : police inattendue {font[3]}")

    if errors:
        print("ÉCHEC —", len(errors), "anomalie(s)")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    size_mb = PDF.stat().st_size / 1024 / 1024
    print(f"OK — {doc.page_count} pages, {size_mb:.1f} Mo, "
          "aucun terme solaire, aucun lien, textes dans les cadres, polices conformes.")


if __name__ == "__main__":
    main()
