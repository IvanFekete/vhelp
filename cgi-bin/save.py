import cgi,shelve, blocks
from structures import dictToShelve,shelveToDict,redirect

form = cgi.FieldStorage()

shlv = shelve.open("db")
db = shelveToDict(shlv)


for name in form.keys():
    i = int(name[1:])
    if name[0]=='r' :
        for ii in range(len(db['resources'])) :
            if db['resources'][ii].name==db['storages'][db['logined'].storageID].resources[i].name :
                db['resources'][ii].quantity += int(form[name].value)-db['storages'][db['logined'].storageID].resources[i].quantity
        db['storages'][db['logined'].storageID].resources[i].quantity=int(form[name].value)
    elif name[0]=='l' :
        db['volunteers'][i].login= form[name].value
    else :
        if name[0]=='p' : db['volunteers'][i].password= form[name].value
        

dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect('http://127.0.0.1/cgi-bin/storage.py')
