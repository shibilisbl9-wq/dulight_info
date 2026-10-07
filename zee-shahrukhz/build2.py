"""ZEE REAL ESTATE x Shahrukhz Residences - v2 creatives (1080x1350).
Big type, clean renders, real Dirham sign, footer = ZEE logo + email + empty QR space only."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os

U = '/root/.claude/uploads/c4209a85-c4cd-59ab-8caf-53b60a036e6c/'
IMG_SKYLINE = U + 'ffc89cc1-image.webp'   # dusk skyline, 1920x1080
IMG_ISLAND = U + '60c483a9-image.jpg'     # island aerial, 1920x1080
IMG_PODIUM = U + '4df3d556-image.webp'    # podium close-up, 1920x1080
COUPLE = os.environ.get('COUPLE_PNG', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'couple_cutout.png'))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_v2')
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
FD = '/usr/share/fonts/opentype/inter/'
GOLD = (242, 196, 109)
WHITE = (255, 255, 255)


def F(w, s):
    return ImageFont.truetype(FD + 'Inter-%s.otf' % w, s)


def vramp(y0, y1, a0, a1):
    m = Image.new('L', (1, H))
    for y in range(H):
        t = 0 if y <= y0 else 1 if y >= y1 else (y - y0) / (y1 - y0)
        m.putpixel((0, y), round(a0 + (a1 - a0) * t))
    return m.resize((W, H))


def shade(im, y0, y1, a0, a1, color=(0, 0, 0)):
    im.paste(Image.new('RGB', (W, H), color), (0, 0), vramp(y0, y1, a0, a1))


def crop45(path, x0, y0=0, h=1080):
    """Crop a 4:5 window from a 16:9 render and scale to 1080x1350."""
    im = Image.open(path).convert('RGB')
    w = int(h * 0.8)
    return im.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.LANCZOS)


def text(im, xy, s, font, fill=WHITE, anchor='la', shadow=140):
    """Text with a soft shadow so it stays readable on a photo."""
    if shadow:
        lay = Image.new('L', (W, H), 0)
        ImageDraw.Draw(lay).text((xy[0] + 2, xy[1] + 5), s, font=font, fill=shadow, anchor=anchor)
        lay = lay.filter(ImageFilter.GaussianBlur(9))
        im.paste(Image.new('RGB', (W, H), (0, 0, 0)), (0, 0), lay)
    ImageDraw.Draw(im).text(xy, s, font=font, fill=fill, anchor=anchor)


def tw(s, font):
    return ImageDraw.Draw(Image.new('L', (1, 1))).textlength(s, font=font)


# ---------- new UAE Dirham sign (vector-drawn) ----------
def dirham_w(cap_h):
    return cap_h * 0.80 + cap_h * 0.30


def dirham(im, x, y_top, cap_h, fill=WHITE, shadow=True):
    """D with two flared horizontal bars. Draws at (x, y_top); returns width used."""
    size = cap_h / 0.727
    f = F('Bold', int(size))
    d = ImageDraw.Draw(im)
    bb = f.getbbox('D')
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    ox = x + cap_h * 0.12
    S = 4  # supersample the sign for crisp edges
    pad = int(cap_h * 0.4)
    lw, lh = int((gw + cap_h * 0.5) * S), int((gh + pad) * S)
    mask = Image.new('L', (lw, lh), 0)
    md = ImageDraw.Draw(mask)
    fs = ImageFont.truetype(FD + 'Inter-Bold.otf', int(size * S))
    md.text((int(cap_h * 0.16 * S) - bb[0] * S, int(pad / 2 * S) - bb[1] * S), 'D', font=fs, fill=255)
    t = gh * 0.105 * S
    left = cap_h * 0.02 * S
    right = (gw + cap_h * 0.30) * S
    for cy in (0.37, 0.64):
        yy = pad / 2 * S + gh * cy * S
        md.rounded_rectangle((left, yy - t / 2, right, yy + t / 2), radius=t / 2, fill=255)
    mask = mask.resize((lw // S, lh // S), Image.LANCZOS)
    px, py = int(x), int(y_top - pad / 2)
    if shadow:
        sh = Image.new('L', (W, H), 0)
        sh.paste(mask.point(lambda v: v * 140 // 255), (px + 2, py + 5))
        sh = sh.filter(ImageFilter.GaussianBlur(9))
        im.paste(Image.new('RGB', (W, H), (0, 0, 0)), (0, 0), sh)
    im.paste(Image.new('RGB', mask.size, fill), (px, py), mask)
    return gw + cap_h * 0.34


def price(im, x, y, num, cap_h, fill=WHITE):
    """[Dirham sign] + number. y = top of cap height."""
    w1 = dirham(im, x, y, cap_h, fill)
    f = F('Black', int(cap_h / 0.727))
    bb = f.getbbox(num)
    text(im, (x + w1 + cap_h * 0.12 - bb[0], y - bb[1]), num, f, fill)
    return w1 + cap_h * 0.12 + (bb[2] - bb[0])


# ---------- footer: ZEE logo + email + empty QR space ----------
def footer(im):
    shade(im, 1090, 1230, 0, 240)
    d = ImageDraw.Draw(im)
    # logo
    d.rounded_rectangle((60, 1196, 128, 1264), 6, fill='white')
    d.text((94, 1230), 'Z', font=F('Medium', 50), fill='black', anchor='mm')
    x = 150
    d.text((x, 1204), 'ZEE', font=F('Bold', 34), fill='white')
    d.text((x, 1244), 'REAL ESTATE', font=F('Light', 22), fill='white')
    d.text((60, 1290), 'info@zeerealestate.ae', font=F('Medium', 32), fill='white')
    # QR space (paste the QR here)
    d.rounded_rectangle((880, 1172, 1020, 1312), 10, fill='white')


def ribbon(im, y, s, size=34, pad_x=26, pad_y=14):
    f = F('ExtraBold', size)
    w = tw(s, f)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, y, 60 + w + pad_x * 2, y + size + pad_y * 2 + 4), 12, fill=GOLD)
    d.text((60 + pad_x, y + pad_y + 2), s, font=f, fill=(25, 20, 10))
    return 60 + w + pad_x * 2


def save(im, name):
    im.save(os.path.join(OUT, name + '.jpg'), quality=95)
    im.save(os.path.join(OUT, name + '.png'))


# ======================= 1: Golden Visa (skyline) =======================
def ad1():
    im = crop45(IMG_SKYLINE, 380)
    shade(im, 0, 560, 150, 0)
    shade(im, 700, 1090, 0, 215)
    f = F('Black', 112)
    text(im, (56, 52), 'YOUR OWN', f)
    text(im, (56, 164), 'HOME IN', f)
    text(im, (56, 276), 'DUBAI', f, GOLD)
    ribbon(im, 430, '+ 10-YEAR GOLDEN VISA*', 36)
    text(im, (60, 866), 'STARTING FROM', F('Bold', 44))
    price(im, 60, 934, '2.3M', 150)
    text(im, (60, 1112), '1 BHK  |  FULLY FURNISHED  |  10% DOWN', F('Bold', 34))
    text(im, (60, 1156), '*Golden Visa for units valued AED 2M+, subject to approval.', F('Medium', 24), (225, 225, 225), shadow=0)
    footer(im)
    save(im, 'zee-shahrukhz-1-golden-visa')


# ======================= 2: Couple / waterfront lifestyle (island) =======================
def ad2():
    im = crop45(IMG_ISLAND, 330)
    shade(im, 0, 480, 120, 0)
    c = Image.open(COUPLE).convert('RGBA')
    s = 1000 / c.height
    c = c.resize((int(c.width * s), 1000), Image.LANCZOS)
    cx, cy = -30, 410
    # ground the couple: fade their lower part into dark
    im.paste(c, (cx, cy), c)
    shade(im, 860, 1130, 0, 245)
    f = F('Black', 90)
    text(im, (56, 56), 'WATERFRONT', f)
    text(im, (56, 152), 'LIVING', f, GOLD)
    text(im, (60, 276), 'DESIGNED BY', F('Medium', 34), (235, 235, 235))
    text(im, (60, 318), 'GAURI KHAN', F('ExtraBold', 62))
    text(im, (60, 862), 'STARTING FROM', F('Bold', 44))
    price(im, 60, 930, '1.65M', 150)
    text(im, (60, 1108), '30/70 PLAN  |  HANDOVER Q4 2029', F('Bold', 34))
    text(im, (60, 1154), 'FULLY FURNISHED  |  DUBAI MARITIME CITY', F('Medium', 28), (225, 225, 225), shadow=0)
    footer(im)
    save(im, 'zee-shahrukhz-2-waterfront-living')


# ======================= 3: 10% down + prices (podium) =======================
def ad3():
    im = crop45(IMG_PODIUM, 470)
    shade(im, 0, 560, 225, 90)
    shade(im, 560, 700, 90, 0)
    shade(im, 700, 1000, 0, 225)
    text(im, (60, 56), 'OWN IT WITH JUST', F('ExtraBold', 62))
    fs = 190
    while tw('10% DOWN', F('Black', fs)) > 960:
        fs -= 4
    text(im, (52, 128), '10% DOWN', F('Black', fs), GOLD)
    text(im, (60, 350), 'SHAHRUKHZ RESIDENCES BY DANUBE', F('Bold', 34))
    text(im, (60, 396), 'DUBAI MARITIME CITY', F('Medium', 32), (235, 235, 235))
    # price grid 2x2
    cells = [('STUDIO', '1.65M'), ('1 BHK', '2.3M'), ('2 BHK', '4.25M'), ('3 BHK', '6.5M')]
    d = ImageDraw.Draw(im)
    gx, gy, cw, ch, gap = 60, 800, 470, 150, 20
    for i, (lab, val) in enumerate(cells):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rounded_rectangle((x, y, x + cw, y + ch), 18, fill=(10, 14, 22), outline=GOLD, width=3)
        d.text((x + 28, y + 18), lab, font=F('Bold', 30), fill=GOLD)
        price(im, x + 28, y + 70, val, 52)
    text(im, (60, 1138), '30% DURING CONSTRUCTION  |  70% ON HANDOVER (DEC 2029)', F('Bold', 27), shadow=0)
    footer(im)
    save(im, 'zee-shahrukhz-3-10-percent-down')


if __name__ == '__main__':
    ad1(); ad2(); ad3()
    print(sorted(os.listdir(OUT)))
