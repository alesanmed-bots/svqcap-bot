CapturaBot
=======
CapturaBot es un bot de Telegram que permite pedir capturas a Intel. En esta guía se indica el funcionamiento básico del bot cómo descargarlo y prepararlo para su uso en cualquier lugar.

## Funcionamiento ##
El funcionamiento del bot se sencillo. El bot **no acepta comandos**. El bot únicamente acepta una ubicación. En ese momento comenzará el proceso de petición de captura, momento en el cual el bot preguntará el nivel de zoom que se desea, pudiendo seleccionar uno de los niveles que aparecen en el teclado o escribir el nivel deseado siempre que sea un número entre 3 (el mundo entero) y 17 (todos los portales). Una vez se seleccione el nivel de zoom deseado el bot informará de que ha recibido la información y en unos segundos tendrá la captura. En ese momento, el bot le enviará la imagen con la captura realizada.

## Despliegue ##
El bot puede ser desplegado por cualquiera para ofrecer el uso del mismo a su comunidad. El proceso de despliegue se explica a continuación.

**Pre-requisitos:**
1. Python 3.5 o superior.
2. Paquete de Python [Telepot](http://telepot.readthedocs.io/en/latest/#)
3. Paquete de Python [Selenium](selenium-python.readthedocs.io/installation.html)

**Procedimiento:**

 - Crear un Bot de Telegram mediante BotFather. Se explica cómo hacer esto [aquí](https://core.telegram.org/bots#6-botfather).
 - Descargar el ejecutable de PhantomJS, puede hacerlo desde [aquí](http://phantomjs.org/download.html).
 - Descargar el código de este repositorio y colocarlo en una carpeta
 - Abrir el fichero config.ini y configurarlo de la siguiente manera:

   ```
   [DEFAULT]
   phantomjs_path=Ruta/hasta/ejecutable/phantomjs.exe

   [IITC]
   mail = email de la cuenta de IITC a usar para las capturas
   pass = contraseña de dicha cuenta
   iitc_plugins = ["URL_Plugin_1", "URL_Plugin_2"] #No incluir la URL del plugin de IITC
   plugins_config = [{"key": "iitc-base-map", "value": "Google Roads"}] #Claves y valores de las configuraciones de los plugins añadidos

   [SCREEN] #Si modificas estos valores sin saber lo que haces puede que las capturas no salgan nítidas
   width=1200
   height=934
   ```

 Un archivo config.ini de ejemplo se da a continuación:

    [DEFAULT]
    phantomjs_path=C:\fakepath\phantomjs.exe

    [IITC]
    mail = iitc.mail
    pass = password
    iitc_plugins = ["https://static.iitc.me/build/release/plugins/privacy-view.user.js"]
    plugins_config = [{"key": "iitc-base-map", "value": "Google Roads"}]

    [SCREEN]
    width=1200
    height=934

Se puede encontrar una guía de cómo usar el parámetro **plugins_config** en [TO-DO](TODO).

 - Abrir el archivo files/security.json y configurarlo de la siguiente manera:
```json
{
    "token": "El token del bot creado",
    "token_test": "El token de un bot de prueba (no se usa)"
}
```
- Ejecutar el archivo ```main.py```

Una vez realizado esto el bot debería estar funcionando y operativo para pedirle capturas.

