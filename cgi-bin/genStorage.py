import sys,blocks,shelve,cgi
from structures import *

ID = cgi.FieldStorage().keys()[0]

shlv = shelve.open("db")
db = shelveToDict(shlv)

blocks.startPage()
blocks.enc_print(blocks.page%(blocks.styles,'Склад №'+str(ID),blocks.getHeader(db['logined']),blocks.genStorageContent(db,int(ID)),blocks.adminFooter))

dictToShelve(db,shlv)
shlv.close()