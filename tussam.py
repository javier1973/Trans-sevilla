from suds.client import Client
from lxml import etree
from lxml.html import soupparser
#este es la api de tussam


# Para realizar consultas de datos dinámicos
#cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl',retxml=True)

#realizamos una petición a la api de tussam con la line y el numero de parada
#nos devuelve el dos autobuses mas cercanos con distancia y tiempo estimado para
#llegar a la parada
#print cliente.service.GetPasoParada ("12","974",1)


# Para realizar consultas de datos estaticos
cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl',retxml=True)

#de esta forma obtenemos listado de todas las peticiones que podemos hacer a la url estatica 
#print cliente

#De esta froma podemos consultar los nodos(paradas) de una linea
#print cliente.service.GetNodosMapSublinea ("12",1)


#Conseguimos listado de las lineas actuales

lineas = cliente.service.GetLineas()
print ('lineas es del tipo: ',type(lineas))
#lin = soupparser.fromstring(lineas)
lin = etree.fromstring(lineas)
print ('lin :', type (lin))
#linea = etree.XMLID(lineas)
#linea = etree.ElementTree(element=lin)
#print linea

print etree.tostring(lin , pretty_print = True)
#print ('lin es del tipo: ',type(lin))
#print ('linea es del tipo: ',type(linea))
#ln = lin.xpath("/soap:Envelope/soap:Body/GetLineasResponse/GetLineasResult/InfoLinea/sublineas/InfoSublinea")
#print ('ln es del tipo: ',type(ln))
#for i in lin :
#    print 
    
#De esta forma obtenemos coordenadas del trazado de una linea
#print cliente.service.GetPolylineaSublinea ("13",1)
