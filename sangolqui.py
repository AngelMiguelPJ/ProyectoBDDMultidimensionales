#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "bO45hxub4Qe7Rq5HJQK4sYvA6"
csecret = "kMvFkR8ztUqf5sllfIGGjtN4wSRWOzOEPZdTBlgHqRyPf65fT1"
atoken = "856256322735681539-y8R5tp4pLXqPjnBcUZtRZL5G1mBS39e"
asecret = "8ZkNSgn6pcSscetSSRazhFTGzwc8kveVfKSVISF6tlSjq"

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
    db = server.create('tomorrowland')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['quito3']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(locations=[-124.84,45.54,-116.92,49.0])
twitterStream.filter(track = ["tomorrowland"])