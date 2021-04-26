import cgi,shelve, blocks
from structures import shelveToDict,dictToShelve,redirect,Car

form = cgi.FieldStorage()

shlv = shelve.open("db")
db = shelveToDict(shlv)

name = form['name'].value
carrying = float(form['carrying'].value)
roomines = float(form['roomines'].value)
number = form['number'].value
category= form['category'].value

ID = db['logined'].storageID
db['storages'][ID].addCar(Car(name,carrying,roomines,category,number))

dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect('http://127.0.0.1/cgi-bin/storage.py')
