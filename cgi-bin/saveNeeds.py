import cgi,shelve, blocks
from structures import *

form = cgi.FieldStorage()

shlv = shelve.open("db")
db = shelveToDict(shlv)

for key in form.keys() :
    db['needs'][int(key)].quantity = int(form[key].value)

dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect("http://127.0.0.1/cgi-bin/needs.py")