import blocks,shelve
from structures import *

shlv = shelve.open("db")
db = shelveToDict(shlv)
blocks.startPage()
content = """<br/>"""
for person in db['volunteers'].values() :
    cval = type(person).__name__
    if cval =='MainCoordinator' :
        content+=blocks.administrator%(person.firstName,person.secondName,person.surName,str(person.age),"Головний координатор")
        content+="<br/>"
        
for person in db['volunteers'].values() :
    cval = type(person).__name__
    if cval =='HumanResourcesCoordinator' :
        content+=blocks.administrator%(person.firstName,person.secondName,person.surName,str(person.age),"Кадровий координатор")
        content+="<br/>"

for person in db['volunteers'].values() :
    cval = type(person).__name__
    if cval =='StorageCoordinator' :
            content+=blocks.storageCoordinator%(person.firstName,person.secondName,person.surName,str(person.age),db['storages'][person.storageID].address)
            content+="<br/>"

for person in db['volunteers'].values() :
    cval = type(person).__name__
    if cval =='Driver' :
        content+=blocks.driver%(person.firstName,person.secondName,person.surName,str(person.age),','.join(person.categories),db['storages'][person.storageID].address)
        content+="<br/>"
        
for person in db['volunteers'].values() :
    cval = type(person).__name__
    if cval =='Volunteer' :
        content+=blocks.volunteer%(person.firstName,person.secondName,person.surName,person.age,db['storages'][person.storageID].address)
        content+="<br/>"
        
blocks.enc_print(blocks.page%(blocks.styles,'Список волонтерів',blocks.getHeader(db['logined']),content,blocks.footer))

dictToShelve(db,shlv)
shlv.close()
