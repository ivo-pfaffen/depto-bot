import json
import os
from enum import Enum
from time import sleep
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from win11toast import toast
import re
import random
import datetime

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

class DeptoNotification:
    def display_depto(self, app_name, location, price, src, url):
        print("Got a new apartment, and the url is " + url)
        toast(f"Nuevo en {src}",
            f"Hay un nuevo depto en {location}! Sale ${price} por mes.",
            on_click=url)

class ZonapropScraper:
    base_base_url = "https://www.zonaprop.com.ar"
    base_url = "https://www.zonaprop.com.ar/departamentos"
    end_url = ".html"
    delim = "-"

    deptos = []

    def __init__(self):
        options = ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.minimize_window()
        self.notifications = DeptoNotification()
        self.load_deptos()
        

    def build_url(self, tipo_alquiler, barrios, min_precio, moneda, orden):
        url = self.base_url
        url += self.delim + tipo_alquiler.value
        for barrio in barrios:
            url += self.delim + barrio.value
        url += self.delim + "mas" + self.delim + str(min_precio) + self.delim + moneda.value
        url += self.delim + orden.value
        url += self.end_url

        return url

    def extract_price(self, raw_price):
        cleaned_str = re.sub(r'[^\d]', '', raw_price)
        if cleaned_str != "":
            return int(cleaned_str)
        return 0

    def get_last_published(self, tipo_alquiler, barrios, min_precio, moneda, orden, n):
        url = self.build_url(tipo_alquiler, barrios, min_precio, moneda, orden)
        self.driver.get(url)
        self.driver.minimize_window()
        sleep(5)
        parent = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div[3]")
        depto_listings = parent.find_elements(By.CSS_SELECTOR, '[data-qa="posting PROPERTY"]')

        new_deptos = 0
        for depto in depto_listings:
            depto_url = depto.get_attribute("data-to-posting")
            depto_id = depto.get_attribute("data-id")
            depto_precio = depto.find_element(By.CSS_SELECTOR, '[data-qa="POSTING_CARD_PRICE"]').text
            depto_expensas = depto.find_element(By.CSS_SELECTOR, '[data-qa="expensas"]').text
            depto_barrio = depto.find_element(By.CSS_SELECTOR, '[data-qa="POSTING_CARD_LOCATION"]').text
            depto_precio_final = self.extract_price(depto_precio) + self.extract_price(depto_expensas)
            #depto_img = depto.find_element(By.CLASS_NAME, 'flickity-slider')
            #print(depto_img)
            if depto_id not in self.deptos:
                self.notifications.display_depto(app_name="", location=depto_barrio, price=str(depto_precio_final), src="ZonaProp", url=self.base_base_url+depto_url)
                self.deptos.append(depto_id)
                new_deptos += 1

        print(f"Found {new_deptos} new deptos :)")
        self.save_to_json()

    def load_deptos(self):
        if not os.path.isfile(JSON_PATH) or os.stat(JSON_PATH).st_size == 0:
            return
    
        with open(JSON_PATH, 'r') as file:
            self.deptos = json.load(file)

    def save_to_json(self):
        with open(JSON_PATH, "w") as outfile:
            json.dump(self.deptos, outfile)
            

def main():
    zonaprop = ZonapropScraper()
    while True:
        zonaprop.get_last_published(TipoAlquiler.TEMPORAL, [Barrios.CENTRO, Barrios.NUEVA_CORDOBA], 300000, Moneda.ARS, Orden.RECIENTES, 5)

        random_time = random.uniform(30*60, 55*60)
        current_time = datetime.datetime.now()
        next_run_time = current_time + datetime.timedelta(seconds=random_time)
        print(f"Corrí a las {datetime.datetime.now()}")
        print(f"Vuelvo a correr en {random_time/60} minutos! O sea, a las {next_run_time} \n")
        sleep(random_time)

if __name__ == "__main__":
    main()
