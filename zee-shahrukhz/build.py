"""ZEE REAL ESTATE x Shahrukhz Residences - 3 ad creatives (1080x1350), Equiterra-2 layout."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os

U = '/root/.claude/uploads/c4209a85-c4cd-59ab-8caf-53b60a036e6c/'
SRC1, SRC2, SRC3 = U + '4b8b4fd2-image.jpg', U + '1475dcd2-image.jpg', U + '6b8c5859-image.jpg'
REF = U + '3dddda48-image.jpg'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
FD = '/usr/share/fonts/opentype/inter/'


def F(w, s):
    return ImageFont.truetype(FD + 'Inter-%s.otf' % w, s)


def tracked(d, xy, text, font, fill, track=0, anchor='l'):
    """Draw letter-spaced text. anchor l/m/r on x."""
    widths = [d.textlength(c, font=font) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor == 'm':
        x -= total / 2
    elif anchor == 'r':
        x -= total
    for c, w in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill)
        x += w + track
    return total


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def vfade(h, y0, y1, a0, a1):
    """Vertical alpha ramp mask (L) of height h."""
    m = Image.new('L', (1, h))
    for y in range(h):
        t = 0 if y <= y0 else 1 if y >= y1 else (y - y0) / (y1 - y0)
        m.putpixel((0, y), round(a0 + (a1 - a0) * t))
    return m.resize((W, h))


def hfade_mask(w, h, l0, l1, r0, r1):
    m = Image.new('L', (w, h), 255)
    px = m.load()
    for x in range(w):
        a = 255
        if x < l1:
            a = 0 if x <= l0 else int(255 * (x - l0) / (l1 - l0))
        if x > r0:
            b = 0 if x >= r1 else int(255 * (r1 - x) / (r1 - r0))
            a = min(a, b)
        for y in range(h):
            px[x, y] = a
    return m


def black_ramps(canvas, top_to=0, bot_from=900, bot_full=1060):
    blk = Image.new('RGB', (W, H), (0, 0, 0))
    m = vfade(H, bot_from, bot_full, 0, 255)
    if top_to:
        top = vfade(H, 0, top_to, 255, 0)
        m = ImageChops.lighter(m, top)
    canvas.paste(blk, (0, 0), m)


# ---------- icons (drawn, white) ----------
def icon_bed(d, x, y, s=64, c='white'):
    d.rounded_rectangle((x, y + s * .30, x + s * .16, y + s * .95), 3, fill=c)
    d.rounded_rectangle((x + s * 1.0 - s * .16, y + s * .30, x + s * 1.0, y + s * .95), 3, fill=c)
    d.rounded_rectangle((x, y + s * .55, x + s, y + s * .80), 5, fill=c)
    d.rounded_rectangle((x + s * .12, y + s * .22, x + s * .46, y + s * .50), 6, fill=c)
    d.rounded_rectangle((x + s * .54, y + s * .22, x + s * .88, y + s * .50), 6, fill=c)


def icon_pin(d, x, y, s=64, c='white'):
    r = s * .30
    cx, cy = x + s * .5, y + s * .36
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
    d.polygon([(cx - r * .86, cy + r * .5), (cx + r * .86, cy + r * .5), (cx, y + s * .98)], fill=c)
    d.ellipse((cx - r * .42, cy - r * .42, cx + r * .42, cy + r * .42), fill=(20, 20, 20))


def icon_card(d, x, y, s=64, c='white'):
    d.rounded_rectangle((x, y + s * .2, x + s, y + s * .8), 8, outline=c, width=5)
    d.rectangle((x, y + s * .36, x + s, y + s * .5), fill=c)
    d.rectangle((x + s * .12, y + s * .62, x + s * .38, y + s * .68), fill=c)


def icon_cal(d, x, y, s=64, c='white'):
    d.rounded_rectangle((x + s * .06, y + s * .15, x + s * .94, y + s * .92), 8, outline=c, width=5)
    d.rectangle((x + s * .06, y + s * .15, x + s * .94, y + s * .38), fill=c)
    for i in (0.3, 0.7):
        d.rounded_rectangle((x + s * i - 3, y + s * .04, x + s * i + 3, y + s * .26), 3, fill=c)
    for cx in (.30, .50, .70):
        for cy in (.55, .74):
            d.rectangle((x + s * cx - 3, y + s * cy - 3, x + s * cx + 3, y + s * cy + 3), fill=c)


def icon_key(d, x, y, s=64, c='white'):
    d.ellipse((x + s * .05, y + s * .25, x + s * .45, y + s * .65), outline=c, width=6)
    d.rectangle((x + s * .45, y + s * .42, x + s * .95, y + s * .50), fill=c)
    d.rectangle((x + s * .78, y + s * .50, x + s * .85, y + s * .70), fill=c)
    d.rectangle((x + s * .64, y + s * .50, x + s * .71, y + s * .64), fill=c)


def icon_visa(d, x, y, s=64, c='white'):
    d.rounded_rectangle((x, y + s * .18, x + s, y + s * .82), 8, outline=c, width=5)
    d.ellipse((x + s * .12, y + s * .32, x + s * .36, y + s * .56), outline=c, width=4)
    d.rectangle((x + s * .5, y + s * .36, x + s * .88, y + s * .42), fill=c)
    d.rectangle((x + s * .5, y + s * .50, x + s * .88, y + s * .56), fill=c)
    d.rectangle((x + s * .12, y + s * .66, x + s * .88, y + s * .71), fill=c)


def icon_pct(d, x, y, s=64, c='white'):
    d.ellipse((x + s * .08, y + s * .12, x + s * .38, y + s * .42), outline=c, width=5)
    d.ellipse((x + s * .62, y + s * .58, x + s * .92, y + s * .88), outline=c, width=5)
    d.line((x + s * .85, y + s * .1, x + s * .15, y + s * .9), fill=c, width=6)


ICONS = dict(bed=icon_bed, pin=icon_pin, card=icon_card, cal=icon_cal, key=icon_key, visa=icon_visa, pct=icon_pct)

# ---------- brand assets ----------
ref = Image.open(REF).convert('RGB')
QR = ref.crop((912, 28, 1048, 160))  # ZEE QR from the Equiterra ad


def footer(d, im, dev='DANUBE', dev_italic=True):
    # ZEE logo (rebuilt)
    d.rounded_rectangle((76, 1275, 108, 1307), 3, fill='white')
    d.text((92, 1291), 'Z', font=F('Medium', 24), fill='black', anchor='mm')
    tracked(d, (24, 1312), 'ZEE REAL ESTATE', F('Light' if os.path.exists(FD + 'Inter-Light.otf') else 'ExtraLight', 15), 'white', 2.2)
    d.text((540, 1300), 'info@zeerealestate.ae', font=F('Light' if os.path.exists(FD + 'Inter-Light.otf') else 'ExtraLight', 24), fill='white', anchor='mm')
    f = ImageFont.truetype(FD + ('Inter-ExtraBoldItalic.otf' if dev_italic else 'Inter-ExtraBold.otf'), 38)
    d.text((1056, 1297), dev, font=f, fill='white', anchor='rm')
    im.paste(QR, (912, 28))


def info_band(d, cols, y=1115):
    """cols: list of (icon, line1, line2). Reference 2-col layout, divider line above."""
    d.line((228, y - 10, 852, y - 10), fill=(235, 235, 235), width=2) if len(cols) == 2 else d.line((90, y - 10, 990, y - 10), fill=(235, 235, 235), width=2)
    n = len(cols)
    if n == 2:
        xs = [(228, 556), (558, 852)]
        for (x0, x1), (ic, l1, l2) in zip(xs, cols):
            ICONS[ic](d, x0 + 38, y + 18, 62)
            d.text((x0 + 128, y + 8), l1, font=F('Bold', 26), fill='white')
            d.text((x0 + 128, y + 42), l2, font=F('ExtraLight', 26), fill='white')
        d.line((557, y + 8, 557, y + 68), fill=(235, 235, 235), width=2)
    else:
        colw = (990 - 90) / n
        for i, (ic, l1, l2) in enumerate(cols):
            cx = 90 + colw * i + colw / 2
            d.text((cx, y + 22), l1, font=F('ExtraLight', 22), fill='white', anchor='mm')
            d.text((cx, y + 62), l2, font=F('Bold', 34), fill='white', anchor='mm')
            if i:
                d.line((90 + colw * i, y + 8, 90 + colw * i, y + 78), fill=(235, 235, 235), width=2)


def title_block(d, y=62):
    tracked(d, (58, y), 'SHAHRUKHZ', F('Light' if os.path.exists(FD + 'Inter-Light.otf') else 'ExtraLight', 62), 'white', 8)
    tracked(d, (60, y + 74), 'RESIDENCES  BY DANUBE', F('Medium', 26), 'white', 9)


def price_block(d, label, price, y=190, size=170, prefix='AED'):
    tracked(d, (62, y), label, F('Bold', 32), 'white', 2)
    d.text((62, y + 96), prefix, font=F('Bold', 54), fill='white')
    pw = d.textlength(prefix, font=F('Bold', 54))
    d.text((62 + pw + 18, y + 20), price, font=F('Bold', size), fill='white')


def headline(d, l1, l2, y=985, fs2=66):
    d.text((540, y), l1, font=F('ExtraLight', 62), fill='white', anchor='mm')
    d.text((540, y + 66), l2, font=F('SemiBold', fs2), fill='white', anchor='mm')


def shadow_layer(canvas, box_y0, box_y1, strength=120):
    pass


def finish(im, name):
    im.save(os.path.join(OUT, name + '.jpg'), quality=95)
    im.save(os.path.join(OUT, name + '.png'))


# ======================= AD 1: Golden Visa (image 1) =======================
def strip_bg(src, x0, x1, blur=36, dim=0.95):
    """Background from a text-free vertical strip, stretched wide and blurred."""
    st = src.crop((x0, 0, x1, src.height)).resize((W, H), Image.LANCZOS)
    st = st.filter(ImageFilter.GaussianBlur(blur))
    return Image.eval(st, lambda v: int(v * dim))


def ad1():
    s1 = Image.open(SRC1).convert('RGB')
    bg = strip_bg(s1, 1110, 1254)
    fg = s1.crop((720, 0, 1254, 1160))
    m = hfade_mask(fg.width, fg.height, 0, 70, fg.width, fg.width + 1)
    im = bg.copy()
    im.paste(fg, (W - fg.width, 0), m)
    black_ramps(im, top_to=0, bot_from=800, bot_full=1000)
    d = ImageDraw.Draw(im)
    title_block(d)
    price_block(d, 'STARTING FROM', '2.3M', y=215, size=140)
    d.text((64, 212 + 215 - 34), '1 BHK  |  FULLY FURNISHED', font=F('SemiBold', 26), fill='white')
    headline(d, 'YOUR OWN HOME IN DUBAI', 'PLUS A 10-YEAR GOLDEN VISA*', y=968, fs2=50)
    info_band(d, [('card', '10% DOWN', '30/70 PLAN'), ('pin', 'DUBAI', 'MARITIME CITY')], y=1110)
    d.text((540, 1233), '*Golden Visa for units valued AED 2M+, subject to approval.', font=F('Light', 17), fill=(215, 215, 215), anchor='mm')
    footer(d, im)
    finish(im, 'zee-shahrukhz-1-golden-visa')


# ======================= AD 2: Waterfront lifestyle (image 2) =======================
def ad2():
    s2 = Image.open(SRC2).convert('RGB')
    crop = s2.crop((0, 140, 480, 515))
    fg = crop.resize((1080, int(375 * 2.25)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    im = Image.new('RGB', (W, H), (0, 0, 0))
    im.paste(fg, (0, 350))
    # fade photo top into black and bottom into black
    blk = Image.new('RGB', (W, H), (0, 0, 0))
    m = ImageChops.lighter(vfade(H, 905, 1070, 0, 255), vfade(H, 350, 372, 255, 0))
    im.paste(blk, (0, 0), m)
    d = ImageDraw.Draw(im)
    title_block(d)
    price_block(d, 'STARTING FROM', '1.65M', y=190, size=118)
    d.text((540, 975), 'HANDOVER Q4 2029', font=F('SemiBold', 64), fill='white', anchor='mm')
    d.text((540, 1043), 'FULLY FURNISHED WATERFRONT RESIDENCES', font=F('ExtraLight', 30), fill='white', anchor='mm')
    info_band(d, [('card', '30/70', 'PLAN'), ('pin', 'DUBAI', 'MARITIME CITY')], y=1110)
    footer(d, im)
    finish(im, 'zee-shahrukhz-2-waterfront')


# ======================= AD 3: 10% down + prices (image 3) =======================
def ad3():
    s3 = Image.open(SRC3).convert('RGB')
    bg = strip_bg(s3, 358, 410, blur=30)
    sea = s3.crop((700, 960, 1000, 1030)).resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    bg.paste(Image.new('RGB', (W, H), sea), (0, 0), vfade(H, 700, 860, 0, 255))
    fg = s3.crop((0, 0, 412, 1254))
    fgs = fg.resize((int(412 * 0.97), int(1254 * 0.97)), Image.LANCZOS)
    im = bg.copy()
    m = hfade_mask(fgs.width, fgs.height, 0, 1, fgs.width - 60, fgs.width)
    im.paste(fgs, (0, 0), m)
    black_ramps(im, top_to=0, bot_from=820, bot_full=1000)
    d = ImageDraw.Draw(im)
    tracked(d, (420, 62), 'SHAHRUKHZ', F('Light', 62), 'white', 8)
    tracked(d, (422, 136), 'RESIDENCES  BY DANUBE', F('Medium', 22), 'white', 6)
    tracked(d, (1018, 245), 'PAY JUST', F('Bold', 32), 'white', 2, anchor='r')
    d.text((1018, 275), '10%', font=F('Bold', 200), fill='white', anchor='ra')
    d.text((1018, 495), 'DOWN PAYMENT', font=F('SemiBold', 44), fill='white', anchor='ra')
    headline(d, 'OWN A SEA-VIEW HOME IN', 'DUBAI MARITIME CITY', y=955, fs2=62)
    info_band(d, [(None, 'STUDIO', 'AED 1.65M'), (None, '1 BHK', 'AED 2.3M'), (None, '2 BHK', 'AED 4.25M'), (None, '3 BHK', 'AED 6.5M')], y=1100)
    d.text((540, 1215), '30% DURING CONSTRUCTION   |   70% ON HANDOVER (DEC 2029)   |   FULLY FURNISHED', font=F('Medium', 17), fill=(225, 225, 225), anchor='mm')
    footer(d, im)
    finish(im, 'zee-shahrukhz-3-10-percent-down')


if __name__ == '__main__':
    ad1(); ad2(); ad3()
    print(os.listdir(OUT))
