import sys,shelve,blocks

rootStorageView ="""
	  <br />
    <div  id='driversContainer'>
		<DIV><img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAb1BMVEX///8zMzMuLi4lJSVWVlbz8/NcXFwfHx/c3Nzh4eEoKCjk5OQrKysdHR0iIiKnp6ednZ0YGBj
					   Y2NhZWVlMTExTU1MODg4/Pz86Ojp7e3tubm5nZ2eYmJjp6emqqqpiYmLLy8tHR0fQ0NC8vLyEhITbMelRAAAEZ0lEQVR4nO2di3aiMBRFIaARjDxUbNVabKf//41Tqp3GZ0lykxDn7A9gZa/rIeZJ
					   FAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwH/NaP8+n/puhEX+tIzzImnffTfEEllas7hD1GnmuzE2KBMRfyOS0ndzyJmOeSzDxw8Wx4qL+BTBK9+NIiRb8PgSvniYNJbivIDHMorHS
					   OMuLa76dRTpznfzzCmPXcR1WB16GbPxtQSevlSDTmOZX0/gSRrzcMs4XdxO4EkaF4H2jfcTKBNmGrP2twTK8Da4NPZJoExoaZw2KgU8lrEJKI1loVbAYxmLUMqYjWcafh2zMPpG1QSelDGANOokUG
					   bwaZQH8pplHPTw/3wgr1nG4Q7/y5lpAQ+I2TDLqP8KvWSQL1XzBMoML400CZQZWBrLmrKAB8SABhyUCZQZTBpvTaWZM4zJuF1KnUAZ7n8yjqoPvIXvvtFWAmW8ptFeAmX8pXFqNYEyPPXSN772nko
					   zh9Wvzv12SlNp5vDW8Ut1F7tIoIxgE5eCWeHuF/oNW7kMY+u6gh1i405w3m89ghq+d2a4zr0Y5h/ODBuNFLJzNB7RuhIcqTcufh6f86zxlJErw0S5aWx88ZSxehUTGMIQhjCEIQxhCEMYwvAHjeEh
					   jWExdyNYaswC0xjGTibAJ1orhUSGMR9bn4+qtLY7kRnGorC7xT/T3S1DZtjtuLG4jlElupOIhIYxS2yVMTNYp6A07NYxrJSx4gazwLSGMbNw4EY7gVYMLaRRP4GWDInTOL1z7MWXYXfghmwho1oZr
					   8PYMIzZiqaMk6sHz4Zg2B1/I/iLU5HsV2PN5BydpYELhHEas4ZqmSlPTqFa3CnMXqqVw7V6XVitX0aSBDpAO42VwaZ7t4hcp4zZ0s9Crx7FUjmNRv9CPaD6T3XibLsTHTxVSCNNH+ia/n3jZBleAQ
					   /wZa8ylrOwEijDekzGTXqe3R0qxW99Y2V5y699xOxeGieGB8+GAW9ultF0ID8Ubg3/TabShsbVybgQhhH9uRxwPEYCZc7SGM4woj/ygGMX1DCiP8XyuDd8yh6vgAdE8rWkmsWP9Io5hYmuihs/G37
					   dkK8/S1j7boVV6nn08cgljOPPvzcUU88Dhm0ine3WIfEU+W6BdWAYPjAMHxiGDwzDB4bhA8PwgWH4wFCR851POhBPq5AasmZEAcmOt3/QGqZ3Fif7k8JQCRgqAUMYwlALGCoBQxjCUAsYKgFDGMJQ
					   CxgqAUMYwlALGCoBQxjCUAsYKgFDGMJQCxgqAUMYwlALGCoBQxjCUAvSk11sQWJIe5wu2hI+TmxJDNeU55LfohfCrYBEnw4vCY+W5y/RnvCUbEJzVeOc8PaDeh5FW7LfRE71LR+6ry2JZUT4hTFG9
					   imfEdUdHYx9/ar2NDcO5ILuqu35E0kVRbE/PG+6rE0fyJJ6Tfn5vl27Mr0sh+X19ucOl/nLm9HTnjYV9ZX3WdUYNel5+7L/etBfI417L1F5JDgAAAAASUVORK5CYII='
					   height='150' width='160'></DIV>
		<DIV class='driversGroup'>
			<p style='font-size:33px;color:#000080'>Склад № %s</p>
			<p style='font-size:18px;'>Адреса:</p><p style='font-size:18px;'> %s</p>
			<form action="genStorage.py" method="post">
				<a href="#"><input charset="cp1251" class='ButtonStoradge' name="%s" type="submit" value="Показати більше" /></a>
			</form>
		</div>	
	  </div>
"""

db=shelve.open("db")

storageList = """"""
for storage in db['storages'].values() :
    storageList+=rootStorageView%(storage.ID,storage.address,storage.ID)

if type(db['logined']).__name__=='MainCoordinator' : storageList+='<a href="addStorage.py" style="color:#FF0000">Додати склад</a>'

blocks.startPage()
blocks.enc_print(blocks.page%(blocks.styles,'Список складів',blocks.getHeader(db['logined']),storageList,blocks.adminFooter))

db.close()
