#-*- coding: UTF-8 -*-
from browser import window, timer, document, ajax, alert, html
import json
from browser.template import Template  
import browser
import ui
from io import StringIO
parser = window.DOMParser.new()
menu_port = {'home': "Главная",'overlays':"Оверлеи", 'doc': 'Документации', 'portage_settngs':"Настройка portage",'app_st':"Настройка",'status':"Процесс"}
overlay_cell = ["Имя", "Описание","Домашняя страничка", "Email", "Исходники"]

version = "web_port - 00.0.025"
#document['v'].bind('click', view_row)
# Temlate Menu
Template(document["link_panel"]).render(menu_port=menu_port)
#Template(document["nav_memu"]).render(catalog=catalog)
# location

#document['btnSclose'].bind('click', view_search)

def view_catalog():
  pass

class App():
  """docstring for App"""
  def __init__(self):
    self.data =""
    self.widget_tables = ["Новости", "Рекомендации", "Документация"]
    self.install_apps = []
    self.portList = []
    self.portage_list ={}
    self.req_istall_pkg()
    self.get_settings_portage()
    self.Req_portage_dump()

    #super(App, self).__init__()

  def get_portage_dump(self, req):
    if req.status == 200:
      d_list =[]
      d_list = json.loads(req.responseText)

      self.portList = d_list['dump_portage']

    elif req.status == 404:
      alert('Путь не найден')
    elif req.status == 403:
      alert("Доступ запрещён")

  def Req_portage_dump(self):
    req = ajax.ajax()
    req.open('GET', '/get_dump_list', True)
    req.bind('complete', self.get_portage_dump)
    req.send()

  def p_install_list(self, req):
    if req.status == 200:
      list(plist= json.loads(req.responseText)['install_pkgs'])
      alert(plist)
      self.install_apps = plist
      #alert(self.install_apps)
    elif req.status == 404:
      alert('Путь не найден')
    elif req.status == 403:
      alert("Доступ запрещён")
      
    return plist

  def req_istall_pkg(self):
    req = ajax.ajax()
    req.open('GET', '/get_dump_list', True)
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

  def main(self, req):
    #alert(str(req.responseText))
    document["conteiner"] <= ui.v_main(req.responseText, self.widget_tables)

  def m_req(self):
    req = ajax.ajax()
    req.open('GET', "/main", True)
    req.bind('complete', self.main)
    req.send()

  def show_result(self, req):
    if req.status == 200:
      alert("Конфигурация прянята и вступит в силу после перезагрузки приложения")
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
    
    document["conteiner"] <= ui.v_app_settings(json.loads(req.responseText))
    document['App_save'].bind('click', self.app_save)

  def get_sett(self):
    req = ajax.ajax()
    req.open("GET", "/get_settings_app", True)
    req.bind('complete', self.app_settings)
    req.send()

  def view_pkg(self, req):
    self.loading()

    #print(self.install_apps)
    ui.dashbord_view(json.loads(req.responseText))
    #document[str(i["Name"]) + "_btn"].bind('click', self.install_config)

  def info_pkg(self, ev):
    self.loading()
    document['dashbboard'].clear('card')
    pkg = str(ev.currentTarget.id)
    req =ajax.ajax()
    req.open('GET', '/?p=' + pkg,True)
    #location ='/?p=' + pm
    req.bind('complete', self.view_pkg)
    req.send()


  def find_bind(self, p_list):    #req):  
    #if req.status == 200 or req.status == 0:
      #alert(req.responseText)
    self.clear_el()
    self.loading()

    pl = json.loads(p_list)
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
      c = html.OL(id="list_p", Class="list-group")
      c.style.width ='100vw'
      d = html.DIV(id="dashbboard")
      c <= html.STRONG("Найдено совпадений:\t" + str(len(pl["Package_result"])))
      c <= html.HR()
      container <= c
      container <= d
      document["conteiner"] <= widget
            
      for i in pl["Package_result"]: 
        #n = n +1
        item = html.P(i, id=i)
        item.bind('click', self.info_pkg)
        c <= item

  def find_pkg(self, req):
    p = []
    self.clear_el()
    self.loading()
    for i in self.portList:
      if document["inS"].value in i and not i in p:
        print(i)
        p.append(str(i))
        #json.dumps({"Package_result": pk})
   
    self.clear_el()
    self.find_bind(str(json.dumps({"Package_result": p})))
    

  def route(self, method, url, b_metod):
    req = ajax.ajax()
    req.open(metod, url, True)
    req.bind(b_metod['metod'], b_metod['callback'])

  def show_file(ev):
    config = ev.currentTarget.id
    for e in self.portage_list['ev.currentTarget.id']:
      document['edit'] <= html.P(e)

  def show_settings_portage(self, req):
    print(req.responseText)
    self.portage_list = json.loads(req.responseText)

  def get_settings_portage(self):
    req = ajax.ajax()
    req.open('GET', '/get_portage', True)
    req.bind('complete', self.show_settings_portage)
    req.send()
  
  def view_st_portage(self):
    alert(self.portage_list)
    document["conteiner"] <= ui.st_portage(self.portage_list)

  def view_overlays(self, req):
    #alert(req.responseText)
    try:
       overlays = json.loads(req.responseText)
    except SyntaxError:
      alert("Синтаксическая ошибка")

    document['container'] <= ui.overlays(overlays)
    self.loading()
  
  def get_overlays(self):
    self.loading()
    self.clear_el()
    document['conteiner'] <= html.DIV(id="container")

    req = ajax.ajax()
    req.open('GET', "/ovelays", True)
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

app = App()

def view_console(event):
  alert(app.portList)

# All BINDS
 
def h():
  app.m_req()

def app_s():
  app.get_sett()

def v_overlays():
  app.get_overlays()

def v_portge_st():
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
if  __name__  ==  '__main__':
  app.m_req()