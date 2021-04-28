import shelve,sys
from contracts import contract

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
loginPasswordSymbols = alphabet + '0123456789_'

def redirect(link) :
		sys.stdout.buffer.write(('Refresh: 0; URL=%s\n'%link).encode('utf8') + b'\n')

def incVolunteerID(db) :
        db['maxVolunteerID']+=1
        return db['maxVolunteerID']
def incStorageID(db) :
        db['maxStorageID']+=1
        return db['maxStorageID']

def getID(db,firstName,secondName,surName) :
        for person in db['volunteers'].values() :
                if firstName == person.firstName and secondName == person.secondName and surName == person.surName :
                        return person.ID
        else :
                print("There aren't this coordinator")
                return 0
def getStorageID(db,address) :
        for storage in db['storages'].values() :
                if storage.address==address :
                        return storage.ID
def shelveToDict(shlv) :
        db = {}
        for key in shlv : db[key]=shlv[key]
        return db

def dictToShelve(db,shlv) :
        for el in db['resources'] :
                if el.quantity==0 : db['resources'].remove(el)
        for el in db['needs'] :
                if el.quantity==0 : db['needs'].remove(el)

        for key in db['storages'] :
                for el in db['storages'][key].resources :
                        if el.quantity==0 :
                                db['storages'][key].resources.remove(el)
        for request in db['resourcesRequests'] :
                for resource in request.resources :
                        if resource.quantity==0 : request.resources.remove(resource)
                if request.resources==[] : db['resourcesRequests'].remove(request)
        for key in db : shlv[key] = db[key]

def addNeed(db,resource) :
        for i in range(len(db['needs'])) :
                if db['needs'][i].name==resource.name :
                        db['needs'][i].quantity+=resource.quantity
                        break
        else :
                db['needs'].append(resource)

def removeNeed(db,resource) :
         for i in range(len(db['needs'])) :
                if db['needs'][i].name==resource.name :
                        if db['needs'][i].quantity>=resource.quantity :
                                db['needs'][i].quantity-=resource.quantity
                        else :
                                db['needs'][i].quantity = 0
                        break

class Request(object) :
        def __init__(self,firstName,secondName,surName,age,email,phone,categories,note) :
                self.firstName = firstName
                self.secondName = secondName
                self.surName = surName
                self.age = age
                self.email = email
                self.phone = phone
                self.categories = categories
                self.note = note
class ResourcesRequest(object) :
		def __init__(self,location,resources) :
				self.location = location
				self.resources = resources

class Resource(object) :
        def __init__(self,code,name,kind,mass,volume) :
                self.kind = kind;self.name = name;self.code = code
                self.quantity = 0
                self.mass = mass
                self.volume = volume
        
        def add(self,quantity=1) :
                self.quantity+=quantity
                return self
        def get(self,quantity=1) : 
                if self.quantity>=quantity : 
                        self.quantity-=quantity
                return self
        
class Volunteer(object) :
        def __init__(self,ID,firstName,secondName,surName,age,storageID) :
                self.ID = ID
                self.firstName = firstName
                self.secondName = secondName
                self.surName = surName
                self.age = age
                self.storageID = storageID
                self.login=''
                self.password=''

        def changeLogin(self,new) :
                contract.is_not_empty(new)
                contract.is_greater_than_or_equal(len(new), 4)
                contract.is_greater_than_or_equal(len(new), 4)
                contract.is_equal_to_any(new[0], alphabet)
                for c in new[1:]: contract.is_equal_to_any(c, loginPasswordSymbols)
                
                self.login=new
                
        def changePassword(self,new) :
                contract.is_not_empty(new)
                contract.is_greater_than_or_equal(len(new), 4)
                for c in new[1:]: contract.is_equal_to_any(c, loginPasswordSymbols)
                
                self.password=new

        def __str__(self) : return "testing_of_the_method"
                

class Driver(Volunteer) :
        def __init__(self,ID,firstName,secondName,surName,age,categories,storageID) :
                self.ID = ID
                self.firstName = firstName
                self.secondName = secondName
                self.surName = surName
                self.age = age
                self.categories = categories
                self.storageID = storageID
                self.status = "Вільний"
                self.login=''
                self.password=''
                
        def get(self) : self.status = "В дорозі"
        def retr(self) : self.status = "Вільний"

class StorageCoordinator(Volunteer) :
        def __str__(self) : return "testing_of_the_method"
        
class HumanResourcesCoordinator(object) :
        def __init__(self,ID,firstName,secondName,surName,age) :
                self.ID = ID
                self.firstName = firstName
                self.secondName = secondName
                self.surName = surName
                self.age = age
                self.login=''
                self.password=''
                
        def changeLogin(self,new) :
                self.login=new
        def changePassword(self,new) :
                self.password=new

class MainCoordinator(HumanResourcesCoordinator) :
        def __str__(self) : return "testing_of_the_method"


class Car(object) :
        def __init__(self,name,carrying,roomines,category,number) :
                self.name = name
                self.carrying = carrying
                self.roomines = roomines
                self.category = category
                self.number = number
                self.status = "Вільний"
        def get(self) : self.status = "В дорозі"
        def retr(self) : self.status = "Вільний"
class Storage(object) :
        def __init__(self,ID,address,roomines) :
                self.ID = ID
                self.address = address
                self.coordinator = None
                self.roomines = roomines
                self.volunteers = []
                self.carpark = []
                self.resources = []
        
        def addResource(self,db,resource) :
                if resource.volume*resource.quantity>self.roomines :
                        print("We haven't any place for this resource")
                        return
                self.roomines-=resource.volume*resource.quantity
                
                for i in range(len(self.resources)) :
                        if self.resources[i].name==resource.name :
                                self.resources[i].add(resource.quantity)
                                break
                else :
                        self.resources.append(resource)
                
                for i in range(len(db['resources'])) :
                        if db['resources'][i].name==resource.name :
                                db['resources'][i].add(resource.quantity)
                                break
                else :
                        db['resources'].append(resource)

                removeNeed(db,resource)
                
        def getResource(self,db,resource) :
                for i in range(len(self.resources)) :
                        if self.resources[i].name==resource.name :
                                self.roomines+=self.resources[i].volume*self.resources[i].quantity
                                self.resources[i].get(resource.quantity)
                                break
                else :
                        print("There aren't resource that you want.")
                        addNeed(db,resource)
                        return

                for i in range(len(db['resources'])) :
                        if db['resources'][i].name==resource.name :
                                db['resources'][i].get(resource.quantity)
                                break       
        
        def addVolunteer(self,db,firstName,secondName,surName,age) :
                newID = incVolunteerID(db)
                volunteer = Volunteer(newID,firstName,secondName,surName,age,self.ID)
                self.volunteers.append(newID)
                db['volunteers'][newID] = volunteer
                
        def removeVolunteer(self,db,volunteerID) :
                del db['volunteers'][volunteerID]
                self.volunteers.remove(volunteerID)

        def changeCoordinator(self,db,coordinatorID) :
                if type(db['volunteers'][coordinatorID]).__name__ != 'StorageCoordinator' :
                        print("This person is %s"%type(db['volunteers'][coordinatorID]).__name__)
                        return
                db['volunteers'][coordinatorID].storageID = self.ID
                self.coordinator = coordinatorID

        def addDriver(self,db,firstName,secondName,surName,age,categories) :
                newID = incVolunteerID(db)
                driver = Driver(newID,firstName,secondName,surName,age,categories,self.ID)
                self.volunteers.append(newID)
                db['volunteers'][newID] = driver
                                
        def removeDriver(self,db,driverID) :
                del db['volunteers'][driverID]
                self.volunteers.remove(driverID)
        
        
        def addCar(self,car) : self.carpark.append(car)

        def removeCar(self,car) : 
                if car in self.carpark : 
                        self.carpark.remove(car)
                        
        def giveRace(self,db,resourcesList) :
                resources = []
                sumM,sumV = 0,0
                for resource in resourcesList :
                        for _ in range(resource.quantity) :
                                resources.append(Resource(resource.code,resource.name,resource.kind,resource.mass,resource.volume).add())
                                sumM+=resource.mass
                                sumV+=resource.volume
                
				#BAG
                def bag(m,resources) :
                        for resource in resources :
                                for storageResource in self.resources :
                                        if storageResource.name==resource.name and storageResource.quantity>=resource.quantity : break
                                else :
                                        print("We haven't all of these resources,sorry.")
                                        return {'mass' : 0,'list' : [] }
                        n = len(resources)
                        resources = [0]+resources
                        b = [[0 for i in range(m+1)] for j in range(n+1)]
                        lst = {(0,0) : [],(0,1):[],(1,0):[]}
                        for k in range(1,n+1) :
                                for i in range(1,m+1) :
                                        if i>=resources[k].mass :
                                                if b[k-1][i-int(resources[k].mass)]+resources[k].volume>=b[k-1][i] :
                                                        b[k][i] = b[k-1][i-int(resources[k].mass)]+resources[k].volume
                                                        lst[(k,i)] = lst[(k-1,int(i-resources[k].mass))]+[resources[k]] if (k-1,int(i-resources[k].mass)) in lst.keys() else [resources[k]]
                                                else :
                                                        b[k][i] = b[k-1][i]
                                                        lst[(k,i)] = lst[(k-1,i)]
                                        else :
                                                b[k][i] = b[k-1][i]
                                                lst[(k,i)] = lst[(k-1,i)]

                        return {'mass' : b[n][m],'list' : lst[(n,m)] }
				#giving races
                pairs = []
                while resources!=[] :
						#initialization
                        deltaM = 10**18
                        myCar = None
                        haveCategory = []
                        for car in self.carpark :
                                if abs(car.carrying-sumM)<deltaM and car.status=="Вільний" :
                                        deltaM = abs(car.carrying-sumM)
                                        myCar = car
                        if myCar is None : break
                        #getting a car and a driver
                        for i in range(len(self.carpark)) :
                                if self.carpark[i]==myCar :
                                        self.carpark[i].get()

                        for i in self.volunteers :
                                if type(db['volunteers'][i]).__name__=='Driver' :
                                        db['volunteers'][i].get()
                                        volIndex= i;break
                        
						#getting resources
                        if myCar.carrying>sumM :
                                for resource in resources :
                                        self.getResource(db,resource)
                                pairs.append((db['volunteers'][volIndex],myCar,sumM,resources))
                                break
                        else :
                                result = bag(int(sumM),resources)
                                sumM-=result['mass']
                                pairs.append((db['volunteers'][volIndex],myCar,result['mass'],bag['list']))
                                for resource in result['list'] :
                                        self.getResource(db,resource);resources.remove(resource)
                return pairs

def addStorage(db,address,roomines) :
        contract.is_not_empty(address)
        contract.is_greater_than(roomines, 0)
                
        newID = incStorageID(db)
        db['storages'][newID] = Storage(newID,address,roomines)
        
def addStorageCoordinator(db,firstName,secondName,surName,age) :
        contract.is_not_empty(firstName)
        contract.is_not_empty(secondName)
        contract.is_not_empty(surName)
        contract.is_greater_than(age, 17)
        
        newID = incVolunteerID(db)
        db['volunteers'][newID] = StorageCoordinator(newID,firstName,secondName,surName,age,-1)

def addHumanResourcesCoordinator(db,firstName,secondName,surName,age) :
        contract.is_not_empty(firstName)
        contract.is_not_empty(secondName)
        contract.is_not_empty(surName)
        contract.is_greater_than(age, 17)
        
        cnt = 0
        for person in db['volunteers'].values() :
                cnt+= type(person).__name__=='HumanResourcesCoordinator'
        if cnt>=2 :
                print('There are too many human resources coordinators,sorry')
                return False
        newID = incVolunteerID(db)
        db['volunteers'][newID] = HumanResourcesCoordinator(newID,firstName,secondName,surName,age)
        return True

def addMainCoordinator(db,firstName,secondName,surName,age) :
        contract.is_not_empty(firstName)
        contract.is_not_empty(secondName)
        contract.is_not_empty(surName)
        contract.is_greater_than(age, 17)
        
        for person in db['volunteers'].values() :
                if type(person).__name__=='MainCoordinator'  :
                        print('There are main coordinators')
                        return False
        newID = incVolunteerID(db)
        db['volunteers'][newID] = MainCoordinator(newID,firstName,secondName,surName,age)
        return True

def changeMainCoordinator(db,firstName,secondName,surName,age) :
        contract.is_not_empty(firstName)
        contract.is_not_empty(secondName)
        contract.is_not_empty(surName)
        contract.is_greater_than(age, 17)
        
        for person in db['volunteers'].values() :
                if type(person).__name__=='MainCoordinator' :
                        db['volunteers'][person.ID] = MainCoordinator(person.ID,firstName,secondName,surName,age)
                        return 0
        else :
                addMainCoordinator(db,firstName,secondName,surName,age)
                return 1

def addRequest(db,request) :
        db['requests'].append(request)

def doRequest(db,requestIndex,storageID) :
        if db['requests'][requestIndex].categories==[] :
                db['storages'][storageID].addVolunteer(db,db['requests'][requestIndex].firstName,db['requests'][requestIndex].secondName,db['requests'][requestIndex].surName,db['requests'][requestIndex].age)
        else :
                db['storages'][storageID].addDriver(db,db['requests'][requestIndex].firstName,db['requests'][requestIndex].secondName,db['requests'][requestIndex].surName,db['requests'][requestIndex].age,db['requests'][requestIndex].categories)

def addResourcesRequest(db,request) :
		db['resourcesRequests'].append(request)


#MADYAR ALGO
class Point(object) :
        def __init__(self,x,y,location,ID) :
                self.x = x;self.y = y;self.location = location;self.ID = ID
        def __str__(self) :
                return "<h1>Location: %s</h1></br><h1>ID: %s</h1><br /><h1> Coordinates:\n</h1><br /><h1>X:%s  Y%s</h1>"%(self.location,str(self.ID),str(self.x),str(self.y))
dist = lambda a,b : (a.x-b.x)**2+(a.y-b.y)**2

def hungrian_algo(db,storages,need_points) :
        #preview
        INF = 10**9
        storages = [Point(0,0,"_",0)]+storages
        need_points = [Point(0,0,"_",0)]+need_points
        n,m = len(storages)-1,len(need_points)-1

        a = [[INF for i in range(max(n,m)+1)] for j in range(max(n,m)+1)]
        for i in range(1,n+1) :
                for j in range(1,m+1) :
                        for resource1 in db['storages'][int(storages[i].ID)].resources :
                                for resource2 in db['resourcesRequests'][int(need_points[j].ID)].resources :
                                        if(resource1.name==resource2.name) :
                                                a[i][j] = dist(storages[i],need_points[j])
                                                break
        mm = m
        m = max(n,m)

        maxCoord = 181
        u = [0 for i in range(maxCoord)]
        v = [0 for i in range(maxCoord)]
        p = [0 for i in range(maxCoord)]
        way = [0 for i in range(maxCoord)]
        for i in range(1,n+1) :
                p[0] = i
                j0 = 0
                minv = [INF for i in range(maxCoord)]
                used = [False for i in range(maxCoord)]
                while True :
                        used[j0] = True
                        i0 = p[j0]
                        j1 = 0
                        delta = INF
                        for j in range(1,m+1) :
                                if not used[j] :
                                        cur = a[i0][j]-u[i0]-v[j]
                                        if cur<minv[j] :
                                                minv[j] = cur;way[j] = j0
                                        if delta>minv[j] :
                                                delta = minv[j];j1 = j

                        for j in range(m+1) :
                                if used[j] : u[p[j]]+=delta;v[j]-=delta
                                else : minv[j]-=delta
                        j0 = j1

                        if p[j0]==0 : break

                while True :
                        j1 = way[j0]
                        p[j0] = p[j1]
                        j0 = j1

                        if j0==0 : break

        ans = [0 for i in range(n+1)]
        for j in range(1,n+1) :
                ans[p[j]] = j
        response = []
        for i in range(1,n+1) :
                if(ans[i]<=mm) : response.append((storages[i],need_points[ans[i]]))

        return response
