import blocks,shelve,sys
from structures import *


content = """
<form action = "doResourcesRequests.py" method = "POST">
    %s

<input charset="cp1251" type="submit" class="ButtonStoradge1" value="Відправити" />
</form>
"""

rootResourcesRequestString = """
<div style='width: 544px;
			padding: 10px;
			border-radius: 2px;
			background-color: #FC0;'>

		<p>
			<b style="padding-right:75px;font-size:22px;text-align:center;">Адреса пункту потреби : %s</b>
		</p>
		<p>
			<b style="padding-right:75px;font-size:22px;text-align:center;">Кількість найменувань товару : %s</b>
		</p>
        %s
		<br/>
		<input charset="cp1251" type="checkbox"  size='7' name="%s" ><b>Прийняти</b>
</div>
"""

resourcesTable = """
    <table border="2" style="border-collapse:collapse;margin-top:20px;border-color:black;">
		<tbody>
				<tr style="font-size:18px;text-align:center;">
					<td width="80px" height="20px">Код</td>
					<td width="200px">Назва</td>
					<td width="150px">Тип</td>
					<td width="100px">Кількість</td>
				</tr>

				%s

		</tbody>
</table>
"""

rootResourceString = """
<tr style="font-size:18px;text-align:center;">
					<td width="80px">%s</td>
					<td width="200px">%s</td>
					<td width="150px">%s</td>
					<td width="100px">%s</td>
				</tr>

"""

requests = """"""

db = shelve.open("db")
i = 0
for request in db['resourcesRequests'] :
    requests+="<br />"
    strings=""""""
    for resource in request.resources :
        strings+=rootResourceString%(resource.code,resource.name,resource.kind,resource.quantity)
    requests+=rootResourcesRequestString%(request.location,str(len(request.resources)),resourcesTable%strings,str(i))
    i+=1


blocks.startPage()
blocks.enc_print(blocks.page%(blocks.styles,"Заявки на ресурси",blocks.getHeader(db['logined']),content%requests,blocks.adminFooter))

db.close()