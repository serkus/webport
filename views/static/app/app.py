#-*- coding: UTF-8 -*- 
from browser import window, timer, document, ajax, alert, html
import json
from browser.template import Template  
import browser
from io import StringIO
parser = window.DOMParser.new()
menu_port = {'home': "Главная",'overlays':"Оверлеи", 'doc': 'Документации', 'portage_settngs':"Настройка portage",'app_st':"Настройка",'status':"Процесс"}
catalog = ["Аудио и Видео", "Графика", "Интернет", "Игры", "Программирование", "Система" ]
overlay_cell = ["Имя", "Описание","Домашняя страничка", "Email", "Исходники"]

version = "web_port-00.0.024"
#document['v'].bind('click', view_row)
# Temlate Menu
Template(document["link_panel"]).render(menu_port=menu_port)
#Template(document["nav_memu"]).render(catalog=catalog)
# location

#document['btnSclose'].bind('click', view_search)

def view_catalog():
  pass

class App(object):
  """docstring for App"""
  def __init__(self):
    self.data =""
    self.widget_tables = ["Новости", "Рекомендации", "Документация"]
    self.istall_apps = []
    self.req_istall_pkg()
    self.Main_page = ""
    self.m_req()

    #super(App, self).__init__()
  def get_main_text(self, req):
    self.Main_page = str(req.responseText)

  def p_install_list(self, req):
    if req.status == 200:
      plist = json.loads(req.responseText)['install_pkgs']
      self.install_apps = plist
      #alert(self.install_apps)
    elif req.status == 404:
      alert('Путь  не  найден')
    elif req.status == 403:
      alert("Доступ  запрещён")
      
    return plist


  def req_istall_pkg(self):
    req = ajax.ajax()
    req.open('GET', '/get_inastal_list', True)
    req.bind('complete', self.p_install_list)
    req.send()

  def clear_el(self):
    try:
      document["conteiner"].clear('container')
      print("clear_el")
    except KeyError:
      print("KeyError in clear_el")

  def loading(self):
    if document['splash'].style.display == "none":
      #document['splash'].style.opacity ="0.15"
      document['splash'].style.display = "block"
    else:
      #document['splash'].style.opacity ="1"
      document['splash'].style.display = 'none'



  def add_evenet(self, element):
    pass
  
  def main_bind(self, ev):
    alert(ev.currentTarget.id)


  def main(self):
    self.clear_el()
    
    widget = html.DIV(id="container")
    container = html.DIV(Class="window-content")
  #main_page = html.DIV(id="Main_page")
  #widget_menu_page = html.DIV(id="menu_page")
  #widget = html.DIV(Class=" widget")
    w_H = html.HEADER(Class="toolbar toolbar-header")
    w_H <= html.H1("Home Page", Class="title")
    widget <= w_H
    widget_t = html.DIV(Class="list-group")
    for i in self.widget_tables:
      item = html.DIV(i, Class="list-group-item")
      item <= html.A(id=i)
      widget_t <= item

    widget <= widget_t
    #for i in  self.widget_tables:
    #  document[i].bind('click',  main_bind)
    if len(self.Main_page) == 0:
      alert("А ничего  и нет")
    else:
      widget <= html.DIV(self.Main_page)

    widget <= container

    document["conteiner"] <= widget


  def m_req(self):
    req = ajax.ajax()
    req.open('GET', "/main", True)
    req.bind('complete', self.get_main_text)
    req.send()

  def show_result(self, req):
    if req.status == 200:
      alert("Конфигурация прянята и вступит в силу после после перезагрузки сервера")
    elif req.status == 403:
      alert("Доступ запрещен")

  def app_save(self,  event):
    port = document['Sv_port'].value
    req = ajax.ajax()
    req.open("GET", "?st_app=" +'port='+str(port) + ",Lang=" + "ru", True)
    req.bind('complete', self.show_result)
    req.send()

  def app_settings(self, req):
    #location ="/app_st"
    self.clear_el()
    d = json.loads(req.responseText)
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
    document["conteiner"] <= container
    document['App_save'].bind('click', self.app_save)

  def get_sett(self):
    req = ajax.ajax()
    req.open("GET", "/get_seiings_app", True)
    req.bind('complete', self.app_settings)
    req.send()

  def view_pkg(self, pkgname):
    dashbboard = html.DIV(id='card', Class="card")
    i = 0
    for n in self.data['Package_result']:
      if n['Name'] == pkgname:
        i = n 

    dashbboard <= html.H2(i["Name"])
    vers = html.UL("Доступные версии:\t",  Class="Version")
    cl =""
    inst = ""

    for v in i["version"]:
      if v.endswith('[M]'):
        v = str(v.replace('[M]', ""))
        inst = i['Name'] + v
        if inst in self.install_apps:
          v = v + "[I]"
        vers <= html.LI(v, Class="mask")
      else:
        v = v.replace('[U]', "")
        inst = i['Name'] + v
        if inst in self.install_apps:
          v = v + "[I]"

        vers <= html.LI(v, Class="pkg")
      print(inst)
    dashbboard <= vers
      
    use = html.UL("USE: \t", Class="Use")
    for u in i["USE"]:
      use <= html.LI(u)
    dashbboard <= use
      
    dashbboard <= html.P("Описание:\t" +  i["Description"])
    dashbboard <= html.P("Оверлеи:\t" + i['repo'])
    dashbboard <= html.A("Home_page >> ", href=i["Home_page"])
    
    b_panel = html.DIV(Class=" btm") #toolbar toolbar-footer

    b_panel <= html.STRONG(html.SPAN("Установить", Class=" btn right", href="#" + i["Name"], id=str(i["Name"])+ "_btn"))
    dashbboard <=  b_panel

    document['dashbboard'] <= dashbboard
    document[str(i["Name"]) + "_btn"].bind('click', self.install_config)

  def info_pkg(self, ev):
    #try:
    #  alert("click on %s" %ev.currentTarget.id)
    #except Exception as e:
    #  alert(str(e))
    pkg = str(ev.currentTarget.id)
    document['dashbboard'].clear('card')
    self.view_pkg(pkg)

  def find_bind(self, req):  
    if req.status == 200 or req.status == 0:
      #alert(req.responseText)
      pl = json.loads(req.responseText)
      self.data = pl
      widget= html.DIV(id="container", Class="")
      w_H = html.HEADER(Class="toolbar toolbar-header")
      w_H <= html.H1("Поиск", Class="title")
      widget <= w_H
      container = html.DIV(Class="window-content")
      widget <= container

      pkg_list = []
      if pl["Package_result"] == 0:
        pass
      else:
        c = html.UL(id="list_p", Class="list-group")
        c <= html.STRONG("Найдено совпадений:\t" + str(len(pl["Package_result"])))
        c <= html.HR()
        container <= c
        dashbboard = html.DIV(id ="dashbboard", Class="window-content dashbboard")
        container <= dashbboard
        card =  html.DIV(id="card", Class="card")
        dashbboard <= card 
        n = 0
        for i in pl["Package_result"]: 
          n = n +1
          item = html.LI( id=i["Name"], Class="list-group-item")
          item <= html.A(i["Name"])    
          c <= item

      document["conteiner"] <= widget
      for i in pl['Package_result']: 
        try:
          document[i["Name"]].bind("click", self.info_pkg)

        except KeyError:
          print("KeyError в доб.поиск")

      #self.view_pkg(pl['Package_result'][0])
    self.loading()
            
  def find_pkg(self, req):
    
    req = ajax.ajax()
    if document["inS"].value !='':
      self.loading()
      pm = document["inS"].value
      req.open('GET', '/?p=' + pm,True)
      location ='/?p=' + pm
      req.bind('complete', self.find_bind)
      req.send()
      
    else:
        alert("Name package is Null")
    self.clear_el()

  def view_st_portage(self):
    self.clear_el()
    widget = html.DIV(id="container", Class="")
    container = html.DIV(Class="window-content")
    w_H = html.HEADER(Class="toolbar toolbar-header")
    w_H <= html.H1("Настройка PORTAGE", Class="title")
    widget <= w_H
    tab_items = ["make.conf", "package.use", "package.mask", "package.unmask", "sets"]
    c = html.DIV(id="ps_menu", Class="list-group")
    for i in  tab_items:
      c <= html.DIV(i, Class="list-group-item")
    edit = html.DIV(id="edit")
    widget <= c
    widget <= container
    container <=  edit
    document["conteiner"] <= widget

  def view_overlays(self, req):
    #alert(req.responseText)
    try:
       overlays = json.loads(req.responseText)
    except SyntaxError:
      alert("Синтаксическая ошибка")
    document['container'] <= html.STRONG( "Доступно:\t" + str(len(overlays["repositories"])) + " Оверлеев")
    widget = html.TABLE(Class="table-striped")
    widget_h = html.THEAD()
    widget_h_l = html.TR()
    widget_h_l <= html.TH("Имя")
    widget_h_l<= html.TH("Описание")
    widget_h_l <= html.TH("Домашняя страничка")
    widget_h <= widget_h_l
    widget <= widget_h
    widget_b = html.TBODY()
    for ov in overlays["repositories"]:

      widget_l = html.TR()
      
      try:
        widget_l <= html.TD(ov['name'])
      except Exception as e:
        print("name: " + str(e))
      try:
        widget_l <= html.TD(ov['description'])
      except Exception as e:
        print("Description: " + str(e))
      try:
        widget_l <= html.TD(html.A(ov['homepage'], href=ov['homepage']))
      except Exception as e:
        print("homepage: " + str(e))
      widget_b <= widget_l
      
    widget <= widget_b 

    document['container'] <= widget
    self.loading()

    
  def get_overlays(self):
    self.loading()
    self.clear_el()
    document['conteiner'] <= html.DIV(id="container")

    req = ajax.ajax()
    req.open('GET', "/ovelays", True)
    location = "/ovelays"
    req.bind('complete', self.view_overlays)
    req.send()
  #document['all'].bind('click', all_pkgs)

  #get_overlays()
  def install_config(self, ev):
    alert(str(ev.currentTarget.id))

# End  Class App

location = '/'
def check_location():
  pass
# change  themes
def set_theme(req):
  pass

def get_theme(theme):
  req = ajax.ajax()
  name = theme + '.css'
  req.open('GET', '/static/css/' + name, True)
  req.bind('complete', set_theme)
  red.send()

def view_console(event):
  try:
    alert("click on %s" %event.currentTarget.id)
  except Exception as e:
    print(e)

app = App()

# All BINDS
 
def h():
  app.main()

def app_s():
  app.get_sett()

def v_overlays():
  app.get_overlays()

def  v_portge_st():
  app.view_st_portage()

def onKDown(event):
  if event.keyCode == 13:
    document['submit_search'].click()

document["overlays"].bind('click', v_overlays)
document["submit_search"].bind('click', app.find_pkg)
document['inS'].bind("keypress", onKDown)
document["app_st"].bind('click', app_s)
document["portage_settngs"].bind('click',  v_portge_st)
document["home"].bind('click', h)

document["debug"].bind("click", view_console)

app.main()