from suds.client import Client
#este es la api de tussam
#realizamos una petición a la api de tussam con la line y el numero de parada
#nos devuelve el dos autobuses mas cercanos con distancia y tiempo estimado para
#llegar a la parada

cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl ')
print cliente.service.GetPasoParada ("26","357",1)



#de esta forma obtenemos listado de todas las peticiones que podemos hacer a la url estatica 
cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl ')
print cliente

#De esta froma podemos consultar los nodos(paradas) de una linea
cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl ')
print cliente.service.GetNodosMapSublinea ("01",1)


#Conseguimos listado de las lineas actuales
cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl ')
print cliente.service.GetLineas()


#De esta forma obtenemos coordenadas del trazado de una linea
cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl ')
print cliente.service.GetPolylineaSublinea ("13",1)
