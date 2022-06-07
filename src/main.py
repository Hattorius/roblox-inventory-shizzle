import src.image as image
import requests, json, glob, os, time
from datetime import datetime
from discord_webhook import DiscordWebhook

rolimons = {}
with open('cookie.txt') as f:
    cookie = f.readline()
with open('webhook.txt') as f:
    webhook_url = f.readline()

def createImage(received=[], sent=[]):
    receivedImages = []
    sentImages = []

    receivedRapTotal = 0
    receivedRolimonTotal = 0
    sentRapTotal = 0
    sentRolimonTotal = 0

    for id in received:
        item = rolimons[str(id)]
        limitedImage = requests.get(item[-1])
        with open('limiteds/' + str(id) + '.png', 'wb') as f:
            f.write(limitedImage.content)
        receivedImages.append(image.importLimited(str(id), item[8], item[0], item[16], item[19]))
        receivedRapTotal += item[8]
        if item[16] is not None:
            receivedRolimonTotal += item[16]
        else:
            receivedRolimonTotal += item[8]

    for id in sent:
        item = rolimons[str(id)]
        limitedImage = requests.get(item[-1])
        with open('limiteds/' + str(id) + '.png', 'wb') as f:
            f.write(limitedImage.content)
        sentImages.append(image.importLimited(str(id), item[8], item[0], item[16], item[19]))
        sentRapTotal += item[8]
        if item[16] is not None:
            sentRolimonTotal += item[16]
        else:
            sentRolimonTotal += item[8]

    tradeImage = image.putLimitedsInTradeScreen(sentImages, receivedImages, sentRapTotal, receivedRapTotal, sentRolimonTotal, receivedRolimonTotal, receivedRolimonTotal - sentRolimonTotal)
    for f in glob.glob('limiteds/*'):
        os.remove(f)
    return tradeImage

def updateRolimons():
    global rolimons
    body = requests.get('https://www.rolimons.com/catalog').text
    rolimons = json.loads(body.split('var item_details = ')[1].split(';')[0])

userid = requests.get('https://www.roblox.com/mobileapi/userinfo', headers={'Cookie': '.ROBLOSECURITY=' + cookie}).json()['UserID']

def getInventory(userid, cursor="", prevData=[]):
    data = requests.get('https://inventory.roblox.com/v1/users/%i/assets/collectibles?sortOrder=Asc&limit=100&cursor=%s' % (userid, cursor)).json()
    if data['nextPageCursor'] is None:
        return prevData + data['data']
    time.sleep(1)
    return getInventory(userid, cursor=data['nextPageCursor'], prevData=prevData + data['data'])

def getTrade(id):
    trade = requests.get('https://trades.roblox.com/v1/trades/%i' % id, headers={'Cookie': '.ROBLOSECURITY=' + cookie}).json()
    try:
        trade['offers']
    except:
        time.sleep(5)
        return getTrade(id)
    received = []
    sent = []
    for offer in trade['offers']:
        if offer['user']['id'] == userid:
            for asset in offer['userAssets']:
                sent.append(asset['assetId'])
        else:
            for asset in offer['userAssets']:
                received.append(asset['assetId'])
    return [received, sent]

def getTrades():
    trades = requests.get('https://trades.roblox.com/v1/trades/Completed?sortOrder=Asc&limit=10', headers={'Cookie': '.ROBLOSECURITY=' + cookie}).json()
    try:
        trades['data']
    except:
        time.sleep(5)
        return getTrades()
    newTrades = []
    for trade in trades['data']:
        secondsAgo = time.time() - (datetime.strptime(trade['created'], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime(1970, 1, 1)).total_seconds()
        if secondsAgo < 320:
            newTrades.append(getTrade(trade['id']))
    return newTrades

inventory = getInventory(userid)
while True:
    time.sleep(300)
    inventoryNow = getInventory(userid)
    if inventoryNow != inventory:
        updateRolimons()
        tradesToDo = getTrades()
        for trade in tradesToDo:
            tradeImage = createImage(trade[0], trade[1])
            tradeImage.save('trade.png')
            webhook = DiscordWebhook(url=webhook_url, username="Slave or something idk", rate_limit_retry=True, content="@everyone")
            with open("trade.png", "rb") as f:
                webhook.add_file(file=f.read(), filename='trade.png')
            webhook.execute()
    inventory = inventoryNow
