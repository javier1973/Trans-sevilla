#este es la api de tussam
#realizamos una petición a la api de tussam con la line y el numero de parada
#nos devuelve el dos autobuses mas cercanos con distancia y tiempo estimado para
#llegar a la parada
from suds.client import Client
cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl ')
print cliente.service.GetPasoParada ("26","357",1)
