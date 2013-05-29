from urllib2 import urlopen
from json import load
from bottle import route, run, template, request, debug, static_file
from math import sin, cos, sqrt, asin, pi
import bottle
from suds.client import Client
from lxml import etree
from decimal import *
from pyproj import Proj

@route('/index')
def home():
	return template('index')


###################################################################
##########  inicio de los precedimiento de las bicis  #############
###################################################################
# consultamos la api un tomamos los datos de todos los nodos de bicis en json.
urlt = 'http://api.citybik.es/sevici.json'
bicis = load(urlopen(urlt))

	
#dfinimos dosnde estea la hoja de estilo
@route('/css/:filename#.*#')
def server_static(filename):
    return static_file(filename, root='./css/')	

#creasmo lista con los nodos de las vicicletas y lo pasamos al template
@route('/lista_nodos_o')
def lista_nodos():
	nombre = []
	for i in bicis:
		nombre.append(i.get('name'))
	return template('lista_nodos_o', nombre=nombre)
	

#obtenemos el nodo seleccionado y paasmos al template los datos de dicho nodo
@route ('/nodo_o', method ='post')
def nodo_o():
	global nbicis_o, libres_o, lat_o, lng_o, pto_o
	pto_o = request.forms.get('lista_nodos_o')
	x = 1
	while pto_o != bicis[x].get('name'):#	bucle que me recorre bicis hasta llegar al punto del nodo seleccionado para tomar los datos del nodo
		x = x +1
	nbicis_o = bicis[x].get('bikes')
	libres_o = bicis[x].get('free')
	lat_o = bicis[x].get('lat')
	lng_o = bicis[x].get('lng')
	return template ('nodo_o', pto_o=pto_o, nbicis_o=nbicis_o, libres_o=libres_o, lat_o=lat_o, lng_o=lng_o)
    
#creasmo lista con los nodos de las vicicletas y lo pasamos al template
@route('/lista_nodos_d')
def lista_nodos_d():
	nombre = []
	for i in bicis:
		nombre.append(i.get('name'))

	return template('lista_nodos_d', nombre=nombre)

#obtenemos el nodo seleccionado y paasmos al template los datos de dicho nod	
@route ('/nodo_d', method ='post')
def nodo_d():
	global nbicis_d, libres_d, lat_d, lng_d
	pto_d = request.forms.get('lista_nodos_d')
	x = 1
	while pto_d != bicis[x].get('name'):#	bucle que me recorre bicis hasta llegar al punto del nodo seleccionado para tomar los datos del nodo
		x = x +1
	nbicis_d = bicis[x].get('bikes')
	libres_d = bicis[x].get('free')
	lat_d = bicis[x].get('lat')
	lng_d = bicis[x].get('lng')
	dist = round(distancia (lat_o,lng_o,lat_d,lng_d),2)
	tmp = round((dist/4.166)/60,2) #estimamos una velocidad de 15 km/h
	return template ('nodo_d',pto_o=pto_o, nbicis_o=nbicis_o, libres_o=libres_o, lat_o=lat_o, lng_o=lng_o , pto_d=pto_d, nbicis_d=nbicis_d, libres_d=libres_d, lat_d=lat_d, lng_d=lng_d, dist=dist, tmp=tmp)    



#calculamos la distancia se pasan las coordenadas de los dos nodos
#las coordenadas han de estar en º '"
def distancia(lat1,lng1,lat2,lng2):
#fórmula Harvesine para el calculo de la distancia de dos coordenadas.
# pendiente convaersion de coordenadas UTM a decimales
	p = Proj(proj='utm',zone=30,ellps='WGS84')
	l1x, l1y = p(lat1,lng1,inverse=True)
	l2x, l2y = p(lat2,lng2,inverse=True)
	r = 6371000 #radio terrestre medio, en metros
 	c = pi/180 #constante para transformar grados en radianes
	d = 2*r*asin(sqrt(sin(c*(l2x-l1x)/2)**2 + cos(c*l1x)*cos(c*l2x)*sin(c*(l2y-l1y)/2)**2))
	return d

###################################################################
#############  inicio de los precedimiento de tussam  #############
###################################################################



#consultamos la api de tussam y creamos una lista con las lineas que pasamos al template
@route('/lista_lineas')
def lista_lineas():
	cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl',retxml=True)
	lineas = cliente.service.GetLineas()
	lin = etree.fromstring(lineas)
	ns ={"ns":"http://tempuri.org/","soap":"http://schemas.xmlsoap.org/soap/envelope/" } #definimos el namespace
	label = lin.xpath('/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:label', namespaces = ns)
	nombre = lin.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:nombre", namespaces = ns)
	sublinea = lin.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:sublineas/ns:InfoSublinea/ns:sublinea", namespaces = ns)
	lbl=[]
	lg=(len(nombre))
	for i in xrange(lg):
		dicc = {}
		dicc["linea"] = label[i].text
		dicc["nombre"] = nombre[i].text
		lbl.append(dicc)
	return template ('lista_lineas',lbl=lbl,lg=lg)

#obtenemos la linea seleccionamos y consultamos las paradas a la apiy se los pasamos al template 
@route('/lista_parada_linea',method = 'post')
def lista_paradas_linea():
	global nd, linea_o
	linea_o = request.forms.get('lista_lineas')
	cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl',retxml=True)
	pd=cliente.service.GetNodosMapSublinea (linea_o,1)
	paradas = etree.fromstring(pd)
	ns ={"ns":"http://tempuri.org/","soap":"http://schemas.xmlsoap.org/soap/envelope/" } #definimos el namespace
	nodo = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:nodo', namespaces = ns)
	nombre = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:nombre', namespaces = ns)
	posx_o = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:posx', namespaces = ns)
	posy_o = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:posy', namespaces = ns)
	nd=[]
	lg=(len(nombre))
	for i in xrange(lg):
		dicc={}
		dicc["nodo"] = nodo[i].text
		dicc["nombre"] = nombre[i].text
		dicc["posx_o"] = posx_o[i].text
		dicc["posy_o"] = posy_o[i].text
		nd.append(dicc)
	return template ('lista_parada_linea',nd=nd,lg=lg)

#obtenemos los datos de la linea y la parada y hacemos la consulta para el proximo autobus
#el resultado lo pasamos al template
@route('/proximo_bus',method = 'post')
def proximo_bus():
	global minu_1, minu_2, metros_1, metros_2, lat_o, lng_o, nm_o
	cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl',retxml=True)
#	linea_o = request.forms.get('lista_lineas')
	parada_o = request.forms.get('lista_parada_linea')
	abus = cliente.service.GetPasoParada (linea_o,parada_o,1)
	ab = etree.fromstring(abus)
	ns ={"ns":"http://tempuri.org/","soap":"http://schemas.xmlsoap.org/soap/envelope/" } #definimos el namespace
	minu_1 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:minutos', namespaces = ns)
	metros_1 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:metros', namespaces = ns)
	minu_2 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:minutos', namespaces = ns)
	metros_2 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:metros', namespaces = ns)
	i = 0
	while (nd[i]['nodo'] != parada_o):
		i=i+1
	lat_o = nd[i]['posx_o']
	lng_o = nd[i]['posy_o']
	nm_o = nd[i]['nombre']
	
	return template ('proximo_bus',minu_1=minu_1,metros_1=metros_1,minu_2=minu_2,metros_2=metros_2)
    

	
#obtenemos la linea seleccionamos y consultamos las paradas a la apiy se los pasamos al template 
@route('/lista_parada_linea_destino')
#@route('/lista_parada_linea_destino',method = 'post')
def lista_parada_linea_destino():
	global nd_d
#	linea_o = request.forms.get('lista_lineas')
	cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl',retxml=True)
	pd=cliente.service.GetNodosMapSublinea (linea_o,1)
	paradas = etree.fromstring(pd)
	ns ={"ns":"http://tempuri.org/","soap":"http://schemas.xmlsoap.org/soap/envelope/" } #definimos el namespace
	nodo = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:nodo', namespaces = ns)
	nombre = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:nombre', namespaces = ns)
	posx_d = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:posx', namespaces = ns)
	posy_d = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:posy', namespaces = ns)
	nd_d=[]
	lg=(len(nombre))
	for i in xrange(lg):
		dicc={}
		dicc["nodo"] = nodo[i].text
		dicc["nombre"] = nombre[i].text
		dicc["posx_d"] = posx_d[i].text
		dicc["posy_d"] = posy_d[i].text
		nd_d.append(dicc)
	return template ('lista_parada_linea_destino',nd_d=nd_d,lg=lg)

@route('/resumen_bus',method = 'post')
def resumen_bus():
	global lat_d, lng_d
	cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl',retxml=True)
	linea_o = request.forms.get('lista_lineas')
	parada_d = request.forms.get('lista_parada_linea_destino')
	i = 0
	while (nd_d[i]['nodo'] != parada_d):
		i=i+1
	nm_d = nd_d[i]['nombre']
	lat_d = nd_d[i]['posx_d']
	lng_d = nd_d[i]['posy_d']
	x_o = float(lat_o)
	x_d = float(lat_d)
	y_o = float(lng_o)
	y_d = float(lng_d)
	dist=round(distancia(x_o,y_o,x_d,y_d),2)
	tmp= round((dist/4.166)/60,2) #estimamos una velocidad de 15 km/h
	return template ('resumen_bus',linea_o=linea_o, nm_o=nm_o, nm_d=nm_d ,nodo_o=nodo_o, nodo_d=nodo_d, lat_o=lat_o, lng_o=lng_o, lat_d=lat_d, lng_d=lng_d, dist=dist, tmp=tmp)

       
       
debug(True)    
run(host='localhost', port=8080)
