#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from http.server import BaseHTTPRequestHandler
import os
from utils.utils import get_list_overlays, load_config, write_config, sort_inatll_pkg
from package import search
from findfsdb import on_find 

#repl = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE repositories SYSTEM "http://www.gentoo.org/dtd/repositories.dtd">'
class Handler(BaseHTTPRequestHandler):
	def __int__(self):
		self.p_list =[]

	def r_403(self):
			self.send_response(403)
			self.end_headers()
			print(self.client_address)

	def do_GET(self):
		self.r_t =""
		if self.client_address[0] == '127.0.0.1' or self.client_address[0].startswith('10.0'):
			self.send_response(200)
			self.end_headers()
			if self.path =="/":

				f = open('./views/index.html', 'tr')
				self.r_t=f.read()
				f.close()
				print(self.client_address)
				#print(self.r_t)
				
			elif self.path == '/main':
				f = open("./README.txt", 'r')
				self.r_t =str(f.read())
				f.close()

			elif self.path == '/ovelays':
				overlays = get_list_overlays()
				#print(ovls)
				if overlays == "":
					overlays ="Error"

				self.r_t=json.dumps({"repositories": overlays})
				
			elif self.path == "/favicon.ico":
				f = open('./favicon.png', 'rb')
				self.r_t = f.read()
				f.close()
					
			elif self.path == '/logo.png':
				pass

			elif self.path.startswith( "/static/"):
				self.r_static()
				self.send_response(200)
				#print(self.r_t)

			elif self.path.startswith("/?st_app="):
				config = load_config()
				param = self.path.replace("/?st_app=", "") 
				list_param = param.split(',')
				print(list_param)
				for i in list_param:
					if i.startswith('port'):
						port = int(i.split('=')[1])	
					elif i.startswith('Lang'):
						Lang = i.split('=')[1]
					
				write_config(port, Lang)
				print(config)
				print(param)

			elif self.path.startswith('/?p='):
				param = self.path.replace('/?p=', '')
				pk_list = []
				search_result = {}
				#if len(param.split('/')) == 2:
				#	param = param.split('/')[1]
				p_list = on_find(param)
				#print(p_list)
				if len(p_list) == 0:
					print("Never Found")
					self.r_t = str(json.dumps({"Package_result": p_list}))
				else:
					for p in p_list:
						#print(p)
						if len(p.split("/")) == 2:
							pk_list.append(search(p.split("/")[1]))
						else:
							pk_list.append(search(p))
						#print(pk)
					search_result = {"Package_result": pk_list}
					self.r_t = str(json.dumps(search_result))

			elif self.path.startswith("/get_seiings_app"):
				self.r_t = str(json.dumps(load_config()))



			elif self.path == '/get_inastal_list':
				self.r_t = str(sort_inatll_pkg())
				
			else:
				self.send_response(404)
				
				self.end_headers()
				print(str(self.client_address[0]) +"\t" + str(404))

	        # Send the html message
			#self.wfile.write(bytes(self.r_t, "utf-8"))
			try:
				return self.wfile.write(self.r_t)
			except TypeError:
				#print("TypeError")
				return self.wfile.write(bytes(self.r_t, 'utf-8'))
		else:
			self.r_403()

	def r_static(self):
		if os.path.exists('./views/' + self.path):
			#self.send_response(200)
			#self.send_header('Content-type','text/css')
			#self.end_headers()
			f = open('./views/' + self.path, 'tr')
			self.r_t=f.read()
			f.close()
		else:
			self.send_response(404)
			self.end_headers()