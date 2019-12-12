#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from http.server import BaseHTTPRequestHandler
import os
from utils.utils import get_list_overlays, load_config, write_config, sort_inatll_pkg, scan_config_portage
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
	
	def r_404(self):
		self.send_response(404)
		self.end_headers()
		print(self.client_address)
	def route(self):
		if self.path in route:
			return true
		else:
			return false

	def parse_url(self):
		pass

	def do_GET(self):
		self.r_t =""
		if self.client_address[0] == '127.0.0.1' or self.client_address[0].startswith('10.0'):
			self.send_response(200)
			self.end_headers()
			if self.path =="/":

				with open('./views/index.html', 'tr') as f:
					self.r_t=f.read()
				print(self.client_address)
				
			elif self.path == '/main':
				f = open("./README.txt", 'r')
				self.r_t = str(f.read())
				f.close()

			elif self.path == '/ovelays':
				overlays = get_list_overlays()
				#print(ovls)
				if overlays == "":
					overlays ="Error"

				self.r_t=json.dumps({"repositories": overlays})
				
			elif self.path == "/favicon.ico":
				with open('./favicon.png', 'rb') as f:
					self.r_t = f.read()
					
			elif self.path == '/logo.png':
				pass

			elif self.path.startswith( "/static/"):
				self.r_static()
				self.send_response(200)
				#print(self.r_t)

			elif self.path == '/get_dump_list':
				with open('./pkgs.json', 'r') as fn:
					data = fn.read()
					pkg_list = json.loads(data)
					print(pkg_list)
				self.r_t =json.dumps({"dump_portage": pkg_list})
			
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
				#p_list = on_find(param)
				#print(p_list)
				#if len(p_list) == 0:
				#	print("Never Found")
				#	self.r_t = str(json.dumps({"Package_result": p_list}))
				#else:
					#for p in p_list:
						#print(p)
				if len(param.split("/")) == 2:
					pk_list.append(search(param.split("/")[1]))
				else:
					pk_list.append(search(param))
					#print(pk)
				search_result = {"Package_result": pk_list}
				self.r_t = str(json.dumps(search_result))

			elif self.path.startswith("/get_settings_app"):

				self.r_t = str(json.dumps(load_config()))

			elif self.path == '/get_portage':

				#self.r_t = str(sort_inatll_pkg())
				self.r_t = str(json.dumps(scan_config_portage()))

			elif '.py?' in self.path:
				print("loading")
				self.path = "/static/app" + str(self.path.split('?')[0])
				print(self.path)
				self.r_static()

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
			with open('./views/' + self.path, 'tr') as f:
				self.r_t=f.read()
			
		else:
			self.send_response(404)
			self.end_headers()
