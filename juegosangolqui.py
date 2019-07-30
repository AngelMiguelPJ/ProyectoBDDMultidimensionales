#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "QKTIxQcHXFszsxQkIuZfNhcc4"
csecret = "8YDU4mMe6m10UT9w5G0pqAEf5l0l58tBncV9wg2W5S9rQE5jyB"
atoken = "856256322735681539-wCLXpTVOoMeZQ5ZiEtG8XmBP5JwKqBi"
asecret = "4bGnY2XDcUcDNwNKYY0eA7cH1wyXN85mcwwFugPOQ07P0"

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
    db = server.create('juegosangolqui')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['quito3']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-78.493053,-0.412589,-78.386967,-0.290761])
twitterStream.filter(track = ["playstation","freefire"])