import blocks,sys,shelve,cgi
from structures import *

form = cgi.FieldStorage()
location = form['location'].value
n = int(form['n'].value)
resources = []
for i in range(n) :
	code = form[str(i)+'code'].value
	name = form[str(i)+'name'].value
	kind = form[str(i)+'kind'].value
	quantity = int(form[str(i)+'quantity'].value)
	resources.append(Resource(code,name,kind,-1,-1).add(quantity))
d = shelve.open("db")
db = shelveToDict(d)
addResourcesRequest(db,ResourcesRequest(location,resources))
dictToShelve(db,d)
d.close()

blocks.startPage()
blocks.enc_print(blocks.page%(blocks.styles+'<meta http-equiv="refresh" content="4;URL=http://127.0.0.1/cgi-bin/index.py">','Дякуємо за відправлення',blocks.header,blocks.thanksContent,blocks.footer))