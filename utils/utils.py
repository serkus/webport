# -*-  coding: UTF-8 -*-
#!/usr/bin/env python3
'__autor__'== 'serkus'
import os, sys, json
from urllib import request
#import xml
import xml.etree.ElementTree as ET
#Проверяем пользователь ROOT или нет
def is_root():
	return os.geteuid() == 0
	
#Читаем Файл посторочно
def read_configs(filename):
	param = {}
	if os.path.exists(filename):
		with open(filename) as f:
			for line in f: 
				print(line)
	else:
		print("Path is not Found")

#получаем список оверлеев

def get_list_overlays():
	overlays =""
	url = "https://api.gentoo.org/overlays/repositories.xml"
	response = request.urlopen(url)
	overlays = []
	overlay = {}
	root = ET.fromstring(response.read())
	#print(root.tag)
	#print(root.attrib)
	name = ""
	description = ""
	homepage = ""
	for child in root.findall('repo'):
		name = child.find('name').text
		#try:
		description = child.find('description').text
		#except AttributeError: 
		#	description = "У overlay нет описания"
		try:
			homepage = child.find('homepage').text
		except AttributeError:
			homepage = "У overlay нет домашней странички"
		overlay = dict(name=name, description=description, homepage=homepage)

		overlays.append(overlay)
	#print(str(overlays))
	print(len(overlays))
	#f=open('./overlays.json', 'a')
	#f.write(json.dumps({"repositories": overlays}))
	#f.close()

	return overlays


def xml_element_to_dict(elem):
	"Convert XML Element to a simple dict"
	inner = dict(elem.attrib)
	children = list(map(xml_element_to_dict, list(elem)))
	text = elem.text and elem.text.strip()
	if text:
		inner['@text'] = text
	if children:
		inner['@children'] = children
	return {elem.tag: inner}

def xml2json(xmldata):
	pass
	#doc = ET.parse(xmldata)
	#root = root = ET.fromstring(xmldata)

def write_config(port=8000, Lang='ru', theme="default"):
	
	conf = dict(PORT=port, Lang=Lang, THEME=theme)
	with open('./config.json', 'w') as f:
	    json.dump(conf, f)
	return conf

def read_config():
	with open('./config.json', 'r') as f:
	    conf = json.load(f)
	return conf

def load_config():
	conf = {}
	if not os.path.exists("./config.json"):
		write_config()
	else:
		conf = read_config()
	return conf

#SORT IN  INTALL PAKAGES
#'/var/db/pkg/'
def sort_inatll_pkg():
	INSTALL = []
	path = '/var/db/pkg'
	for d, dirs, files in os.walk(path):
		for f in files:
			if f.endswith('.ebuild'):
				INSTALL.append(f.replace('.ebuild', ""))
	#print(str(len(INSTALL)))
	return json.dumps({'install_pkgs':INSTALL})

def scan_config_portage():
	dir_root ="/etc/portage"
	config = {}
	i = 0
	dr = {}
	data = {}
	pf={}
	for d, dirs, files in os.walk(dir_root):

		print(str(d))
		i=i+1
		for fl in files:
			
			with open(d + "/" +fl) as f:
				pf[str(d.split('/')[-1]) +  "/"+ fl]= f.read().split('\n')
				str(d.split('/')[-1])
	print(dr)
	config = {'portage': pf}
	print("config:\t" + str(config))
	return config