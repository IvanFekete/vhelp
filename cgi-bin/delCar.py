import cgi,shelve,sys, blocks
from structures import dictToShelve,shelveToDict,redirect

form = cgi.FieldStorage()

print('Content-type: text/html\n')

key = int(form.keys()[0])

shlv =shelve.open("db")
db = shelveToDict(shlv)

db['storages'][db['logined'].storageID].carpark.pop(key)
dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect('http://127.0.0.1/cgi-bin/storage.py')

