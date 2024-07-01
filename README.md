## Depto Bot 🌇
Vivís en Argentina y andás buscando depto? Cansado/a de pasartela haciendo F5 en Zonaprop y que te primereen los departamentos igual? Acá tenés la solución ;)

### Qué hace?
Entra a la página de ZonaProp cada cierta cantidad de tiempo *(por default cada 30-55 minutos)* y te manda una noticación de Windows por cada propiedad nueva que aparece. 

Va guardando los IDs de las propiedades ya notificadas en un `deptos.json`.

### Cómo usar
* Cloná el repositorio
* Andá a Chrome y encontrá la versión (entrá a `chrome://settings/help`, ahí aparece)
* Descargá el ChromeDriver correspondiente a tu versión de Chrome [acá](https://sites.google.com/chromium.org/driver/downloads)
* Descomprimí la carpeta que descargaste y dejá el archivo `chromedriver.exe` en la carpeta del repo 
* Instalá Selenium (`pip install selenium`)
* Corré el script `python script.py`


## TODO
* Sacar imagen cada objeto y usarla para las notis

### EXTRAS
* Customizar la query con argumentos que se pasan al programa
* Permitir sacar los dicts con opciones para las queries afuera del main script
* Conectar con bot Telegram
* Tutorial de queries y opciones disponibles 