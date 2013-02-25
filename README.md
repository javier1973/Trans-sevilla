Trans-sevilla
=============

Seleción del transporte publico más eficiente para nuestor destino en Sevilla

Para comenzar vamos a localizar las paradas de las distintas lineas, con el fin de poder 
representarlas en un mapa (si es posible en (openstreetmap), para ello necesitamos obtener
 un listado de las lineas operativas.

Por ahora no se he consequido un listado de lineas desde la web, de seguir sin conseguirlo
creare una lista con las lineas.

Con este codigo en pytho obtenemos un listado de las paradas de una linea en un sentido determinado.
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

Este es un fragmento de la informacion obtenida en la que vemos los datos que se obtiene por nodo(parada).
