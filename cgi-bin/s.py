import cgi,shelve

form = cgi.FieldStorage()

s = form['abc'].value

print('Content-type: text/html\n')
print("<h1>%s</h1>"%s)