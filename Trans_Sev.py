from urllib2 import urlopen
from json import load
from bottle import route, run, template, request, debug
from math import sin, cos, sqrt, asin, pi
import bottle
from suds.client import Client
from lxml import etree

urlt = 'http://api.citybik.es/sevici.json'
bicis = load(urlopen(urlt))

@route('/index')
def home():
	return template('index')

@route('/lista_nodos_o')
def lista_nodos():
	nombre = []
	for i in bicis:
		nombre.append(i.get('name'))
	return template('lista_nodos_o', nombre=nombre)
	
@route ('/nodo_o', method ='post')

def nodo_o():
	global nbicis_o, libres_o, lat_o, lng_o, pto_o
	pto_o = request.forms.get('lista_nodos_o')
	x = 1
	while pto_o != bicis[x].get('name'):
		x = x +1
	nbicis_o = bicis[x].get('bikes')
	libres_o = bicis[x].get('free')
	lat_o = bicis[x].get('lat')
	lng_o = bicis[x].get('lng')
	return template ('nodo_o', pto_o=pto_o, nbicis_o=nbicis_o, libres_o=libres_o, lat_o=lat_o, lng_o=lng_o)
    
@route('/lista_nodos_d')
def lista_nodos_d():
	nombre = []
	for i in bicis:
		nombre.append(i.get('name'))

	return template('lista_nodos_d', nombre=nombre)
	
@route ('/nodo_d', method ='post')
def nodo_d():
	global nbicis_d, libres_d, lat_d, lng_d
	pto_d = request.forms.get('lista_nodos_d')
	#	bucle que me recorra bicis hasta llegar al punto del nodo seleccionado para tomar los datos del nodo	
	x = 1
	while pto_d != bicis[x].get('name'):
		x = x +1
	nbicis_d = bicis[x].get('bikes')
	libres_d = bicis[x].get('free')
	lat_d = bicis[x].get('lat')
	lng_d = bicis[x].get('lng')
	dist = distancia (lat_o,lng_o,lat_d,lng_d)
	return template ('nodo_d',pto_o=pto_o, nbicis_o=nbicis_o, libres_o=libres_o, lat_o=lat_o, lng_o=lng_o , pto_d=pto_d, nbicis_d=nbicis_d, libres_d=libres_d, lat_d=lat_d, lng_d=lng_d, dist=dist)    

def distancia(lat1,long1,lat2,long2):
#fórmula Harvesine para el calculo de la distancia de dos coordenadas.
# pendiente convaersion de coordenadas UTM a decimales
	r = 6371000 #radio terrestre medio, en metros
 	c = pi/180 #constante para transformar grados en radianes
	d = 2*r*asin(sqrt(sin(c*(lat_d-lat_o)/2)**2 + cos(c*lat_o)*cos(c*lat_d)*sin(c*(lng_d-lng_o)/2)**2))
	return d


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

@route('/lista_parada_linea',method = 'post')
def lista_paradas_linea():
	#~ global linea_o
	linea_o = request.forms.get('lista_lineas')
	cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl',retxml=True)
	pd=cliente.service.GetNodosMapSublinea (linea_o,1)
	paradas = etree.fromstring(pd)
	ns ={"ns":"http://tempuri.org/","soap":"http://schemas.xmlsoap.org/soap/envelope/" } #definimos el namespace
	nodo = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:nodo', namespaces = ns)
	nombre = paradas.xpath('/soap:Envelope/soap:Body/ns:GetNodosMapSublineaResponse/ns:GetNodosMapSublineaResult/ns:InfoNodoMap/ns:nombre', namespaces = ns)
	nd=[]
	lg=(len(nombre))
	for i in xrange(lg):
		dicc={}
		dicc["nodo"] = nodo[i].text
		dicc["nombre"] = nombre[i].text
		nd.append(dicc)
	return template ('lista_parada_linea',nd=nd,lg=lg)

@route('/proximo_bus',method = 'post')
def proximo_bus():
	cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl',retxml=True)
	linea_o = request.forms.get('lista_lineas')
	parada_o = request.forms.get('lista_parada_linea')
	cliente.service.GetPasoParada (linea_o,parada_o,1)
	cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl',retxml=True)
	abus=cliente.service.GetPasoParada ("12","974",1)
	ab = etree.fromstring(abus)
	ns ={"ns":"http://tempuri.org/","soap":"http://schemas.xmlsoap.org/soap/envelope/" } #definimos el namespace
	#print etree.tostring(ab , pretty_print = True) #imprimios el contenido del xml
	#~ lineas = cliente.service.GetLineas()
	#~ lin = etree.fromstring(lineas)
	minu_1 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:minutos', namespaces = ns)
	metros_1 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:metros', namespaces = ns)
	minu_2 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:minutos', namespaces = ns)
	metros_2 = ab.xpath('/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:metros', namespaces = ns)
	return template ('proximo_bus',minu_1=minu_1,metros_1=metros_1,minu_2=minu_2,metros_2=metros_2)

        
debug(True)    
run(host='localhost', port=8080)
