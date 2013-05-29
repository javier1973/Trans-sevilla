<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head >
    <title>Trans Sevilla</title>
    <link rel="stylesheet" type="text/css" href="css/estilo.css">	
  </head>
  <div id="tussam">
		<p>
		   <a href="index">Inicio</a>
		   <a href="lista_lineas">Autobus</a>
		   <a href="lista_nodos_o">Bicicleta</a>
		</p>
	</div>
  <h3>Listado de lineas disponibles</h3>
<form action="/resumen_bus" method="post" >
   <select name="lista_parada_linea_destino">
	%for i in xrange(lg):
	    <option value="{{nd_d[i]['nodo']}}">{{nd_d[i]['nodo']}} {{nd_d[i]['nombre']}}</option>
	%end
  </select>
  <input type="submit" value="Enviar">
</form>
</html>
