#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "3IscFBUGTNrfhjPRK8D8yXkAT"
csecret = "r3AY7HZec4CtvVMsGmgLEcb0cJvLSVjWPJ07OG7A3HruR5bc5G"
atoken = "856256322735681539-aDTdveWmj3MRULDlPnoBLcrxNTYNptN"
asecret = "DdEIM4B4Y9s128Y5v0zsl0tsqlvqNFV1gFK2uG0mxRYUv"

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
    db = server.create('juegowashington')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['quito3']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-124.84,45.54,-116.92,49.0])
twitterStream.filter(track = ["playstation","freefire"])