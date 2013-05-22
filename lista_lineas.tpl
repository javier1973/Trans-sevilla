<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head >
    <title>Trans Sevilla</title>
  </head>
  <h3>Listado de lineas disponibles</h3>
<form action="/lista_parada_linea" method="post">
   <select name="lista_lineas">
	%for i in xrange(lg):
	    <option value="{{lbl[i]['linea']}}">{{lbl[i]['linea']}} {{lbl[i]['nombre']}}</option>
	%end
  </select>
  <input type="submit" value="Enviar">
</form>
</html>
