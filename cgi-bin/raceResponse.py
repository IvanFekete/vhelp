import cgi,shelve,blocks,sys,random
from structures import *

form = cgi.FieldStorage()
resources = []

shlv = shelve.open("db")
db = shelveToDict(shlv)

ID = db['logined'].storageID
location2 = form['sendLocation'].value.replace(" ","+")
location1 = db['storages'][ID].address.replace(" ","+")


for key in form.keys() :
    if key=="sendLocation" : continue

    resource = db['storages'][ID].resources[int(key)]
    resource = Resource(resource.code,resource.name,resource.kind,resource.mass,resource.volume).add(int(form[key].value))
    resources.append(resource)

responses= db['storages'][ID].giveRace(db,resources)



page = """
<html>
    <head>
		%s
        <title>%s</title>
        
        
	<meta charset=utf-8 />	
        
        <script src="https://maps.google.com/maps/api/js?v=3.exp&sensor=false"></script>
        <script>
            
            var map, directionsService;
            
            
            function renderDirections(result, polylineOpts) {
            
                    var directionsRenderer = new google.maps.DirectionsRenderer();
                    directionsRenderer.setMap(map);

                    if(polylineOpts) {
                    
                            directionsRenderer.setOptions({
                            
                                    polylineOptions: polylineOpts
                            
                            });
                    }

                    directionsRenderer.setDirections(result);
            }

            function requestDirections(start, end, polylineOpts) {
                    
                    directionsService.route({
                    
                            origin: start,
                            destination: end,
                            travelMode: google.maps.DirectionsTravelMode.DRIVING
                    
                    }, function(result) {
                    
                            renderDirections(result, polylineOpts);
                    
                    });
            }
            

            function initialize() {            

                    var mapOptions = {
                    
                            zoom: 5,
                            center: new google.maps.LatLng(49.0177587,31.4532138),
                            mapTypeId: google.maps.MapTypeId.ROADMAP
                    
                    };
                    
                    map = new google.maps.Map(document.getElementById('map-canvas'),    mapOptions);
                    directionsService = new google.maps.DirectionsService();


                    setTimeout(function() {
                    
                        map.setZoom(5);
                    
                    }, 2000);

            }
            
            function Roadmap() {

                    var start, end;
                    
                    initialize();
                    end = document.getElementsByName("f")[0].value;
                    start = document.getElementsByName("s")[0].value;
                    requestDirections(start, end);
                
            }

            google.maps.event.addDomListener(window, 'load', initialize);
            
        </script>
    </head>
    <body bgcolor="darkblue" onload="Roadmap();">
	
    %s
        %s
		
            %s
    </body>
</html>





"""


raceResponsePage = """
		<div class='not2'>
			
				<input charset="cp1251" type="text" name="f" id="start" value="%s"/>

				<input charset="cp1251" type="text" name="s" id="end" value="%s"/>
			<br />
			<a href="https://www.google.com.ua/maps/dir/%s/%s" target="blank">Переглянути маршрути у повному розмірі</a>
				<table  border='2px' width='80px' class='tableadmin'>
				<h1 style='color:blue;'>Звіт</h1>
					<tr class='string'>
						<td width='80px' height='25px'>Водій</td>
						<td width='80px'>Авто</td>
						<td width='20px'>Отримана вага</td>
					</tr>
					%s
				</table>
				<button id='conteinerforbutton' onClick="document.location.href='http://127.0.0.1/cgi-bin/storage.py';"><b>Готово</b></button>
			</div>


		"""

rootRaceResponseString = """
<tr class='string'>
						<td width='400px' height='25px'>%s</td>
						<td width='400px'>%s</td>
						<td width='200px'>%s</td>
					</tr>"""

RaceResponses  = """"""



for response in responses :
    driver = response[0]
    car = response[1]
    mass = response[2]
    RaceResponses+=rootRaceResponseString%("%s %s %s"%(driver.firstName,driver.secondName,driver.surName),car.name,str(mass))

if random.randint(0,1) :
    for i in range(len(db['storages'][ID].carpark)) :
        if db['storages'][ID].carpark[i].status=="В дорозі" and db["storages"][ID].carpark[i] in [response[1] for response in responses] :
            db['storages'][ID].carpark[i].status="Вільний"
            break

	
f = open("response.html","w")
html = page%(blocks.styles,"Звіт відправленого рейсу",blocks.getHeader(db['logined']),raceResponsePage%(location1,location2,location1,location2,RaceResponses),blocks.adminFooter)

f.buffer.write(html.encode('utf8') + b'\n')
f.close()

dictToShelve(db,shlv)
shlv.close()

blocks.startPage()
redirect("http://127.0.0.1/response.html")