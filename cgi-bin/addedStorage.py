import cgi,shelve, blocks
from structures import *

form = cgi.FieldStorage()
address = form['address'].value
roomines = float(form['roomines'].value)
firstName = form['firstName'].value
secondName = form['secondName'].value
surName = form['surName'].value
age = int(form['age'].value)
login = form['login'].value
password = form['password'].value

shlv = shelve.open("db")
db = shelveToDict(shlv)

addStorage(db,address,roomines)
addStorageCoordinator(db,firstName,secondName,surName,age)

coordinatorsID = getID(db,firstName,secondName,surName)
storageID = getStorageID(db,address)

db['volunteers'][coordinatorsID].changeLogin(login)
db['volunteers'][coordinatorsID].changePassword(password)
db['storages'][storageID].changeCoordinator(db,coordinatorsID)


dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect('http://127.0.0.1/cgi-bin/storageList.py')

