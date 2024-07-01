import json
from enum import Enum
from time import sleep
from selenium import webdriver

JSON_PATH = "deptos.json"

class Barrios(Enum):
    CENTRO = "centro-cordoba"
    NUEVA_CORDOBA = "nueva-cordoba"
    GUEMES = "guemes-cordoba"

class TipoAlquiler(Enum):
    NORMAL = "alquiler"
    TEMPORAL = "alquiler-temporal"

class Moneda(Enum):
    ARS = "pesos"
    USD = "dolar"

class Orden(Enum):
    RECIENTES = "orden-publicado-descendente"

class Depto:
    def __init__(self, titulo, precio, barrio):
        self.titulo = titulo
        self.precio = precio
        self.barrio = barrio

class ZonapropScraper:
    base_url = "https://www.zonaprop.com.ar/departamentos"
    end_url = ".html"
    delim = "-"

    deptos = {
        '1': Depto("Hermoso depto en Nueva!", 350000, "Nueva")
    }

    def __init__(self):
        self.driver = webdriver.Chrome()

    def build_url(self, tipo_alquiler, barrios, min_precio, moneda, orden):
        url = self.base_url
        url += self.delim + tipo_alquiler.value
        for barrio in barrios:
            url += self.delim + barrio.value
        url += self.delim + "mas" + self.delim + str(min_precio) + self.delim + moneda.value
        url += self.delim + orden.value
        url += self.end_url

        return url

    def get_last_published(self, tipo_alquiler, barrios, min_precio, moneda, orden, n):
        url = self.build_url(tipo_alquiler, barrios, min_precio, moneda, orden)
        self.driver.get(url)
        sleep(5)

    def load_deptos(self):
        with open(JSON_PATH, 'r') as file:
            self.deptos = json.load(file)

    def save_to_json(self):
        with open(JSON_PATH, "w") as outfile:
            json.dump(self.deptos, outfile)

def main():
    zonaprop = ZonapropScraper()

    # test 
    zonaprop.get_last_published(TipoAlquiler.TEMPORAL, [Barrios.CENTRO, Barrios.NUEVA_CORDOBA], 300000, Moneda.ARS, Orden.RECIENTES, 5)


if __name__ == "__main__":
    main()