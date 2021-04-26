import cgi,shelve,blocks
from structures import *

form=cgi.FieldStorage()

firstName  = form['firstName'].value
secondName = form['secondName'].value
surName = form['surName'].value
age = int(form['age'].value)
email = form['email'].value
phone = form['phone'].value
categories = []
for category in ["B","C1","C","D1","D"] :
    if category in form.keys() : categories.append(category)
note = form['note'].value if 'note'in form.keys() else ""

shlv = shelve.open("db")
db = shelveToDict(shlv)

db['requests'].append(Request(firstName,secondName,surName,age,email,phone,categories,note))

blocks.startPage()
blocks.enc_print(blocks.page%(blocks.styles+'<meta http-equiv="refresh" content="4;URL=http://127.0.0.1/cgi-bin/index.py">','Дякуємо за відправлення',blocks.header,blocks.thanksContent,blocks.footer))

dictToShelve(db,shlv)
shlv.close()
