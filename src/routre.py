# -*- codding: utf-8 -*-
#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
import json
class Router(BaseHTTPRequestHandler):
    def __int__(self):
		self.p_list =[]
        self.r_t  = ""
	
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
		print(self)
        return json.loads(self.rfile)

	def do_GET(self):
        pass
    
    def do_POST(self):
        pass