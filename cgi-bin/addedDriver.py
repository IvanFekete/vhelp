import cgi,shelve, blocks
from structures import shelveToDict,dictToShelve,redirect

form = cgi.FieldStorage()

shlv = shelve.open("db")
db = shelveToDict(shlv)

firstName = form['firstName'].value
secondName = form['secondName'].value
surName = form['surName'].value
age = int(form['age'].value)
categories= form['categories'].value.split(',')
login = form['login'].value
password = form['password'].value

ID = db['logined'].storageID
db['storages'][ID].addDriver(db,firstName,secondName,surName,age,categories)
vID = db['maxVolunteerID']
db['volunteers'][vID].changeLogin(login)
db['volunteers'][vID].changePassword(password)

dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect('http://127.0.0.1/cgi-bin/storage.py')
