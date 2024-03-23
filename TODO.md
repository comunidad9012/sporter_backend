# Tareas

- Programar endpoint /producto/crear
  - El endpoint debe recibir una peticion POST y un formulario con los siguientes campos
    - nombre  
    - descripcion
    - precio
    - existencias
- Programar endpoint /producto/eliminar/<id>
  - El endpoint debe recibir una peticion POST donde <id> se reemplazara por la id del producto y debe eliminarlo
- Programar endpoint /producto/actualizar/<id>
  - El endpoint debe recibir una peticion POST donde <id> se reemplazara por la id del producto y debe actualizarlo
  - Como /crear, recibira un formulario con los mismos datos
- Programar endpoint /producto/leer/<id>
  - peticion tipo GET
  - como eliminar pero debe retornar un JSON con toda la informacion del producto indicado
- Programar endpoint /producto/leer/total
  - debe recibir una peticion tipo GET y devolver un JSON que sea una lista compuesta de objetos js (diccionarios python) conteniendo TODOS los productos
