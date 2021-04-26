import blocks,shelve

form = """
    <DIV class='regisform' id='registrationContainer1' >
  <h1 style='text-align:center'>Додати потребу</h1>
 <form name="test" method="post" action="addedNeed.py">
  <p><b style='padding-right:75px;'>Назва:</b>
   <input charset="cp1251"  type="text" style="float:right;" name="name" size="40" charset="cp1251" />
  </p>
    <p><b style='padding-right:10px;'>Тип:</b>
   <input charset="cp1251" type="text" style="float:right;" name="kind" size="40">
  </p>
  <p><b style='padding-right:30px;'>Кількість:</b>
   <input charset="cp1251" type="text" style="float:right;" name="quantity" size="40">
  </p>
  <input charset="cp1251" type="submit" style="height:20pt;font:14pt sans-serif; margin: 2pt; margin-right: 0%;text-align:center;margin-top:5px;
                                       background-color:blue;color:white;border-collapse:collapse;" value="Додати">
</form>
</DIV>
"""
db = shelve.open("db")
blocks.startPage()
blocks.enc_print(blocks.page%(blocks.styles,'Додати потребу',blocks.getHeader(db['logined']),form,blocks.adminFooter))
db.close()