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
  <body>
	<h3>Resultado de la consulta: {{nm_o}}--{{nm_d}}</h3>
	<div id="res">
		<p>Parada de origen es {{nm_o}}</p>
		<p>con coordenadas latitud {{lat_o}} y longitud {{lng_o}}</p>
		<p>Parada de destino es {{nm_d}}</p>
		<p>con coordenadas latitud {{lat_d}} y longitud {{lng_d}}</p>
		<p>Se encuentra a una distancia de {{dist}} metros</p>
		<p>Con una velocidad estimada de 15 km/h tardara  {{tmp}} minutos</p>
    </div>
    <p><a href="index">Volver al menu principal</a> </p>
  </body>
</html>
