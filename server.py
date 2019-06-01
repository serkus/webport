from http.server import  HTTPServer
from src.handler import Handler as Handler
import os, sys, json		
#PORT_NUMBER = 8000
from findfsdb import create_db
from utils.utils import load_config
def run():
	create_db()
	config = load_config()
	if len(config) ==0:
		print("конфиг пустой")
	try:
		print(config['PORT'])
	except KeyError:
		print("KeyError")
	server = HTTPServer(('', config['PORT']), Handler)
	print ('Started HTTP Server on port ' , config['PORT'])
	server.serve_forever()

if  __name__ == '__main__':
	run()