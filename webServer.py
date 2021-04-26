import os,sys,shelve
from http.server import HTTPServer,CGIHTTPRequestHandler


webDir = '.'
port = 80
os.chdir(webDir)
serverAddR = ("",port)
serverObject = HTTPServer(serverAddR,CGIHTTPRequestHandler)
serverObject.serve_forever()
