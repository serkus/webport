# -*- codding: utf-8 -*-
#!/usr/bin/env python3
from io import StringIO ## for Python 3
from http.server import BaseHTTPRequestHandler
import json
class Router(BaseHTTPRequestHandler):
	def __int__(self):
		self.p_list = []
		self.r_t  = ""
		pass
	def route(self):
		if self.path in route:
			return true
		else:
			return false
        
	def parse_url(request):
		
		print("request.rfile:\t"  + str(request.rfile.read()))
		#return json.loads(str(request.rfile.read()))

	
"""
	def do_GET(self):
        pass
    
    def do_POST(self):
        pass
"""