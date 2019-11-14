# -*- coding: UTF-8 -*- 

from browser import document, html, alert, ajax

def printui():
    alert("print UI")
#class UI():

def clear_el():
    try:
        document["conteiner"].clear('container')
        print("clear_el")
    except KeyError:
        print("KeyError in clear_el")

def Cards(data):
	cd = html.DIV(id=data["Name"], Class=dashboard)
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

def overlays(data):
    # <= html.STRONG( "Доступно:\t" + str(len(overlays["repositories"])) + " Оверлеев")
    widget = html.DIV(Class="table-striped")
    widget_h = html.DIV()
    widget_h_l = html.UL(Class="flex_header")
    widget_h_l <= html.LI("Имя")
    widget_h_l<= html.LI("Описание")
    widget_h_l <= html.LI("Домашняя страничка")
    widget_h <= widget_h_l
    widget <= widget_h
    widget_b = html.DIV()
    for ov in data["repositories"]:

        widget_l = html.UL(Class="flex_tab")
          
        try:
            widget_l <= html.LI(ov['name'])
        except Exception as e:
            print("name: " + str(e))
        try:
            widget_l <= html.LI(ov['description'])
        except Exception as e:
            print("Description: " + str(e))
        try:
            widget_l <= html.LI(html.A(ov['homepage'], href=ov['homepage']))
        except Exception as e:
            print("homepage: " + str(e))
        widget_b <= widget_l
          
        widget <= widget_b
    return widget


def st_portage(port_st):
    clear_el()
    widget = html.DIV(id="container", Class="")
    container = html.DIV(Class="window-content")
    w_H = html.HEADER(Class="toolbar toolbar-header")
    w_H <= html.H1("Настройка PORTAGE", Class="title")
    widget <= w_H
    list_port_items = port_st['portage']

    #tab_items = ["make.conf", "package.use", "package.mask", "package.unmask", "sets"]
    c = html.DIV(id="ps_menu", Class="list-group")
    for i in list_port_items.keys():
      c <= html.DIV(i, Class="list-group-item", id=i )

    edit = html.DIV(id="edit")
    widget <= c
    widget <= container
    #container <=  edit
    return widget

def v_app_settings(d):
    clear_el()
   
    container = html.DIV(id="container")
    lng = ["Русский"]
    lang = html.P("Язык:\t",id="Lang")  
    #for l in lng:
    lang <= html.STRONG(d["Lang"])

    port = html.P("PORT")
    port <= html.INPUT(type="text", id="Sv_port", value=d["PORT"])
    theme = html.P("Темa:\t")
    #thms = ['default', 'light']
    app_st_btm = html.DIV(Class="btm")
    app_st_btm <= html.STRONG(html.SPAN("Сохранить", id='App_save', Class ="btn right"))
    #for t in thms:  
    #  theme <= html.P(t + "\t")
    container <= lang
    container <=theme
    container <= port
    container <= app_st_btm
    return container

def bind_back():
    document["dashbboard"].style.width ='0vw'
    document["list_p"].style.width='100vw'

def dashbord_view(pkg):
    card = html.DIV(id='card', Class = "dashboard")
    document["list_p"].style.width = '0vw'
    document["dashbboard"].style.width = '100vw'
    bk = html.B("<", id="back", Class="back_btn")
    bk.bind('click', bind_back)
    card <= bk
    #alert(pkg['Package_result'])
    i = pkg['Package_result'][0]
    #for n in pkg['Package_result']:
    card <= html.H2(i['Name'])
    vers = html.UL("Доступные версии:\t",  Class="Version")
    cl =""
    inst = ""
    
    for v in i["version"]:
        print("Debug:\t" +"\nV\n" + str(v) + "\t" + "\nI:\n" +str(i))
        vers <= html.LI(v, Class="pkg")
        print(inst)
    card <= vers
      
    use = html.UL("USE: \t", Class="Use")
    for u in i["USE"]:
      use <= html.LI(u)
    card <= use
    card <= html.P("Описание:\t" +  i["Description"])
    card <= html.P("Оверлеи:\t" + i['repo'])
    card <= html.A("Home_page >> ", href=i["Home_page"])

    b_panel = html.DIV(Class=" btm") #toolbar toolbar-footer

    b_panel <= html.STRONG(html.SPAN("-", Class=" btn right", href="#" + i["Name"], id=str(i["Name"])+ "_btn-"))
    #b_panel <= html.STRONG(html.SPAN("+", Class=" btn right", href="#" + i["Name"], id=str(i["Name"])+ "_btn+"))
    card <=  b_panel
    #try:
    #    document['back'].bind('click', bind_back)
    #except KeyError:
    #    print("KeyError Back")
    #return card
    document["dashbboard"] <= card

def v_main(text, widget_tables):
    clear_el()  
    widget = html.DIV(id="container")
    container = html.DIV(Class="window-content")
    #main_page = html.DIV(id="Main_page")
    #widget_menu_page = html.DIV(id="menu_page")
    #widget = html.DIV(Class=" widget")
    w_H = html.HEADER(Class="toolbar toolbar-header")
    w_H <= html.H1("Home Page", Class="title")
    widget <= w_H
    widget_t = html.DIV(Class="list-group")
    for i in widget_tables:
        item = html.DIV(i, Class="list-group-item")
        item <= html.A(id=i)
        widget_t <= item

    widget <= widget_t
    #for i in  self.widget_tables:
    #  document[i].bind('click',  main_bind)

    widget <= html.DIV(text)

    widget <= container

    return widget