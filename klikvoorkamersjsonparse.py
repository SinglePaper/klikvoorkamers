import requests
import json
from pushbullet import Pushbullet
from time import sleep

def sendNotification(messages):
    API_KEY = "HIDDEN"
    pb = Pushbullet(API_KEY)

    message = "----------------------\n\n".join(messages)
    print(message)
    #pb.channels[0].push_note("Nieuwe kamers beschikbaar!",message)
    print(pb.chats)
    for chat in pb.chats:
        chat.push_note("Nieuwe kamers beschikbaar!",message)
    pb.push_note("Nieuwe kamers beschikbaar!",message)

found = []

while True:
    URL = "https://www.klikvoorkamers.nl/portal/object/frontend/getallobjects/format/json"
    data = requests.get(URL)
    data = data.json()

    messages = []

    #data = open("klikvoorkamers.json", "r")
    # data = data.read()
    # data = json.loads(data)


    dwellingTypesExclude = ["29", "30"] # = niet tijdelijk, niet parkeerplaats/berging
    modelCategorie = ["2", "3"] # = random, reactiedatum
    modelCategorieString = ["Inschrijfduur", "Loting", "Eerste reageerder"]

    for r in data["result"]:
        if(r["dwellingType"]["id"] not in dwellingTypesExclude and r["model"]["modelCategorie"]["id"] in modelCategorie):
            if(r["id"] not in found):
                found.append(r["id"])
                adres = r["street"]+" "+r["houseNumber"]+"-"+r["houseNumberAddition"]+" "+r["postalcode"]+", "+r["city"]["name"]
                prijsTotaal = r["totalRent"]
                link = "https://www.klikvoorkamers.nl/aanbod/te-huur/details/"+r["urlKey"]
                modCat = modelCategorieString[int(r["model"]["modelCategorie"]["id"])-1]
                beschikbaarPer = r["availableFromDate"]+r["availableFrom"]

                message = "" 
                message += adres+"\n\n"
                message += "Totale huurprijs: €"+str(prijsTotaal)+"\n"
                message += "Type: "+modCat+"\n"
                message += "Beschikbaar per: "+beschikbaarPer+"\n"
                message += "Link: "+link+"\n\n" 

                messages.append(message)

    sendNotification(messages)

    sleep(30.0)
