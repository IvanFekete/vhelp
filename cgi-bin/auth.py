import cgi
import blocks,shelve
from structures import dictToShelve,shelveToDict,redirect

form = cgi.FieldStorage()
login = form['login'].value
password=form['password'].value

shlv = shelve.open("db")
db=shelveToDict(shlv)

blocks.startPage()

for volunteer in db['volunteers'].values() :
    if volunteer.login==login and volunteer.password==password :
        db['logined'] = volunteer
        if type(volunteer).__name__ in ['Volunteer','Driver','StorageCoordinator'] :
            redirect('http://127.0.0.1/cgi-bin/storage.py')
        elif type(volunteer).__name__=='HumanResourcesCoordinator' :
            redirect('http://127.0.0.1/cgi-bin/requests.py')
        else :
            redirect('http://127.0.0.1/cgi-bin/allResourcesRequests.py')
        break
else :
    content = """
    <h2 align="center" style='color:white'>Неправильний логін або пароль.Спробуйте ще раз</h2>
	<div style='height:20%;width:60%;margin-left:15%;margin-top:20px;'>
	<div style='width:380px;height:120px;margin-left:30%;margin-top:80px;background-color:#FC0;text-align:center;padding:20px;'>
	                           <h2 style='margin-top:-10px;'>Авторизація</h2>
						<form action="auth.py" method="post">
									<p><b style='padding-right:57.5px;float:left;font-size:20px;margin-left:0px;'>Логін:</b>
                                      <input charset="cp1251" type="text" style="float:right;" name="login" size="30">
                                   </p>
                                   <br/>
                                   <p><b style='padding-right:57.5px;float:left;font-size:20px;'>Пароль:</b>
                                      <input charset="cp1251" type="password" style="float:right;" name="password" size="30">
                                   </p>
                                   <br/>
                                   <p style='margin-top:15px;margin-left:306px;'><input charset="cp1251" type="submit"
                                       style='height:20pt;font:14pt sans-serif; margin: 2pt; margin-right: 25%;text-align:center;
                                       background-color:blue;color:white;border-collapse:collapse;' value="Увійти"></p>
						</form>
				</div>
	</div>
"""
    blocks.enc_print(blocks.page%(blocks.styles,'Авторизація',blocks.header,content,blocks.footer))


dictToShelve(db,shlv)
shlv.close()
