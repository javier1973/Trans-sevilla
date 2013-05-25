from suds.client import Client
from lxml import etree
from bottle import route, run, template, request, debug
from math import sin, cos, sqrt, asin, pi
import bottle

#este es la api de tussam


# Para realizar consultas de datos dinamicos
#cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl',retxml=True)

#realizamos una peticion a la api de tussam con la line y el numero de parada
#nos devuelve el dos autobuses mas cercanos con distancia y tiempo estimado para
#llegar a la parada
#print cliente.service.GetPasoParada ("12","974",1)


# Para realizar consultas de datos estaticos
#cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl',retxml=True)

#de esta forma obtenemos listado de todas las peticiones que podemos hacer a la url estatica 
#print cliente

#De esta froma podemos consultar los nodos(paradas) de una linea
#print cliente.service.GetNodosMapSublinea ("12",1)
    
#De esta forma obtenemos coordenadas del trazado de una linea
#print cliente.service.GetPolylineaSublinea ("13",1)

#Conseguimos listado de las lineas actuales

@route('/')
def home():
	return template('index')

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
