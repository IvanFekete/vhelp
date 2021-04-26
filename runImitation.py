import shelve,random,json,time
from structures import *
from urllib.request import urlopen

persons = []

class Person(object) :
	def __init__(self,firstName,secondName,surName) :
		self.firstName = firstName
		self.secondName = secondName
		self.surName = surName

fl = open("names.txt","r")
f = fl.read().split('\n')
for _ in range(280) :
	r = 41
	fullName = f[_]
	while fullName[r]==' ' : r-=1
	fullName = fullName[7:r+1]
	firstName,secondName,surName = fullName.split(' ')
	persons.append(Person(firstName,secondName,surName))
fl.close()

def getFirstName() :
	random.shuffle(firstNames)
	return firstNames[0]

def getSecondName() :
	random.shuffle(secondNames)
	return secondNames[0]

def getSurName() :
	random.shuffle(surNames)
	return surNames[0]

def getAge() :
	return random.randint(16,55)

def getEmail() :
	domains = ['gmail.com','i.ua','ukr.net','mail.ru','rambler.ru']
	random.shuffle(domains)
	l = random.randint(3,10)
	name = ""
	for _ in range(l) :
		name+=chr(ord('a')+random.randint(0,23))
	return name+'@'+domains[0]

def getPhone() :
	return "+380"+"".join([str(random.randint(0,9)) for _ in range(9)])

def getCategories() :
	categories = ["B1","B","C1","C"]
	isCategories = random.randint(0,4)
	if isCategories!=1 : return []
	r = random.randint(0,3)
	random.shuffle(categories)
	return categories[:r]

def getNote() :
	return ""

def getRandomResourcesList() :
	resourcesNames = [
	Resource("К0568","Форма","Одяг",2,0.2),
	Resource("К0568","Бронежилет","Одяг",16,0.2),
	Resource("Х0066","Хлiб","Їжа",0.5,0.05),
	Resource("R7958","РГО","Зброя",0.5,0.001),
	Resource("R8793","Ф-1","Зброя",0.5,0.001),
	Resource("X132","АK-47","Зброя",5,0.002),
	Resource("Q6237","Тепловiзор","Прилади",0.5,0.001)
	]
	random.shuffle(resourcesNames)
	resources = []
	for resource in resourcesNames :
		canAdd = random.randint(0,1)
		if canAdd : resources.append(resource.add(random.randint(0,50)))

	return resources

def getLocation() :
	locations =['Kyiv','Kharkiv','Dnipropetrovsk','Kirovohrad','Vinnytsa','Lviv','Sumi','Lutsk','Uzhhorod','Lviv']# ["Київ","Харкiв","Днiпропетровськ","Кiровоград","Вiнниця","Львiв","Суми","Луцьк","Ужгород","Львiв"]
	random.shuffle(locations)
	return locations[0]

def getStorageIndex(db) :
	return random.randint(1,db['maxStorageID'])

k = 1000000#coef


ResourcesRequests,VolunteersRequests,ResourcesRequestsCanDo,VolunteersRequestsCanDo,timeInterval = int(input("Коеф. появи заявок на ресурси : ")),int(input("Коеф. появи заявок на волонтерство : ")),int(input("Коеф. обробки заявок на ресурси : ")),int(input("Коеф. обробки заявок на волонтерство : ")),int(input("Тайм-аут затримки : "))

workList = ['vr']*VolunteersRequests+['rr']*ResourcesRequests
didVolunteersRequests = 0
didResourcesRequests = 0
while True :
	random.shuffle(workList)
	for operation in workList :
		d = shelve.open("db")
		db = shelveToDict(d)
		if operation=="vr" :
			random.shuffle(persons)
			person = persons[0]
			firstName = person.firstName
			secondName = person.secondName
			surName = person.surName
			age = getAge()
			email = getEmail()
			phone = getPhone()
			categories = getCategories()
			note = getNote()

			addRequest(db,Request(firstName,secondName,surName,age,email,phone,categories,note))

			print("Вiдправлена заявка волонтера:\n")
			print("Iм'я :%s\nПо-батьковi :%s\nПрiзвище :%s\nВiк :%s\nE-mail :%s\nНомер телефону :%s\nКатегор. прав :%s\nПримiтки :%s\n"%(firstName,secondName,surName,str(age),email,phone,','.join(categories),note))
			didVolunteersRequests+=1
			if(didVolunteersRequests==VolunteersRequestsCanDo) :
				for i in range(len(db['requests'])) :
					doRequest(db,i,getStorageIndex(db))
				db['requests'] = []
				didVolunteersRequests = 0

				print("%s заявок на волонтерство було оброблено.\n"%str(VolunteersRequestsCanDo))

		elif operation=="rr" :
			location = getLocation()
			n = random.randint(1,15)
			resources = getRandomResourcesList()
			resourcesRequest  = ResourcesRequest(location,resources)
			addResourcesRequest(db,resourcesRequest)

			print("Вiдправлена заявка на ресурси\n")
			response = "Адреса пункту потреби : %s\nКiлькiсть найменувань товару : %s\n%s"
			rootResourceString = "Назва : %s Тип : %s Кiлькiсть : %s\n"
			strings = ""
			for resource in resourcesRequest.resources :
				strings+=rootResourceString%(resource.name,resource.kind,resource.quantity)
			print(response%(resourcesRequest.location,len(resourcesRequest.resources),strings))
			didResourcesRequests+=1
			if(didResourcesRequests==ResourcesRequestsCanDo) :
				storages = []
				for key in db['storages'] :
					request = json.loads(urlopen("http://maps.google.com/maps/api/geocode/json?address=%s"%(db['storages'][key].address)).read().decode("UTF-8"))
					x = request["results"][0]["geometry"]["location"]["lat"]*k
					y = request["results"][0]["geometry"]["location"]["lng"]*k
					point = Point(x,y,db['storages'][key].address,str(db['storages'][key].ID))
					storages.append(point)
				need_points = []
				for key in range(len(db['resourcesRequests'])) :
					i = int(key)
					if i >= len(db['resourcesRequests']) : continue
					request = json.loads(urlopen("http://maps.google.com/maps/api/geocode/json?address=%s"%(db['resourcesRequests'][i].location)).read().decode("UTF-8"))
					x = request["results"][0]["geometry"]["location"]["lat"]*k
					y = request["results"][0]["geometry"]["location"]["lng"]*k
					point = Point(x,y,db['resourcesRequests'][i].location,str(i))
					need_points.append(point)
				result = hungrian_algo(db,storages,need_points)
				for (storage,need_point) in result :
					res = db['storages'][int(storage.ID)].giveRace(db,db["resourcesRequests"][int(need_point.ID)].resources)
					for pair in res :
						for resource1 in pair[3] :
							for i in range(len(db['resourcesRequests'][need_point].resources)) :
								if resource1.name==db['resourcesRequests'][need_point].resources[i].name :
									db['resourcesRequests'][need_point].resources[i].get()

				print("%s заявок на ресурси було оброблено\n"%(ResourcesRequestsCanDo))
				didResourcesRequests = 0
		dictToShelve(db,d)
		d.close()
		time.sleep(timeInterval)
	readkey = input("Продовжити сеанс? ")
	correct_answers = ['','Yes','yes','y','Y',"Так","так","т","Т","да","Да","д"]
	if readkey.lower() not in correct_answers : break



