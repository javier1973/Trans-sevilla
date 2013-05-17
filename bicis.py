from urllib2 import urlopen
from json import load
from bottle import route, run, template, request, debug
from math import sin, cos, sqrt, asin, pi
import bottle


urlt = 'http://api.citybik.es/sevici.json'

#for i in bicis:
#    print i.get('name'),'Identificador:' ,'Número',i.get('number'),'Nº bicis' ,i.get('bikes'),'Libres:',i.get('free')
#nombre = bicis[1].get('name')
bicis = load(urlopen(urlt))

@route('/')
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
#	fórmula Harvesine para el calculo de la distancia de dos coordenadas.
# pendiente convaersion de coordenadas UTM a decimales
	r = 6371000 #radio terrestre medio, en metros
 	c = pi/180 #constante para transformar grados en radianes
	d = 2*r*asin(sqrt(sin(c*(lat_d-lat_o)/2)**2 + cos(c*lat_o)*cos(c*lat_d)*sin(c*(lng_d-lng_o)/2)**2))

 
	return d
        
debug(True)    
run(host='localhost', port=8080)
