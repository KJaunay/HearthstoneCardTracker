import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


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

def getRawUrlData(url, numpages, displaytype):

    for page in range(1, numpages):
        parameters = {}
        parameters['display'] = displaytype
        parameters['page'] = page
        url_values = urllib.parse.urlencode(parameters)
        geturl = url
        full_url = geturl + '?' + url_values
        data = urllib.request.urlopen(full_url)
        response = data.read()
        soup = BeautifulSoup(str(response))
        print('got stuff from the net yo!')
        return soup


def getcarddata(urldata):

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

def getcardimganddescription(urldata):

    # thead > tbody > tr = CARD
    # CARD > td class=visual-image-cell > img class="hscard-static" src = IMG
    # CARD > td class=visual-details-cell > h3 = CARDTITLE
    # CARD > td class=visual-details-cell > p = CARD DESCRIPTION

    cardimg = urldata.find_all('')
    carddesc = urldata.find_all('')

    print('finished getting img and cardlist')

def dumpdatatojson():

    jsoncardlist = json.dumps(cardlist, sort_keys=True, indent=4)

    # Print JSON to file
    try:
        f = open('cardlist.json', 'w')
        f.write(jsoncardlist)
        f.close()
    except Exception as e:
        print(str(e))

    print('Dumped to JSON file!!')


def main():
    print('main method')

if __name__ == '__main__':
    main()
