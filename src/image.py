import humanize, textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

background = Image.open('images/item.png').convert("RGBA")
rolimonsICO = Image.open('images/rolimons.png').convert("RGBA")
rolimonsICO2 = Image.open('images/rolimons2.png').convert("RGBA")
rolimonsICO2.thumbnail((20, 20), Image.ANTIALIAS)
font = ImageFont.truetype("fonts/GothamSSm.woff", 16)
fontBig = ImageFont.truetype("fonts/GothamSSm_bold.woff", 20)
tradeBackground = Image.open('images/background.png').convert("RGBA")
projectedPic = Image.open('images/projected.png').convert("RGBA")

def importLimited(id, rap, name="DIY Dominus Empyreus", rolimons=None, projected=False):
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

    # if projected show
    if projected:
        limited.paste(projectedPic, (9, 9), projectedPic)
        pass

    return limited

def putLimitedsInTradeScreen(sent=[], received=[], sentTotal=5, receivedTotal=10, sentTotalRolimons=5, receivedTotalRolimons=10, diff=5):
    trade = tradeBackground.copy()

    # put in sent limiteds
    c = 0
    for item in sent:
        trade.paste(item, (15 + (140*c), 34)) # 270
        c += 1

    # put in received limiteds
    c = 0
    for item in received:
        trade.paste(item, (15 + (140*c), 379))
        c += 1
    
    draw = ImageDraw.Draw(trade)
    draw.text((470, 279), humanize.intcomma(sentTotal), (255,255,255), font=fontBig)
    draw.text((470, 623), humanize.intcomma(receivedTotal), (255,255,255), font=fontBig)

    trade.paste(rolimonsICO2, (445, 305), rolimonsICO2)
    trade.paste(rolimonsICO2, (441, 649), rolimonsICO2)

    draw.text((470, 303), humanize.intcomma(sentTotalRolimons), (255,255,255), font=fontBig)
    draw.text((470, 647), humanize.intcomma(receivedTotalRolimons), (255,255,255), font=fontBig)

    middle = 291.5
    text = humanize.intcomma(diff)
    if diff > 0:
        text = "+" + text
    w, h = font.getsize(text)
    w += 40
    draw.rectangle((middle - w/2, 330, middle - w/2 + w, 330 + h), fill='#232527')

    draw.text((middle - w/2 + 20, 330), humanize.intcomma(text), (255,255,255), font=font)

    return trade