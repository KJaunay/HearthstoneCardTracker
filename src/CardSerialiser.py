import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

cardlist = {}

def getdescriptionandpicture():
    #thead > tbody > tr = CARD
    #CARD > td class=visual-image-cell = IMG
    #CARD > td class=visual-details-cell > h3 = CARDTITLE
    #CARD > td class=visual-details-cell > p = CARD DESCRIPTION

def serialisecarddata():

    for page in range(1, 10):
        data = {}
        data['display'] = 1
        data['page'] = page
        url_values = urllib.parse.urlencode(data)
        url = 'http://www.hearthpwn.com/cards'
        full_url = url + '?' + url_values
        # full_url = http://www.hearthpwn.com/cards?display=1&page=# where # is in range
        data = urllib.request.urlopen(full_url)
        respData = data.read() # source code

        '''
        #prints sourcecode to file
        try:
            f = open('sourcecode.txt', 'a')
            f.write(str(respData))
            f.close()
        except Exception as e:
            print(str(e))
        '''

        # creates a Beautiful Soup object of html webpage
        soup = BeautifulSoup(str(respData)) 

        # BS4.ResultSets of each attribute
        cardname = soup.find_all('td', {'class':'col-name'})
        cardtype = soup.find_all('td', {'class':'col-type'})
        cardclass = soup.find_all('td', {'class':'col-class'})
        cardcost = soup.find_all('td', {'class':'col-cost'})
        cardattack = soup.find_all('td', {'class':'col-attack'})
        cardhealth = soup.find_all('td', {'class':'col-health'})

        # Loop to combine all attributes with key=card_name
        for i in range(len(cardname)):
            cardlist[cardname[i].text.replace('\\r\\n', '')] = {'class':cardclass[i].text.replace('\xa0', ''), 'type':cardtype[i].text, 'cost':cardcost[i].text, 'attack':cardattack[i].text, 'health':cardhealth[i].text}

        print('completed: {0}'.format(full_url))

    jsoncardlist = json.dumps(cardlist, sort_keys=True, indent=4)

    #Print JSON to file
    try:
        f = open('cardlist.json', 'w')
        f.write(jsoncardlist)
        f.close()
    except Exception as e:
        print(str(e))

    print('Done!!')

def main():
    serialisecards()

if __name__ == '__main__':
    main()
