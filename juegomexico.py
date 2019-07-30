#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "zhw9tyRRvR5IGbQw91Bf7GP1E"
csecret = "8WzWViLnPoeMSYPd4ud7LHaXiuIuNpDtiUWgRo9LAu2TaciC5J"
atoken = "856256322735681539-R7Rqr8yDdKzSt6UJoSS0HVRxYL22fwv"
asecret = "1H3k0IMizootkRfoRFuknnehYdq7cVsb25sPUV5nO4EVG"

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('juegomexico')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['quito3']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-101.16,21.62,-98.85,24.03])
twitterStream.filter(track = ["playstation","freefire"])