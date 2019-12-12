#/usr/bin/env python 
# -*- coding: UTF-8 -*-
import os, sys
import json

# создаём разширеную базу пактов с предлизительно структурой
#pkg_list ={"category": [{name: name_pkg, versions:[list_version]}]}
# и клладём это всё в json
#
#

def create_db():
	pkg_list ={}
	port_dir =["/var/lib/layman/", "/usr/portage"]
	if not os.path.exists('./pkgs.json'):
		print("Create ramdb")
		pkg_name =""
		all_pkgs = []
		with open('./pkgs.json', 'a') as fn:
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

							if not pkg_name[:-1] in  all_pkgs:

								print(str(d.split("/")[-2] +"/" + d.split("/")[-1] +"\n"))
								all_pkgs.append(str(d.split("/")[-2] +"/" + d.split("/")[-1]))

							if d.split("/")[-2] not in pkg_list.keys():
								pkg_list[str(d.split("/")[-2])] = [] 
								pkg_list[d.split("/")[-2]].append(d.split('/')[-1])
								print([d.split("/")[-2]])
							else:
								if d.split('/')[-1] not in pkg_list[d.split('/')[-2]]:
									pkg_list[d.split("/")[-2]].append(d.split('/')[-1])
									print([d.split('/')[-1]])

			fn.write(json.dumps({"all_pkgs": all_pkgs,"Catalog": pkg_list}))
		#print(len(pkg_list))

		print("Found:\t"+ str(len(pkg_list.keys())) +  " category\n" + str(len(all_pkgs)) +"packages\n")

def on_find(p_v):
	if not os.path.exists('./pkgs.json'):
		create_db()
	p = []
	ret_p =""
	ret = {}
	with open('./pkgs.json', 'r') as  fn:
		#data = fn.read()
		pkg_list= fn.read()
		"""
		pkg_list = data.split("\n")
		for i in pkg_list:
		if p_v in i and not i in p:
			print(i)
			p.append(str(i))
			#ret_p = ret_p +"\t" + i
	print("Find in template:\t" + str(len(p)))
	"""
	#ret = {"Name": ret_p.split("\t")}
	#print(ret_p)	
	print(p)
	return pkg_list #json.dumps(ret)

if __name__ == '__main__':
	if not os.path.exists('./pkgs.txt'):
		create_db()
	if len(sys.argv) >=2:
		on_find(sys.argv[1])
	else:
		print("No element to  find")

