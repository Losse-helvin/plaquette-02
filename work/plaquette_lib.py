# -*- coding: utf-8 -*-
"""Petit moteur de mise en page pour les plaquettes HelloLead."""
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT
GEN = ROOT / "gen"
GEN.mkdir(exist_ok=True)

W, H = 1440.0, 810.0
BLUE = "#0A5BFF"
PALE = "#F4F5FB"
GREY_TITLE = "#737373"
BLACK = "#000000"
MUTED = "#5F6B7A"
LIGHT_LINE = "#E3E6EF"
NAVY = "#1B3A57"

FONT_FILES = {
    "PR": "Poppins-Regular.ttf",
    "PM": "Poppins-Medium.ttf",
    "PS": "Poppins-SemiBold.ttf",
    "PB": "Poppins-Bold.ttf",
    "PE": "Poppins-ExtraBold.ttf",
}
FONTS = {k: pymupdf.Font(fontfile=str(ASSETS / v)) for k, v in FONT_FILES.items()}


def hexc(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def text_width(s, font, size):
    return FONTS[font].text_length(s, fontsize=size)


def wrap(s, font, size, width):
    """Découpe un texte en lignes qui tiennent dans `width`."""
    out = []
    for para in s.split("\n"):
        words = para.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for wd in words[1:]:
            trial = line + " " + wd
            if text_width(trial, font, size) <= width:
                line = trial
            else:
                out.append(line)
                line = wd
        out.append(line)
    return out


def draw_text(page, x, top, s, font="PR", size=14, color=BLACK, width=None):
    """Écrit `s` en alignant le haut du texte sur `top` (et non la ligne de base)."""
    f = FONTS[font]
    baseline = top + f.ascender * size
    if width is not None:
        # réduction automatique si le mot est trop large
        while s and text_width(s, font, size) > width and size > 4:
            size -= 0.2
        baseline = top + f.ascender * size
    page.insert_text((x, baseline), s, fontname=font, fontsize=size, color=hexc(color))
    return size


def text_center(page, cx, top, s, font="PR", size=14, color=BLACK):
    page.insert_text((cx - text_width(s, font, size) / 2.0,
                      top + FONTS[font].ascender * size),
                     s, fontname=font, fontsize=size, color=hexc(color))


def text_right(page, rx, top, s, font="PR", size=14, color=BLACK):
    page.insert_text((rx - text_width(s, font, size),
                      top + FONTS[font].ascender * size),
                     s, fontname=font, fontsize=size, color=hexc(color))


def _rf(rect_, radius):
    """PyMuPDF attend un rayon relatif (0 < r <= 0.5) ; on raisonne en points."""
    if not radius:
        return None
    w, h = abs(rect_[2] - rect_[0]), abs(rect_[3] - rect_[1])
    return min(0.5, radius / max(1.0, min(w, h)))


def panel(page, rect, fill=PALE, radius=22, opacity=1.0):
    page.draw_rect(pymupdf.Rect(*rect), color=None, fill=hexc(fill),
                   radius=_rf(rect, radius), fill_opacity=opacity)


def shadow(page, rect, radius=10, offset=4, opacity=0.10):
    r = pymupdf.Rect(rect[0], rect[1] + offset, rect[2], rect[3] + offset)
    page.draw_rect(r, color=None, fill=(0.1, 0.15, 0.25), radius=_rf(rect, radius),
                   fill_opacity=opacity)


def card(page, rect, radius=10, fill="#FFFFFF", with_shadow=True, border=None):
    if with_shadow:
        shadow(page, rect, radius=radius)
    page.draw_rect(pymupdf.Rect(*rect), color=hexc(border) if border else None,
                   fill=hexc(fill), radius=_rf(rect, radius),
                   width=0.8 if border else 0.5, fill_opacity=1.0)


def rect(page, rect_, fill=None, color=None, width=1, radius=0):
    page.draw_rect(pymupdf.Rect(*rect_), color=hexc(color) if color else None,
                   fill=hexc(fill) if fill else None, width=width,
                   radius=_rf(rect_, radius))


def circle(page, center, r, fill=None, color=None, width=1):
    page.draw_circle(pymupdf.Point(*center), r,
                     fill=hexc(fill) if isinstance(fill, str) else fill,
                     color=hexc(color) if isinstance(color, str) else color,
                     width=width)


def line(page, p1, p2, color=LIGHT_LINE, width=1):
    page.draw_line(pymupdf.Point(*p1), pymupdf.Point(*p2),
                   color=hexc(color), width=width)


def pill(page, rect_, s, fill=BLUE, color="#FFFFFF", font="PS", size=9):
    page.draw_rect(pymupdf.Rect(*rect_), color=None, fill=hexc(fill),
                   radius=0.5)
    text_center(page, (rect_[0] + rect_[2]) / 2.0,
                (rect_[1] + rect_[3]) / 2.0 - size * 0.72, s, font, size, color)


def _cover_crop(im, ratio):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / ratio)
        top = int((h - nh) * 0.35)
        im = im.crop((0, top, w, top + nh))
    return im


_img_cache = {}


def rounded_image(path, w_pt, h_pt, radius=0, corners=None, dpi=2.2,
                  crop_ratio=None):
    """Renvoie un PNG prêt à insérer (coins arrondis, ratio respecté)."""
    key = (str(path), round(w_pt, 1), round(h_pt, 1), radius,
           tuple(corners) if corners else None)
    if key in _img_cache:
        return _img_cache[key]
    im = Image.open(path).convert("RGB")
    ratio = crop_ratio or (w_pt / h_pt)
    im = _cover_crop(im, ratio)
    px_w = max(2, int(w_pt * dpi))
    px_h = max(2, int(h_pt * dpi))
    im = im.resize((px_w, px_h), Image.LANCZOS)
    if radius or corners:
        mask = Image.new("L", (px_w, px_h), 0)
        d = ImageDraw.Draw(mask)
        r = int(radius * dpi)
        if corners is None:
            d.rounded_rectangle([0, 0, px_w - 1, px_h - 1], radius=r, fill=255)
        else:
            # corners = (haut-gauche, haut-droit, bas-droit, bas-gauche)
            d.rectangle([r, 0, px_w - r, px_h], fill=255)
            d.rectangle([0, r, px_w, px_h - r], fill=255)
            c = corners
            for on, box in zip(c, [
                [0, 0, 2 * r, 2 * r], [px_w - 2 * r, 0, px_w, 2 * r],
                [px_w - 2 * r, px_h - 2 * r, px_w, px_h],
                [0, px_h - 2 * r, 2 * r, px_h]]):
                if on:
                    d.ellipse(box, fill=255)
        im = im.convert("RGBA")
        im.putalpha(mask)
    out = GEN / ("img_%d.png" % (abs(hash(key)) % 10 ** 9))
    im.save(out)
    _img_cache[key] = str(out)
    return str(out)


def image(page, path, rect_, radius=0, corners=None, crop_ratio=None):
    p = rounded_image(path, rect_[2] - rect_[0], rect_[3] - rect_[1],
                      radius=radius, corners=corners, crop_ratio=crop_ratio)
    page.insert_image(pymupdf.Rect(*rect_), filename=p, keep_proportion=False)


def arrow(page, pts, color=BLUE, width=6, head=16):
    """Flèche composée de segments droits ou d'une courbe (liste de points)."""
    shape = page.new_shape()
    shape.draw_polyline([pymupdf.Point(*p) for p in pts])
    shape.finish(color=hexc(color), width=width, lineCap=1, lineJoin=1)
    # tête de flèche
    import math
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    left = (x1 - head * math.cos(ang - 0.45), y1 - head * math.sin(ang - 0.45))
    right = (x1 - head * math.cos(ang + 0.45), y1 - head * math.sin(ang + 0.45))
    shape.draw_polyline([pymupdf.Point(*left), pymupdf.Point(x1, y1),
                         pymupdf.Point(*right)])
    shape.finish(color=hexc(color), width=width, lineCap=1, lineJoin=1)
    shape.commit()


def curved_arrow(page, start, end, bulge=0.35, color=BLUE, width=5.5, head=14):
    """Flèche courbe (quadratique) entre deux points."""
    shape = page.new_shape()
    p0, p3 = pymupdf.Point(*start), pymupdf.Point(*end)
    dx, dy = p3.x - p0.x, p3.y - p0.y
    c1 = pymupdf.Point(p0.x + dx * 0.5, p0.y + dy * bulge)
    c2 = pymupdf.Point(p0.x + dx * 0.5, p0.y + dy * (1 - bulge * 0.2))
    shape.draw_bezier(p0, c1, c2, p3)
    shape.finish(color=hexc(color), width=width, lineCap=1, lineJoin=1)
    import math
    ang = math.atan2(p3.y - p0.y, p3.x - p0.x)
    # tangente approchée en fin de courbe
    ang = math.atan2(c2.y - p3.y, c2.x - p3.x)
    left = (p3.x + head * math.cos(ang - 0.5), p3.y + head * math.sin(ang - 0.5))
    right = (p3.x + head * math.cos(ang + 0.5), p3.y + head * math.sin(ang + 0.5))
    shape.draw_polyline([pymupdf.Point(*left), p3, pymupdf.Point(*right)])
    shape.finish(color=hexc(color), width=width, lineCap=1, lineJoin=1)
    shape.commit()


class Page:
    """Registre les polices sur une page et simplifie l'écriture."""
    def __init__(self, doc):
        self.page = doc.new_page(width=W, height=H)
        for k, v in FONT_FILES.items():
            self.page.insert_font(fontname=k, fontfile=str(ASSETS / v))

    # raccourcis
    def t(self, x, y, s, font="PR", size=14, color=BLACK, width=None):
        return draw_text(self.page, x, y, s, font, size, color, width)

    def tc(self, cx, y, s, font="PR", size=14, color=BLACK):
        text_center(self.page, cx, y, s, font, size, color)

    def tr(self, rx, y, s, font="PR", size=14, color=BLACK):
        text_right(self.page, rx, y, s, font, size, color)

    def wrap(self, s, font, size, width):
        return wrap(s, font, size, width)

    def panel(self, r, fill=PALE, radius=22):
        panel(self.page, r, fill, radius)

    def card(self, r, radius=10, fill="#FFFFFF", with_shadow=True, border=None):
        card(self.page, r, radius, fill, with_shadow, border)

    def rect(self, r, fill=None, color=None, width=1, radius=0):
        rect(self.page, r, fill, color, width, radius)

    def line(self, p1, p2, color=LIGHT_LINE, width=1):
        line(self.page, p1, p2, color, width)

    def image(self, path, r, radius=0, corners=None, crop_ratio=None):
        image(self.page, path, r, radius, corners, crop_ratio)

    def pill(self, r, s, fill=BLUE, color="#FFFFFF", font="PS", size=9):
        pill(self.page, r, s, fill, color, font, size)

    def save(self, path):
        self.page.parent.save(path, garbage=4, deflate=True)
