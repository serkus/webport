#-*- coding: UTF-8 -*-
from browser import window, timer, document, ajax, alert, html
import json
from browser.template import Template  
import browser
import ui
from io import StringIO
parser = window.DOMParser.new()
menu_port = {'home': "Главная", 'list_pakages': "Список пакетов", 'overlays':"Оверлеи", 'doc': 'Документации', 'portage_settngs':"Настройка portage",'app_st':"Настройка",'status':"Процесс"}
overlay_cell = ["Имя", "Описание","Домашняя страничка", "Email", "Исходники"]

version = "web_port - 00.0.026"
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
    self.portList = {}
    self.portage_list ={}
    self.req_istall_pkg()
    self.get_settings_portage()
    self.Req_portage_dump()
    self.active =""
    #super(App, self).__init__()

  def get_portage_dump(self, req):
    if req.status == 200:
      d_list = []
      d_list = json.loads(req.responseText)
      
      self.portList = d_list['dump_portage']
      alert(self.portList[0])

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
      list(plist=json.loads(req.responseText)['install_pkgs'])
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
    
  def views_list_pkgs(self, ev):
    item = ev.currentTarget.id
    #tem.Class="menu_active" 
    self.active = str(item)
    print("self.active" + self.active)
    try:
      cont = document[item + "_c"]

      ui.clear_el(item, item + "_c")
    except KeyError:
      cont =  html.UL(id=item + "_c", Class="menu_active")
    for i in  self.portList['Catalog'][item]: 
      MItem = html.LI(i, id=i)
      
      cont <= MItem
      document[item] <= cont
      MItem.bind('click', self.info_pkg)

  def view_package(self):
    ui.clear_el()
    context = html.DIV(id="context")
    Menupackages = html.UL(id="list_p",  Class="list-group")
    dashbord = html.DIV(id="dashbboard", Class="dashboard")
    #catalog = {}
    #print(self.portList["Catalog"])
    for n in self.portList["Catalog"].keys():
      #if c in n.keys():
        #catalog[n.split('/')[0]].append(n.split('/')[1])
        #try:
        #Menupackages <= html.LI(n.split('/')[0], id=n.split('/')[0])
        #except KeyError:
        #else:
        #print(n.split('/')[0])
        #catalog[n.split('/')[0]] = [n.split('/')[0]]
        MenuItems = html.UL(n, id=n)
        MenuItems.bind('click', self.views_list_pkgs)
        Menupackages <= MenuItems
        print(n)
    context <= Menupackages
    document['conteiner'] <= context
    document['conteiner'] <= dashbord
    
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
    #self.loading()

    #print(self.install_apps)
    ui.dashbord_view(json.loads(req.responseText))
    #document[str(i["Name"]) + "_btn"].bind('click', self.install_config)

  def info_pkg(self, ev):
    document['dashbboard'].clear('card')
    pkg = str(ev.currentTarget.id)
    if not pkg.split('/'):
      pkg = self.active + "/" + pkg
    #alert(pkg)
    req =ajax.ajax()
    req.open('GET', '/?p=' + pkg, True)
    alert(pkg)
    #location ='/?p=' + pm
    req.bind('complete', self.view_pkg)
    req.send()

  def find_pkg(self, env):
    document['splash'].style.display = "block"
    ui.clear_el() 
    #pl = json.loads(p_list)
    #self.data = pl
    widget= html.DIV(id="container", Class="")
    w_H = html.HEADER(Class="toolbar toolbar-header")
    w_H <= html.H1("Поиск", Class="title")
    widget <= w_H
    container = html.DIV(Class="window-content")
    widget <= container

    #ui.loading()
    #ui.clear_el()
    p = []
    c = html.OL(id="list_p", Class="list-group")
    c.style.width ='100vw'
    c <= html.HR()
    container <= c
    d = html.DIV(id="dashbboard")
    container <= d
    #c <= html.STRONG("Найдено совпадений:\t" + str(len(pl["Package_result"])))
    for i in self.portList['all_pkgs']:
      if document["inS"].value in i and not i in p:

        print(i) 
        #n = n +1
        p.append(i)
        item = html.P(i, id=i)
        item.bind('click', self.info_pkg)
        c <= item
    document["conteiner"] <= widget
    document['splash'].style.display = 'none'
    
  def route(self, method, url, b_metod):
    req = ajax.ajax()
    req.open(metod, url, True)
    req.bind(b_metod['metod'], b_metod['callback'])

  def show_file(self, ev):
    config = ev.currentTarget.id
    document["edit"].clear('config')

    text = self.portage_list['portage'][config]
    document['edit'] <= html.DIV(id="config")
    n=0
    for t in text:
      n = n+1
      document['config'] <= html.P(t)
        
  def show_settings_portage(self, req):
    print(req.responseText)
    self.portage_list = json.loads(req.responseText)
    #alert(self.portage_list)

  def get_settings_portage(self):
    req = ajax.ajax()
    req.open('GET', '/get_portage', True)
    req.bind('complete', self.show_settings_portage)
    req.send()
  
  def view_st_portage(self):
    #alert(self.portage_list)
    document["conteiner"] <= self.st_portage(self.portage_list)

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
    ui.clear_el()
    document['conteiner'] <= html.DIV(id="container")

    req = ajax.ajax()
    req.open('GET', "/ovelays", True)
    req.bind('complete', self.view_overlays)
    req.send()
  #document['all'].bind('click', all_pkgs)

  #get_overlays()
  def install_config(self, ev):
    alert(str(ev.currentTarget.id))

  def st_portage(self, port_st):
    ui.clear_el()
    widget = html.DIV(id="container", Class="")
    container = html.DIV(Class="window-content")
    w_H = html.HEADER(Class="toolbar toolbar-header")
    w_H <= html.H1("Настройка PORTAGE", Class="title")
    widget <= w_H
    list_port_items = port_st['portage']

    #tab_items = ["make.conf", "package.use", "package.mask", "package.unmask", "sets"]
    c = html.DIV(id="ps_menu", Class="list-group")
    for i in list_port_items.keys():
      it = html.DIV(i, Class="list-group-item", id=i)
      c <= it
      it.bind("click", self, self.show_file)

    edit = html.DIV(id="edit")
    widget <= c
    widget <= container
    container <=  edit
    return widget

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

def on_v_p():
  app.view_package()

document["overlays"].bind('click', v_overlays)
document["submit_search"].bind('click', app.find_pkg)
document['inS'].bind("keypress", onKDown)
document["app_st"].bind('click', app_s)
document["portage_settngs"].bind('click',  v_portge_st)
document["list_pakages"].bind('click', on_v_p)
document["home"].bind('click', h)

document["debug"].bind("click", view_console)
if  __name__  ==  '__main__':
  app.m_req()