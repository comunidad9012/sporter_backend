# Explicar como preparse para desarrollar

## Requerimientos

Previo a poder desarrollar algo con este repositorio hay que cumplir algunos requisitos:

- MySQL instalado
- Python 3.10 (preferiblemente) o mayor

## Pasos de Setup

### 1- Clonar repositorio

Clonar el repositorio desde github para comenzar a configurar el entorno de desarrollo, elije en que directorio comenzaras a desarrollar y luego:

``` bash
  $ git clone  git@github.com:sporter-management/product_api_service.git
        git clone output...
```

Para continuar debemos ingresar al directorio del proyecto:

``` bash
   $ cd product_api_service
```

### 2- Entorno Virtual y dependencias

A continuación corresponde crear un entorno virual, para se pueden utilizar distintas herramientas, dos de las más comunes son `virtualenv` y el módulo de Python `venv`.

Con `venv`:

``` bash
    # Para windows reemplazar python3 por python
    $ python3 -m venv <nombre_del_entorno_virtual>
```

Con `virtualenv`:

``` bash
    $ virtualenv <nombre_del_entorno_virtual>
```

Una vez creado el entorno virtual, debemos activarlo:

``` bash
    # En windows
    $ nombre_del_entorno_virtual\\Scripts\\activate
```

``` bash
    # En linux
    $ source nombre_del_entorno_virtual\\bin\\activate
```

Puedes verificar que el entorno virual este activado con `which python3` en Linux y `where python` en Windows, el resultado del comando deberia mostrar un string en formato PATH ('/algo/asi/luciria' o 'C:\algo\asi\luciria') que indica que python se está usando, el python que se este usando deberia estar en un PATH que dirija al entorno virtual.

Ahora debemos instalar las dependencias:

``` bash
    $ pip install -r requirements.txt
```

### 3- Establecer configuracion de entorno de aplicacion

Ahora estableceremos unas variables de entorno para la ejecución de la aplicación, estas permitiran conectar a la base de datos sin exponer los secretos en el Control de Versiones.

De momento seguimos parados en el directorio del proyecto, que luciria algo asi: 

``` bash
    product_api_service < --- aqui estamos parados y podemos ver los archivos mencionados.
    ├── .gitignore
    ├── LICENSE
    ├── .python-version
    ├── README.md
    ├── requirements.txt
    ├── TODO.md
    ├── nombre_del_entorno_virtual
    ├── dev_setup
    ├── .git
    └── product_api_service
```

Ahora necesitamos crear un archivo llamado `.env`, en el que definiremos los datos de acceso para la base de datos, copia lo siguiente y reemplaza segun tu servidor local de MySQL:

``` bash
# MYSQL Congiguration
    MYSQL_DRIVERNAME=mysql+mysqlconnector
    MYSQL_USERNAME=tu_nombre_de_usuario_mysql
    MYSQL_PASSWORD=tu_contraseña_de_usuario_mysql
    # (seguramente es `localhost`!)
    MYSQL_HOST=host_de_mysql
    # puede ser otro puerto, pero lo mas seguro es que no!
    MYSQL_PORT=3306
    # de ser posible, no cambies esto, pero no deberia haber problema si lo haces
    MYSQL_DATABASE=sporter_product_database
    # Aqui puedes configurar los datos para el administrador
    # que el sistema creara por defecto
    APP_ADMIN_NAME=admin
    APP_ADMIN_PASS=password
    APP_ADMIN_EMAIL=admin@example.com
```

### 4- Levantar la Base de Datos

Una vez hayas instalado las dependencias y configurado las variables de entorno, nos corresponse levantar la base de datos. Para esto recuerda que debes tener MySQL instalado y corriendo y los datos de acceso que definiste en el paso anterior deben ser los correctos. Toma un momento para verificarlo y a continuación corre los siguientes comandos:

``` bash
    $ flask --app product_api_service db-cli crear-todo
```

Ahora puedes verificar que la base de datos haya sido creada, su nombre será el que se definió en `MYSQL_DATABASE` y esta base de datos contendrá de momento una sola tabla llamada `producto`.

### 5 - Programar

Ahora abre el directorio en el que estamos parados con tu editor de texto o IDE favorito y comienza a desarrollar!
