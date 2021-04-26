import blocks,sys,shelve,cgi,json,random
from structures import *
from urllib.request import urlopen

k = 1000000#coef

form = cgi.FieldStorage()
d = shelve.open("db")
db = shelveToDict(d)

page = """
<html>
    <head>
		%s
        <title>%s</title>
        
        
	<meta charset=utf-8 />	
        <script src="https://maps.google.com/maps/api/js?v=3.exp&sensor=false"></script>
        <script>
            var zm;
            var map, directionsService;
            var color=['#000000','#000099','#003300','#006600','#00FF00','#330000','#330066','#333300','#336600','#663300','#66FFCC','#990000','#9933CC','#CC0066','#CC9900','#CCCC00','#FF0000','#FFCC00'];
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
            
            function Roadmap(sz) {
             
                var f,s;
              for(var i=0;i<=sz;i++){
                    f = document.getElementsByName("f")[i].value;
                    s = document.getElementsByName("s")[i].value;
                    requestDirections(f, s, {strokeColor:color[1],
                                             strokeWeight: 3}
                                     );
                }
            }

            google.maps.event.addDomListener(window, 'load', initialize);

        </script>
    </head>
    <body bgcolor="darkblue" onload="Roadmap(%s);">
	
    %s
        %s
		
            %s
    </body>
</html>





"""


raceResponsePage = """
<div id="map-canvas"></div>
		<div class='not2'>
			
				%s
				<button id='conteinerforbutton' onClick="document.location.href='http://127.0.0.1/cgi-bin/storage.py';"><b>Готово</b></button>
			</div>
		"""

rootRaceString = """
			<input charset="cp1251" type="text" name="f" id="start" value="%s"/>
			<input charset="cp1251" type="text" name="s" id="end" value="%s"/>
			
			<br />
			<a href="https://www.google.com.ua/maps/dir/%s/%s" target="blank">Переглянути маршрути у повному розмірі</a>
			<br />
			<table  border='2px' width='80px' class='tableadmin'>
					<tr class='string'>
						<td width='80px' height='25px'>Водій</td>
						<td width='80px'>Авто</td>
						<td width='20px'>Отримана вага</td>
					</tr>
					%s
				</table>

				<br />
				<br />
"""

rootRaceResponseString = """
    <tr class='string'>
						<td width='80px' height='25px'>%s</td>
						<td width='80px'>%s</td>
						<td width='20px'>%s</td>
					</tr>"""
races = """"""

storages = []
xx,yy = 1, 1
for key in db['storages'] :
    #request = json.loads(urlopen("http://maps.google.com/maps/api/geocode/json?address=%s"%(db['storages'][key].address)).read().decode("cp1251"))
    x = xx#request["results"][0]["geometry"]["location"]["lat"]*k
    y = yy#request["results"][0]["geometry"]["location"]["lng"]*k
    xx += 1
    yy += 1
    point = Point(x,y,db['storages'][key].address,str(db['storages'][key].ID))
    storages.append(point)
	
need_points = []
for key in form.keys() :
    i = int(key)
    if i >= len(db['resourcesRequests']) : continue
    #request = json.loads(urlopen("http://maps.google.com/maps/api/geocode/json?address=%s"%(db['resourcesRequests'][i].location)).read().decode("cp1251"))
    x = xx#request["results"][0]["geometry"]["location"]["lat"]*k
    y = yy#request["results"][0]["geometry"]["location"]["lng"]*k
    xx += 1
    yy += 1
    point = Point(x,y,db['resourcesRequests'][i].location,str(i))
    need_points.append(point)

result = hungrian_algo(db,storages,need_points)
for (storage,need_point) in result :
    responses = db['storages'][int(storage.ID)].giveRace(db,db["resourcesRequests"][int(need_point.ID)].resources)
    for pair in responses :
        for resource1 in pair[3] :
            for i in range(len(db['resourcesRequests'][int(need_point.ID)].resources)) :
                if resource1.name==db['resourcesRequests'][int(need_point.ID)].resources[i].name :
                    db['resourcesRequests'][int(need_point.ID)].resources[i].get()

    raceResponses = """"""
    for response in responses :
        driver = response[0]
        car = response[1]
        mass = response[2]
        raceResponses+=rootRaceResponseString%("%s %s %s"%(driver.firstName,driver.secondName,driver.surName),car.name,str(mass))

    races+=rootRaceString%(storage.location,need_point.location,storage.location,need_point.location,raceResponses)

for ID in range(1,db['maxStorageID']+1) :
	if random.randint(0,1) :
		for i in range(len(db['storages'][ID].carpark)) :
			if db['storages'][ID].carpark[i].status=="В дорозі" and db["storages"][ID].carpark[i] in [response[1] for response in responses] :
				db['storages'][ID].carpark[i].status="Вільний"
				break
	
f = open("response1.html","w")
html=page%(blocks.styles,"Звіт відправки рейсів",str(len(result)-1),blocks.getHeader(db['logined']),raceResponsePage%races,blocks.adminFooter)
f.buffer.write(html.encode('utf8') + b'\n')
f.close()

dictToShelve(db,d)
d.close()


blocks.startPage()
redirect("http://127.0.0.1/response1.html")
