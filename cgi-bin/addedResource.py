import cgi,shelve, blocks
from structures import shelveToDict,dictToShelve,redirect,Resource

form = cgi.FieldStorage()



shlv = shelve.open("db")
db = shelveToDict(shlv)

code = form['code'].value
name = form['name'].value
kind = form['kind'].value
mass = float(form['mass'].value)
volume = float(form['volume'].value)
quantity = int(form['quantity'].value)
ID = db['logined'].storageID
db['storages'][ID].addResource(db,Resource(code,name,kind,mass,volume).add(quantity))

dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect('http://127.0.0.1/cgi-bin/storage.py')
