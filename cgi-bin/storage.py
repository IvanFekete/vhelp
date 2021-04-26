import shelve,blocks,sys
from structures import *

#content patterns

page=""" <div style='Background-color:gold;width:90%;border-radius:10px;height:200px;padding:20px;margin-top:20px;margin-left:3%;'>
		<h1 style='font-size:48px;color:blue;'>Склад № $ID$ </h1>
		<h2 style='color:blue'>Завідувач складу: $MainCoord$ </h2><h2 style='color:blue; '>Вільне місце: $Roomines$ куб. м</h2>
		</div>
		
		<div style='padding:20px;background-color:gold;margin-top:20px;margin-left:3%;width:90%;'>
	<table  border='2px' class='tableadmin'>
				<h2 style='margin-left:15px; color:blue;'>Ресурси</h2>
				<tr class='string'>
					<td width='250px' height='25px'>Назва</td>
					<td width='190px'>Тип</td>
					<td width='150px'>Кількість</td>
					<td width='50px'>Вага</td>
					<td width='50px'>Об'єм</td>
				</tr>	
				$Resources$
	</table>
	</div>
		
	<div style='padding:20px;background-color:gold;margin-top:20px;margin-left:3%;width:90%;'>
	<table  border='2px' class='tableadmin'>
				<h2 style='margin-left:15px; color:blue;'>Волонтери</h2>
				<tr class='string'>
					<td width='200px' height='25px'>Ім'я</td>
					<td width='200px'>По-батькові</td>
					<td width='200px'>Прізвище</td>
					<td width='80px'>Вік</td>
				</tr>
				$Volunteers$
				
	</table>
	</div>

	
	<div style='padding:20px;background-color:gold;margin-top:20px;margin-left:3%;width:90%;'>
	<table  border='2px'  style='border-collapse:collapse;border-color:blue;'>
				<h2 style='margin-left:10px; color:blue;'>Водії</h2>
			     <tr class='string'>
					<td width='200px' height='25px'>Ім'я</td>
					<td width='200px'>По-батькові</td>
					<td width='200px'>Прізвище</td>
					<td width='80px'>Вік</td>
					<td width='150px'>Категорії</td>	
					<td width='180px'>Статус</td>					
				</tr>
			    $Drivers$
				
	</table>
	</div>
	<div style='padding:20px;background-color:gold;margin-top:20px;margin-left:3%;width:90%;'>
	<table  border='2px' class='tableadmin'>
				<h2 style='margin-left:15px; color:blue;'>Автопарк</h2>
				<tr class='string'>
					<td width='180px' height='25px'>Марка</td>
					<td width='100px'>Категорія</td>
					<td width='180px'>Вантажопідйомність</td>
					<td width='100px'>Місткість</td>
					<td width='240px'>Статус</td>
				</tr>	
				$Carpark$
	</table>
	</div>"""

#root strings
rootVolunteersString = """
    <tr class='string'>
					<td width='200px' height='20px'>%s</td>
					<td width='200px'>%s</td>
					<td width='200px'>%s</td>
					<td width='80px'>%s</td>
				</tr>
    """

rootDriversString = """
    <tr class='string'>
					<td width='200px' height='20px'>%s</td>
					<td width='200px'> %s </td>
					<td width='200px'> %s </td>
					<td width='80px'> %s </td>
					<td width='150px'> %s </td>	
				</tr>
    """

rootCarsString = """
    <tr class='string'>
					<td width='320px' height='20px'>%s</td>
					<td width='100px'>%s</td>
					<td width='200px'>%s</td>
					<td width='200px'>%s</td>
					<td width='80px'>%s</td>
				</tr>
    """
rootResourcesString = """
	<tr class='string'>
					<td width='280px' height='25px'>%s</td>
					<td width='200px'>%s</td>
					<td width='150px'>%s</td>
					<td width='150px'>%s</td>
					<td width='150px'>%s</td>
				</tr>	

"""

adminPage ="""
        <form action="save.py" method="post">
        <div style='Background-color:gold;width:90%;border-radius:10px;height:200px;padding:20px;margin-top:20px;margin-left:3%;'>
		<h1 style='font-size:48px;color:blue;'>Склад № $ID$ </h1>
		<h2 style='color:blue'>Завідувач складу: $MainCoord$ </h2>
		<h2 style='color:blue;'>Вільне місце: $Roomines$ куб. м</h2>
		</div>
		
		<div class='not'>
	<table  border='2px' width='100%' class='tableadmin'>
				<h2 style='margin-left:15px; color:blue;'>Ресурси</h2>
				<tr class='string'>
				        <td width='50px'>Код</td>
					<td width='280px' height='25px'>Назва</td>
					<td width='200px'>Тип</td>
					<td width='100px'>Кількість</td>
					<td width='150px'>Вага</td>
					<td width='150px'>Об'єм</td>
				</tr>	
					
				$Resources$
				
	</table>
	<a href='addResource.py'><input charset="cp1251" type="button"
                                       style='height:20pt;font:14pt sans-serif; margin: 2pt; margin-right: 0%;text-align:center;margin-top:20px;
                                       background-color:blue;color:white;border-collapse:collapse;' value="Додати"></a>
	</div>
	</div>
		
	<div class='not'>
	<table  border='2px' width='100%' class='tableadmin'>
				<h2 style='margin-left:15px; color:blue;'>Волонтери</h2>
				<tr class='string'>
				        <td width='50px'>ID</td>
					<td width='200px' height='25px'>Ім'я</td>
					<td width='200px'>По-батькові</td>
					<td width='200px'>Прізвище</td>
					<td width='80px'>Вік</td>
					<td width='80px'>Логін</td>
					<td width='80px'>Пароль</td>
				</tr>
				
				
				$Volunteers$
				
	</table>
	<a href='addVolunteer.py'><input charset="cp1251" type="button"
                                       style='height:20pt;font:14pt sans-serif; margin: 2pt; margin-right: 0%;text-align:center;margin-top:20px;
                                       background-color:blue;color:white;border-collapse:collapse;' value="Додати"></a>
	</div>
	</div>

	
	<div class='not'>
	<table  border='2px' width='100%' style='border-collapse:collapse;border-color:blue;'>
				<h2 style='margin-left:10px; color:blue;'>Водії</h2>
			     <tr class='string'>
			                <td width='50px'>ID</td>
					<td width='200px' height='25px'>Ім'я</td>
					<td width='200px'>По-батькові</td>
					<td width='200px'>Прізвище</td>
					<td width='80px'>Вік</td>	
					<td width='180px'>Статус</td>
					<td width='80px'>Логін</td>
					<td width='80px'>Пароль</td>
				</tr>
				 
			    $Drivers$
				
	</table>
	<a href='addDriver.py'><input charset="cp1251" type="button"
                                       style='height:20pt;font:14pt sans-serif; margin: 2pt; margin-right: 0%;text-align:center;margin-top:20px;
                                       background-color:blue;color:white;border-collapse:collapse;' value="Додати"></a>
	</div>
	</div>
	<div class='not'>
	<table  border='2px' width='100%' class='tableadmin'>
				<h2 style='margin-left:15px; color:blue;'>Автопарк</h2>
				<tr class='string'>
					<td width='180px' height='25px'>Марка</td>
					<td width='100px'>Категорія</td>
					<td width='180px'>Вантажопідйомність</td>
					<td width='100px'>Місткість</td>
					<td width='240px'>Статус</td>
					<td width='50px'>№</td>
				</tr>		
				$Carpark$
	</table>
	<a href='addCar.py'><input charset="cp1251" type="button"
                                       style='height:20pt;font:14pt sans-serif; margin: 2pt; margin-right: 0;text-align:center;margin-top:20px;
                                       background-color:blue;color:white;border-collapse:collapse;' value="Додати"></a>

	</div>
	<div class="not">
		<input charset="cp1251" type="button" onclick="document.location.href='http://127.0.0.1/cgi-bin/giveRace.py';" value="Відправити рейс"
                                       style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:20px;
                                       background-color:blue;color:white;border-collapse:collapse;' />
        <input charset="cp1251" type="submit"
                                       style='height:20pt;font:14pt sans-serif;margin-left:3px; text-align:center;margin-top:20px;
                                       background-color:blue;color:white;border-collapse:collapse;' value="Зберегти зміни" />
	</div>
        </form>
"""

rootAdminResourcesString = """
        <tr class='string'>
                                        <td width='50px'>%s</td>
					<td width='290px' height='25px'>%s</td>
					<td width='210px'>%s</td>
					<td width='110px'><input charset="cp1251" style='text-align:center;' type="text" size="11" value="%s" name="%s"></td>
					<td width='160px'>%s</td>
					<td width='160px'>%s</td>
					<td width='80px'><form action="delResource.py" method="post"><input charset="cp1251" type="submit"
                                       style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:0;
                                       background-color:blue;color:white;border-collapse:collapse;float:right;' value="Видалити" name="%s"></form></td>
        </tr>
				
"""

rootAdminVolunteersString = """
        <tr class='string'>
                                        <td width='50px'>%s</td>
					<td width='220px' height='20px'>%s</td>
					<td width='220px'>%s</td>
					<td width='220px'>%s</td>
					<td width='80px'>%s</td>
					<td width='100px'><input charset="cp1251" style='text-align:center;' type="text" size="12" value="%s" name="%s"></td>
					<td width='100px'><input charset="cp1251" style='text-align:center;' type="text" size="12" value="%s" name="%s"></td>
					<td width='80px'><form action="delVolunteer.py" method="post"><input charset="cp1251" type="submit"
                                       style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:0;
                                       background-color:blue;color:white;border-collapse:collapse;float:right;' value="Видалити" name="%s"></form></td>
        </tr>

"""

rootAdminDriversString = """
        <tr class='string'>
					<td width='50px'>%s</td>
					<td width='200px' height='20px'>%s</td>
					<td width='200px'> %s </td>
					<td width='200px'> %s </td>
					<td width='80px'> %s </td>
					<td width='150px'> %s </td>	
					<td width='80px'><input charset="cp1251" style='text-align:center;' type="text" size="10" value="%s" name="%s" /></td>
					<td width='80px'><input charset="cp1251" style='text-align:center;' type="text" size="10" value="%s" name="%s" /></td>
					<td width='80px'><form action="delDriver.py" method="post"><input charset="cp1251" type="submit"
                                       style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:0;
                                       background-color:blue;color:white;border-collapse:collapse;float:right;' value="Видалити" name="%s"></form></td>
        </tr>
				
"""

rootAdminCarsString = """
        <tr class='string'>
					<td width='320px' height='20px'>%s</td>
					<td width='100px'>%s</td>
					<td width='200px'>%s</td>
					<td width='200px'>%s</td>
					<td width='80px'>%s</td>
					<td width='50px'>%s</td>
					<td width='80px'><form action="delCar.py" method="post"><input charset="cp1251" type="submit"
                                       style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:0;
                                       background-color:blue;color:white;border-collapse:collapse;float:right;' value="Видалити" name="%s"></form></td>
        </tr>
				
"""


#generation of the content
blocks.startPage()

resources = """"""
volunteers = """"""
drivers = """"""
carpark = """"""

shlv = shelve.open("db"
				   )
db = shelveToDict(shlv)
if type(db['logined']).__name__=='StorageCoordinator' :
        ID = db['logined'].storageID
        
        storage = db['storages'][ID]

        for resourceI in range(len(storage.resources)) :
                resource = storage.resources[resourceI]
                resources+=rootAdminResourcesString%(resource.code,resource.name,resource.kind,str(resource.quantity),'r'+str(resourceI),str(resource.mass),str(resource.volume),str(resourceI))
        for volunteerID in storage.volunteers :
            volunteer = db['volunteers'][volunteerID]
            if type(volunteer).__name__=='Volunteer' :
                    volunteers+=rootAdminVolunteersString%(str(volunteer.ID),volunteer.firstName,volunteer.secondName,volunteer.surName,str(volunteer.age),volunteer.login,'l'+str(volunteer.ID),volunteer.password,'p'+str(volunteer.ID),str(volunteer.ID))
        for driverID in storage.volunteers :
            driver = db['volunteers'][driverID]
            if type(driver).__name__=='Driver' : drivers+=rootAdminDriversString%(str(driver.ID),driver.firstName,driver.secondName,driver.surName,str(driver.age),driver.status,driver.login,'l'+str(driver.ID),driver.password,'p'+str(driver.ID),str(driver.ID))
        for i in range(len(storage.carpark)) :
                car = storage.carpark[i]
                carpark+=rootAdminCarsString%(car.name,car.category,str(car.carrying),str(car.roomines),car.status,car.number,str(i))

        db['storages'][ID] = storage



        page=adminPage.replace('$ID$',str(ID))
        page=page.replace('$MainCoord$',' '.join([db['volunteers'][storage.coordinator].firstName,db['volunteers'][storage.coordinator].secondName,db['volunteers'][storage.coordinator].surName]))
        page=page.replace('$Roomines$',str(int(storage.roomines)))
        page=page.replace('$Resources$',resources)
        page=page.replace('$Volunteers$',volunteers)
        page=page.replace('$Drivers$',drivers)
        page=page.replace('$Carpark$',carpark)

        blocks.enc_print(blocks.page%(blocks.styles,'Cклад № %s'%str(ID),blocks.storageCoordinatorsHeader,page,blocks.adminFooter))
        
elif type(db['logined']).__name__ =='Volunteer' or type(db['logined']).__name__ =='Driver':
        ID = db['logined'].storageID
        storage = db['storages'][ID]

        for resource in storage.resources :
                resources+=rootResourcesString%(resource.name,resource.kind,str(resource.quantity),str(resource.mass),str(resource.volume))
        for volunteerID in storage.volunteers :
            volunteer = db['volunteers'][volunteerID]
            if type(volunteer).__name__=='Volunteer' : volunteers+=rootVolunteersString%(volunteer.firstName,volunteer.secondName,volunteer.surName,str(volunteer.age))
        for driverID in storage.volunteers :
            driver = db['volunteers'][driverID]
            if type(driver).__name__=='Driver' : drivers+=rootDriversString%(driver.firstName,driver.secondName,driver.surName,str(driver.age),driver.status)
        for car in storage.carpark :
            carpark+=rootCarsString%(car.name,car.category,str(car.carrying),str(car.roomines),car.status)

        db['storages'][ID] = storage



        page=page.replace('$Header$','')
        page=page.replace('$ID$',str(ID))
        page=page.replace('$MainCoord$',' '.join([db['volunteers'][storage.coordinator].firstName,db['volunteers'][storage.coordinator].secondName,db['volunteers'][storage.coordinator].surName]))
        page=page.replace('$Roomines$',str(int(storage.roomines)))
        page=page.replace('$Resources$',resources)
        page=page.replace('$Volunteers$',volunteers)
        page=page.replace('$Drivers$',drivers)
        page=page.replace('$Carpark$',carpark)
        
        blocks.enc_print(blocks.page%(blocks.styles,'Cклад № %s'%str(ID),blocks.getHeader(db['logined']),page,blocks.adminFooter))

else :
        if type(db['logined']).__name__=='HumanResourcesCoordinator' :
                redirect('http://127.0.0.1/cgi-bin/requests.py')
        elif type(db['logined']).__name__=='MainCoordinator':
                redirect('http://127.0.0.1/cgi-bin/globalResources.py')
        else :
                if db['logined'] is None : redirect('http://127.0.0.1/cgi-bin/login.py')
                else : redirect('http://127.0.0.1/cgi-bin/index.py')

dictToShelve(db,shlv)
shlv.close()
