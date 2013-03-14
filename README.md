Trans-sevilla
=============

Selección del transporte publico más eficiente para nuestro destino en Sevilla.












Obtencion de datos
==================

La empresa municipal de servicio de autobus facilita desde su plataforma web informacion sobre el servicio ofertdo que se puede consultar para tratar la informcion, desde esta url "http://www.infobustussam.com:9001/services/estructura.asmx" nos da información de el tipo de consultas que podemos hacer.
Asi podemos consultar datos estaticos, lineas, paradas ...




de esta forma obtenemos listado de todas las peticiones que podemos hacer a la url estática 
cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl ')
print cliente




Para comenzar vamos a localizar las paradas de las distintas lineas, con el fin de poder 
representarlas en un mapa (si es posible en (openstreetmap), para ello necesitamos obtener
un listado de las lineas operativas.


De este modo obtenemos un listado de las lineas operativas.
cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl ')
print cliente.service.GetLineas()

Con este código en python obtenemos un listado de las paradas de una linea en un sentido determinado.
si realizamos la consulta recorriendo una lista con las lineas y indicando los dos sentidos de cada
linea, obtendremos todas las paradas de las lineas de autobuses.

"cliente = Client('http://www.infobustussam.com:9001/services/estructura.asmx?wsdl ')"
"print cliente.service.GetNodosMapSublinea ("01",1)"

(ArrayOfInfoNodoMap){
   InfoNodoMap[] = 
      (InfoNodoMap){
         nodo = 2
         tipo = 1
         nombre = "MENÉNDEZ PELAYO (PUERTA CARMONA)"
         label = "01"
         visible = True
         posx = 235851.0625
         posy = 4142363.75
      },
      (InfoNodoMap){
         nodo = 3
         tipo = 1
         nombre = "MENÉNDEZ PELAYO (PUERTA DE LA CARNE)"
         label = "01"
         visible = True
         posx = 235735.296875
         posy = 4142099.5

Este es un fragmento de la información obtenida en la que vemos los datos que se obtiene por nodo(parada).

Ya hemos conseguido identificar lineas y paradas, necesitamos tratar el resultado para poder hacer una petición que nos diga cuando llega el próximo autobús.

Esta petición nos da el tiempo estimado en llegar de los dos autobuses más cercanos a la parada, hemos saber la parada, linea y sentido.

cliente = Client('http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl ')
print cliente.service.GetPasoParada ("26","357",1)
