import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

# TODO:
# Develop rules for downloading image and description
'''
#prints sourcecode to file
try:
    f = open('sourcecode.txt', 'a')
    f.write(str(respData))
    f.close()
except Exception as e:
    print(str(e))
'''

cardlist = {}

def getRawUrlData(url, parameters):
    # Takes in URL string and parameter list
    # Returns BS4 object of webpage

    url_values = urllib.parse.urlencode(parameters)
    target_url = url
    full_url = target_url + '?' + url_values
    data = urllib.request.urlopen(full_url)
    response = data.read()
    webpagedata = BeautifulSoup(str(response))
    print('got stuff from the net yo!')
    return webpagedata 


def serialiseCardData(urldata):

    # BS4.ResultSets of each attribute
    cardname = urldata.find_all('td', {'class': 'col-name'})
    cardtype = urldata.find_all('td', {'class': 'col-type'})
    cardclass = urldata.find_all('td', {'class': 'col-class'})
    cardcost = urldata.find_all('td', {'class': 'col-cost'})
    cardattack = urldata.find_all('td', {'class': 'col-attack'})
    cardhealth = urldata.find_all('td', {'class': 'col-health'})

    # Loop to combine all attributes with key=card_name
    for i in range(len(cardname)):
        cardlist[cardname[i].text.replace('\\r\\n', '')] = {'class':cardclass[i].text.replace('\xa0', ''), 'type':cardtype[i].text, 'cost':cardcost[i].text, 'attack':cardattack[i].text, 'health':cardhealth[i].text}

    print('put data into cardlist')

def getCardImgAndDescription(urldata):

    # thead > tbody > tr = CARD
    # CARD > td class=visual-image-cell > img class="hscard-static" src = IMG
    # CARD > td class=visual-details-cell > h3 = CARDTITLE
    # CARD > td class=visual-details-cell > p = CARD DESCRIPTION

    cardname = urldata.find_all('')
    cardimg = urldata.find_all('')
    carddesc = urldata.find_all('')

    for i in range(len(cardimg)):
        cardlist[cardname[i]] = {'description':carddesc[i], 'img':cardimg[i]}

    print('finished getting img and description')

def dumpDataToJson():

    jsoncardlist = json.dumps(cardlist, sort_keys=True, indent=4)

    # Print JSON to file
    try:
        f = open('cardlist.json', 'w')
        f.write(jsoncardlist)
        f.close()
    except Exception as e:
        print(str(e))

    print('Dumped to JSON file')


def main():
    url = 'http://www.hearthpwn.com/cards'
    parameters = {}
    parameters['display']=1
    parameters['page']=1
    var = getRawUrlData(url, parameters) 
    serialiseCardData(var)
    dumpDataToJson()
    

if __name__ == '__main__':
    main()
