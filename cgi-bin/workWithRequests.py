import cgi,sys,shelve,blocks
from structures import *

form = cgi.FieldStorage()

shlv = shelve.open("db")
db = shelveToDict(shlv)
if(db['requests']!=[]) :
    for i in range(len(db['requests'])) :
        work = form[str(i)+'_class'].value
        storageID = int(form[str(i)+'_storage_id'].value)
        person = db['requests'][i]
        if   (work=='Volunteer') : db['storages'][storageID].addVolunteer(db,person.firstName,person.secondName,person.surName,person.age)
        elif (work=='Driver')    : db['storages'][storageID].addDriver(db,person.firstName,person.secondName,person.surName,person.age,person.categories)
    db['requests'] = []

dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect("http://127.0.0.1/cgi-bin/volunteers.py")
