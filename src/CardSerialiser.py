import json
import os
import re
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


def getRawUrlData(url, parameters):
    # Takes in URL string and parameter list
    # Returns BS4 object of webpage

    url_values = urllib.parse.urlencode(parameters)
    target_url = url
    full_url = target_url + '?' + url_values
    data = urllib.request.urlopen(full_url)
    response = data.read()
    webpagedata = BeautifulSoup(str(response))
    
    return webpagedata  # Returns BS4 object of webpage


def serialiseCardData(urldata):

    # BS4.ResultSets of each attribute
    cardname = urldata.find_all('td', {'class': 'col-name'}).text.replace('\\r\\n', '')
    cardtype = urldata.find_all('td', {'class': 'col-type'}).text
    cardclass = urldata.find_all('td', {'class': 'col-class'}).text.replace('\xa0', '')
    cardcost = urldata.find_all('td', {'class': 'col-cost'}).text
    cardattack = urldata.find_all('td', {'class': 'col-attack'}).text
    cardhealth = urldata.find_all('td', {'class': 'col-health'}).text

    # Loop to combine all attributes with key=card_name
    for i in range(len(cardname)):
        cardlist[cardname[i]] = {'class': cardclass[i], 'type': cardtype[i], 'cost': cardcost[i], 'attack': cardattack[i], 'health': cardhealth[i]}

    print('put data into cardlist')
    

def dumpDataToJson():

    # Create JSON object
    jsoncardlist = json.dumps(cardlist, sort_keys=True, indent=4)

    # Print JSON to file
    try:
        f = open('cardlist.json', 'w')
        f.write(jsoncardlist)
        f.close()
    except Exception as e:
        print(str(e))

    print('Dumped to JSON file')


def testMethod(urldata):

    soup = urldata

    #---------------------------------------
    # TODO: COMPLETE - Get names of card
    cardnamelist = soup.find_all("h3")
    for tag in cardnamelist:
        print(tag.text)
    #---------------------------------------
    # TODO: COMPLETE - Get description
    carddesc = soup.find_all("td", {'class': 'visual-details-cell'})
    for item in carddesc:
        print(item.find("p"))
    #---------------------------------------
    # TODO: COMPLETE - Get img url
    cardurllist = soup.find_all("img", class_="hscard-static")  # ['src'] = url
    for tag in cardurllist:
        print(tag['src'])
    #---------------------------------------
    # TODO: COMPLETE - Download img to directory using card name as filename
##    curdir = os.getcwd()
##    os.makedirs(curdir + '\images', exist_ok=True)
##    for i in range(len(cardimgname)):
##        name = cardimgname[i].text
##        url = cardurllist[i]['src']
##        print(name + ' ' + cardurllist)
##        fw = open('images\\' + name + '.png', 'wb')
##        imgfile = urllib.request.urlopen(url)
##        resp = imgfile.read()
##        fw.write(resp)
##        fw.close()

def main():
    url = 'http://www.hearthpwn.com/cards'
    parameters = {}
    parameters['display'] = 2
    parameters['page'] = 1
    var = getRawUrlData(url, parameters)
    testMethod(var)
    print()
    print('done')
    

if __name__ == '__main__':
    main()


