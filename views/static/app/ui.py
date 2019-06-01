# -*- coding: UTF-8 -*- 

from browser import document, html

def Cards(data):
	cd = html.DIV(id=data["Name"], Class="card")
        #pl["Name"].split(',')
        """
        if len(pl["Name"])>1:
          for i in pl["Name"]:
            cd <= html.P(html.B(i, id=i))
            print(i)
            cd <=  html.HR()
        else:
          """
        cd <= html.P(html.B(data["Name"]))
        cd <=  html.HR()
        
        vers = html.UL("Доступные версии:")
        for v in data["version"]:
          vers <= html.LI(v)
        cd <= vers
        
        use = html.UL("USE", Class="Use")
        for u in data["USE"]:
          use <= html.LI(u)
        cd <= use
        
        cd <= html.P("Описание:\t" +  data["Description"])
        cd <= html.A("Home_page >> ", href=data["Home_page"])
        b_panel = html.DIV(Class="btm")
        b_panel <= html.STRONG(html.SPAN("Установить", Class="btn right", href="#", id=data["Name"] + "_btn"))
        cd <=  b_panel

def Repositories():
	pass

def Menu():
	pass
