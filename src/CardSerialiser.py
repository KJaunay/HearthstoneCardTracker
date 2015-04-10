import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def serialiseCards():

    cardList = {}

    for page in range(1,10):
        data = {}
        data['display'] = 1
        data['page'] = page
        url_values = urllib.parse.urlencode(data)
        url = 'http://www.hearthpwn.com/cards'
        full_url = url + '?' + url_values
        # full_url = http://www.hearthpwn.com/cards?display=1&page=# where # is in range
        data = urllib.request.urlopen(full_url)
        respData = data.read() #source code

        '''
        #prints sourcecode to file
        try:
            f = open('sourcecode.txt', 'a')
            f.write(str(respData))
            f.close()
        except Exception as e:
            print(str(e))
        '''

        #creates a Beautiful Soup object of html webpage
        soup = BeautifulSoup(str(respData)) 

        #BS4.ResultSets of each attribute
        cardName = soup.find_all('td', {'class':'col-name'})
        cardType = soup.find_all('td', {'class':'col-type'})
        cardClass = soup.find_all('td', {'class':'col-class'})
        cardCost = soup.find_all('td', {'class':'col-cost'})
        cardAttack = soup.find_all('td', {'class':'col-attack'})
        cardHealth = soup.find_all('td', {'class':'col-health'})

        #Loop to combine all attributes with key=card_name
        for i in range(len(cardName)):
            cardList[(cardName[i].text).replace('\\r\\n', '')] = {'class':cardClass[i].text.replace('\xa0', ''), 'type':cardType[i].text, 'cost':cardCost[i].text, 'attack':cardAttack[i].text, 'health':cardHealth[i].text}

        print('completed: {0}'.format(full_url))

    var = json.dumps(cardList, sort_keys=True, indent=4)

    #Print JSON to file
    try:
        f = open('cardlist.json', 'w')
        f.write(var)
        f.close()
    except Exception as e:
        print(str(e))

    print('Done!!')

def main():
    serialiseCards()

if __name__ == '__main__':
    main()