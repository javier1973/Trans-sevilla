<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head >
    <title>Trans Sevilla</title>
  </head>
  <h3>Listado de nodos disponibles</h3>
<form action="/nodo_d" method="post">
   <select name="lista_nodos_d">
  %for i in nombre:
	<option value="{{i}}">{{i}}</option>
  %end
  </select>
  <input type="submit" value="Enviar">

</form>


</html>
