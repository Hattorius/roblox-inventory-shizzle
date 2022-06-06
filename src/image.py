import humanize, textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

background = Image.open('images/item.png').convert("RGBA")
rolimonsICO = Image.open('images/rolimons.png').convert("RGBA")
font = ImageFont.truetype("fonts/GothamSSm.woff2", 16)
fontBig = ImageFont.truetype("fonts/GothamSSm_bold.woff2", 20)
tradeBackground = Image.open('images/background.png').convert("RGBA")

def importLimited(id, rap, name="DIY Dominus Empyreus", rolimons=None):
    # put limited image on top of background
    im = Image.open('limiteds/%s.png' % id).convert("RGBA")
    im.thumbnail((126, 126), Image.ANTIALIAS)
    limited = background.copy()
    limited.paste(im, (9, 9), im)

    # write rap in image
    draw = ImageDraw.Draw(limited)
    draw.text((30, 190), humanize.intcomma(rap), (255,255,255), font=font)

    # write name in image
    c = 0
    for text in textwrap.wrap(name, 12):
        if c == 2:
            break
        draw.text((12, 144 + (c*20)), text, (255,255,255), font=font)
        c += 1

    # if rolimons value is there
    if rolimons is not None:
        temp = rolimonsICO.copy()
        limited.paste(temp, (12, 210), temp)
        draw.text((30, 210), humanize.intcomma(rolimons), (255,255,255), font=font)

    return limited

def putLimitedsInTradeScreen(sent=[], received=[], sentTotal=5, receivedTotal=10):
    trade = tradeBackground.copy()

    # put in sent limiteds
    c = 0
    for item in sent:
        trade.paste(item, (15 + (140*c), 30)) # 270
        c += 1

    # put in received limiteds
    c = 0
    for item in received:
        trade.paste(item, (15 + (140*c), 375))
        c += 1
    
    draw = ImageDraw.Draw(trade)
    draw.text((470, 279), humanize.intcomma(sentTotal), (255,255,255), font=fontBig)
    draw.text((470, 623), humanize.intcomma(receivedTotal), (255,255,255), font=fontBig)

    trade.show()