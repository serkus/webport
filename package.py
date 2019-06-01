# -*- coding: UTF-8 -*-
#!/usr/bin/python 
import json
import portage
portage.root
portge = portage.db[portage.root]["porttree"].dbapi
from utils.utils import sort_inatll_pkg
#ПЛАН:
#    
# API PORTAGE IN SEARCH

def search(r_p):
    Cat =[]
    pkg = {}
    Category =""
    Name = ""
    version =""
    USE =""
    Description = ""
    Home_page =""
    repository = ""
    try:
        pametrs = ["HOMEPAGE", "IUSE","DESCRIPTION", "repository", "LICENSE"]
        #print(r_p)
        p_list = portge.xmatch('match-all', r_p)
        m_list = portge.xmatch('match-visible', r_p)
        #print(m_list)
        
        #print(len(p_list))
        if len(p_list) != 0:
            for l in p_list:
                params = portge.aux_get(l, pametrs)               
                if str(Cat) in Category and str(l).split('/')[1].split('-')[0] in Name:
                    version = version + "    " + str(l.replace(l.split("/")[0] + "/"+ r_p, ""))
                    if not l in m_list:
                        version = str(version) +"[M]"
                    else:
                        version = str(version) +"[U]"
                    #version + "    " + str(l).split('/')[1].split('-')[:-1]
                else:
                    Category= str(Cat)
                    #Name =str(l).split('/')[1].split('-')[0]
                    

                    Name = l.split("/")[0] +"/" + r_p
                    version = str(l.replace(l.split("/")[0] + "/"+r_p, ""))
                    if not l in m_list:
                        version = str(version) + "[M]"
                    else:
                        version = str(version) +"[U]"

                    USE = params[1]
                    Description = params[2]
                    Home_page = params[0]
                    repository = params[3]
        else:
            Name = "Package is not Found" 

        #print(Category + "\n" + Name + "\n" + version +"\n" + USE + "\n" + Description + "\n" + Home_page  +"\n") 
        #p_list = str(Category + "\n" + Name + "\n" + version +"\n" + USE + "\n" + Description + "\n" + Home_page  +"\n")
    except Exception as e:
        print(str(e))
        p_list = " ERROR IN Package "
        
    pkg = {"Category": Category, "Name": Name,"version": version.split("    "), "USE":USE.split(" "), "Description": Description, "Home_page":Home_page, 'repo': str(repository) }
    print(pkg)
    return pkg
