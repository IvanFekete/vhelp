import blocks,sys,shelve

content = """
<DIV class='regisform' id='registrationContainerResurses' > 
		<h1 style='text-align:center;padding-top:20px;'>Заявка на ресурси</h1> 
		<form method="post" action="resourcesRequest2.py"> 
			<div style='padding:5px;'> 
				<p>
					<b style='padding-right:75px;'>Адреса пункту потреби :</b> 
					<input charset="cp1251" type="text" style="float:right;" name="location" size="30" charset="cp1251" /> 
				</p> 
				<p>
					<b style='padding-right:30px;'>Кількість найменувань товару :</b> 
					<input charset="cp1251" type="text" style="float:right;margin-top:-20px;" name="n" size="30" charset="cp1251"/> 
				</p> 
			</div> 
			
			<p><input charset="cp1251" type="submit" class="ButtonStoradge" value="Відправити" charset="cp1251" /></p> 
		</form> 
		"""
db = shelve.open("db")

blocks.startPage()
blocks.enc_print(blocks.page%(blocks.styles,"Заявка на ресурси",blocks.getHeader(db['logined']),content,blocks.footer))

db.close()