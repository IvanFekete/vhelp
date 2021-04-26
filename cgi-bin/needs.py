import shelve,blocks,sys
from structures import *

table = """
<div id="containerwindows" style="color:white;">
<h1>Тут виставлений список тих ресурсів,які потрібні нашій організації.Якщо ви можете чимось допомогти,звяжіться з нашою адміністрацією.</h1>
<table border='2px'  align='center' style='margin-top:-70px;margin-bottom:80px;border-collapse:collapse;border: 2px solid white;padding-bottom:100px;font-size:22px;color:white;' width='700px'>
				<tr height='50px';align='center'>
					<th width='250px'>Продукт</th>
					<th width='250px'>Тип</th>
					<th>Кількість</th>
				</tr>
				$Strings$
</div>					
"""

rootString = """
<tr height='30px;'>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>
"""

adminPage = """
<div id="containerwindows" style="color:white;">
<form action="saveNeeds.py" method="post">
<h1>Тут виставлений список тих ресурсів,які потрібні нашій організації.Якщо ви можете чимось допомогти,звяжіться з нашою адміністрацією.</h1>
<br><br><br><br><table border="2px" align="center" style="margin-top:-70px;margin-bottom:80px;border-collapse:collapse;border: 2px solid white;padding-bottom:100px;font-size:22px;
	color:white;text-align:center;" width="800px">
				<tr height="50px" ;align="center" >
					<td width="350px">Продукт</td>
					<td width="300px">Тип</td>
					<td>Кількість</td>
				</tr>
				$Strings$

</table>
<div style='float:left;margin-left:5%;'>
<div style='margin-top:-70px;margin-left:220px;'><input charset="cp1251" type="button"
                                        onClick="document.location.href='http://127.0.0.1/cgi-bin/addNeed.py'"
                                       style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:px;
                                       background-color:gold;;color:Black;border-collapse:collapse;margin-left:0px;' value="Додати" /></div>
<input charset="cp1251" type="submit"
                                       style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:10px;
                                       background-color:gold;;color:Black;border-collapse:collapse;margin-left:220px;' value="Зберегти" />
</form>
</div>
</div>
"""

rootAdminString = """
    <tr height="30px;">
    <td>%s</td>
    <td>%s</td>
    <td><input charset="cp1251" style='text-align:center;' type="text" size="16" value="%s" name="%s"></td>
    <td>
        <form action="delNeed.py" method="post">
            <input charset="cp1251" type="submit" style='height:20pt;font:14pt sans-serif;text-align:center;margin-top:0px;background-color:gold;;color:Black;border-collapse:collapse;float:right;' name="%s" value="Видалити" />
        </form>
    </td>
    </tr>
"""

strings = """<form action="delNeed.py" method="post"></form>"""


blocks.startPage()

shlv = shelve.open("db")
db = shelveToDict(shlv)
if type(db['logined']).__name__=='MainCoordinator' :
    i = 0
    for need in db['needs'] :
        strings+=rootAdminString%(need.name,need.kind,need.quantity,str(i),str(i))
        i+=1
    adminPage = adminPage.replace('$Strings$',strings)
    blocks.enc_print(blocks.page%(blocks.styles,'Потреби волонтерської організації',blocks.getHeader(db['logined']),adminPage,blocks.adminFooter))
else :
    for need in db['needs'] :
        strings+=rootString%(need.name,need.kind,str(need.quantity));footer = blocks.footer if db['logined'] is None else blocks.adminFooter

    blocks.enc_print(blocks.page%(blocks.styles,'Потреби волонтерської організації',blocks.getHeader(db['logined']),table.replace('$Strings$',strings),footer))

dictToShelve(db,shlv)
shlv.close()

