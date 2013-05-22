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


cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl',retxml=True)
lineas = cliente.service.GetLineas()
#print ('lineas es del tipo: ',type(lineas))
lin = etree.fromstring(lineas)

#print etree.tostring(lin , pretty_print = True) #imprimios el contenido del xml
ns ={"ns":"http://tempuri.org/","soap":"http://schemas.xmlsoap.org/soap/envelope/" } #definimos el namespace
nombre = lin.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:nombre", namespaces = ns)
label = lin.xpath('/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:label', namespaces = ns)
sublinea = lin.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:sublineas/ns:InfoSublinea/ns:sublinea", namespaces = ns)
for i in xrange(1,len(label)):
	print ("Linea ",label[i].text,"nombre ",nombre[i].text,'sublinea ',sublinea[i].text)

#print ('lin es del tipo: ',type(lin))
#print ('label es del tipo: ',type(label))
#print ('la longitud de label : ',len(label))
#print ('la longitud de nombre : ',len(nombre))
#print ('la longitud de label : ',len(sublinea))
#for i in xrange(1,len(label)):
#print ('Linea ',label[i].text,'nombre ',nombre[i].text,'sublinea ',sublinea[i].text)

