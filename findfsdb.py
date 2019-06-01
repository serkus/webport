#/usr/bin/env python 
# -*- coding: UTF-8 -*-
import os, sys
import json

pkg_list = []
port_dir =["/var/lib/layman/", "/usr/portage"]

def create_db():
	
	if not os.path.exists('./pkgs.txt'):
		print("Create ramdb")
		pkg_name =""
		fn = open('./pkgs.txt', 'a')
		for p in port_dir:
			for d, dirs, files in os.walk(p):
				for f in files:
					if f.endswith('.ebuild'):
						#print(d +"/" + f)
						pkg_name =""
						try:
							#ver=int(f.replace('.ebuild', '').split('-')[-1][0])
							for pn in f.replace('.ebuild', '').split('-')[:-1]:
								pkg_name = pkg_name + pn + "-"
						except TypeError:
							for pn in f.replace('.ebuild', '').split('-')[:-2]:
								pkg_name = pkg_name + pn + "-"
						except Exception as e:
							print(e)

						if not pkg_name[:-1] in pkg_list:
							print(str(d.split("/")[-2] +"/" + d.split("/")[-1] +"\n"))
							"""
							cat = d.replace(p, "")
							cat_l = cat.split()
							for c_l in cat_l:
								if '-' in c_l:
									c = c_l
									print(c)
									break;
							"""
							pkg_list.append(str(d.split("/")[-2] +"/" + d.split('/')[-1]))
							#with open('./pkgs.txt') as fn:
							fn.writelines(d.split("/")[-2] +"/" + d.split('/')[-1] +"\n")
							print(len(pkg_list))

		fn.close()
		print("Found:\t"+ str(len(pkg_list)) +  " packages\n")

def on_find(p_v):
	if not os.path.exists('./pkgs.txt'):
		create_db()
	p = []
	ret_p =""
	ret = {}
	fn = open('./pkgs.txt', 'r')
	data = fn.read()
	pkg_list = data.split("\n")
	fn.close()
	for i in pkg_list:
		if p_v in i and not i in p:
			print(i)
			p.append(str(i))
			#ret_p = ret_p +"\t" + i
	print("Find in template:\t" + str(len(p)))
	#ret = {"Name": ret_p.split("\t")}
	#print(ret_p)
	print(p)
	return p #json.dumps(ret)

if __name__ == '__main__':
	if not os.path.exists('./pkgs.txt'):
		create_db()
	if len(sys.argv) >=2:
		on_find(sys.argv[1])
	else:
		print("No element to  find")

