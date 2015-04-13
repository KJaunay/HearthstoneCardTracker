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
    print('get raw url data - BEGIN')
    url_values = urllib.parse.urlencode(parameters)
    target_url = url
    full_url = target_url + '?' + url_values
    data = urllib.request.urlopen(full_url)
    response = data.read()
    webpagedata = BeautifulSoup(str(response))
    print('get raw url data - FINISHED')
    return webpagedata  # Returns BS4 object of webpage


def serialiseCardData(urldata):

    print('serialiseCardData - BEGIN')

    # BS4.ResultSets of each attribute
    cardname = urldata.find_all('td', {'class': 'col-name'})
    cardtype = urldata.find_all('td', {'class': 'col-type'})
    cardclass = urldata.find_all('td', {'class': 'col-class'})
    cardcost = urldata.find_all('td', {'class': 'col-cost'})
    cardattack = urldata.find_all('td', {'class': 'col-attack'})
    cardhealth = urldata.find_all('td', {'class': 'col-health'})

    # Loop to combine all attributes with key=card_name
    for i in range(len(cardname)):
        cardlist[cardname[i].text.replace('\\r\\n', '')] = {'class': cardclass[i].text.replace('\xa0', ''), 'type': cardtype[i].text, 'cost': cardcost[i].text, 'attack': cardattack[i].text, 'health': cardhealth[i].text}

    print('serialiseCardData - FINISHED')


def testMethod(urldata):

    soup = urldata

    print('test method - BEGIN')
    #---------------------------------------
    # TODO: COMPLETE - Get names of card
    cardnamelist = soup.find_all("h3")
    # for tag in cardnamelist:
    #     print(tag.text)
    #---------------------------------------
    # TODO: COMPLETE - Get description
    carddesc = soup.find_all("td", {'class': 'visual-details-cell'})
    # for item in carddesc:
    #     print(item.find("p"))
    #---------------------------------------
    # TODO: COMPLETE - Get img url
    cardurllist = soup.find_all("img", class_="hscard-static")  # ['src'] = url
    # for tag in cardurllist:
    #     print(tag['src'])
    #---------------------------------------
    # TODO: COMPLETE - Download img to directory using card name as filename
    curdir = os.getcwd()
    os.makedirs(curdir + '\images', exist_ok=True)
    for i in range(len(cardnamelist)):
        # desc = carddesc[i].find("p")
        desc = re.sub(r'<((/?[bp])|(br/))>', '', str(carddesc[i].find("p")))
        name = cardnamelist[i].text
        url = cardurllist[i]['src']
        #cardlist[name] = {'description': desc, 'img': url}

        cardlist[name]['description'] = desc
        #cardlist[name]['url'] = url

        if not os.path.isfile('images\\' + name + '.png'):
            fw = open('images\\' + name + '.png', 'wb')
            imgfile = urllib.request.urlopen(url)
            resp = imgfile.read()
            fw.write(resp)
            fw.close()

    print('test method - FINISHED')


def dumpDataToJson():

    print('Dumping to JSON file - BEGIN')
    # Create JSON object
    jsoncardlist = json.dumps(cardlist, sort_keys=True, indent=4)

    # Print JSON to file
    try:
        f = open('cardlist.json', 'w')
        f.write(jsoncardlist)
        f.close()
    except Exception as e:
        print(str(e))

    print('Dumping to JSON file - FINISHED')


def main():

    url = 'http://www.hearthpwn.com/cards'
    parameters = {}

    # TODO: repeat for all pages
    for pagenumber in range(1, 10):
        # name, cost etc
        parameters['display'] = 1
        parameters['page'] = pagenumber
        var = getRawUrlData(url, parameters)
        serialiseCardData(var)

        # url + desc
        parameters['display'] = 2
        parameters['page'] = pagenumber
        var = getRawUrlData(url, parameters)
        testMethod(var)

    dumpDataToJson()


if __name__ == '__main__':
    main()


