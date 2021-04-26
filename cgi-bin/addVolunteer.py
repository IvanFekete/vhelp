import blocks

form = """
    <DIV class='regisform' id='registrationContainer4' > 
  <h1 style='text-align:center'>Додати волонтера</h1>
 <form name="test" method="post" action="addedVolunteer.py">
  <p><b style='padding-right:75px;'>Ім'я:</b>
   <input charset="cp1251" type="text" style="float:right;" name="firstName" size="40">
  </p>
  <p><b style='padding-right:30px;'>По-батькові:</b>
   <input charset="cp1251" type="text" style="float:right;" name="secondName" size="40">
  </p>
  <p><b style='padding-right:10px;'>Прізвище:</b>
   <input charset="cp1251" type="text" style="float:right;" name="surName" size="40">
  </p>
  <p><b style='padding-right:82.5px;'>Вік:</b>
   <input charset="cp1251" type="text" style="float:right;" name="age" size="40">
  </p>
  <p><b style='padding-right:57.5px;'>Логін:</b>
   <input charset="cp1251" type="text" style="float:right;" name="login" size="40">
  </p>
  <p><b style='padding-right:40px;'>Пароль:</b>
   <input charset="cp1251" type="text" style="float:right;" name="password" size="40">
  </p>
  <input charset="cp1251" type="submit" style="height:20pt;font:14pt sans-serif; margin: 2pt; margin-right: 0%;text-align:center;margin-top:5px;
                                       background-color:blue;color:white;border-collapse:collapse;" value="Додати">
</form>
</DIV>
"""

blocks.startPage()
import shelve
db = shelve.open("db")
blocks.enc_print(blocks.page%(blocks.styles,'Додати ресурс',blocks.getHeader(db['logined']),form,blocks.adminFooter))
db.close()
