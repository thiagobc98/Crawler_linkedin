import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import dotenv
import re
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup 

import requests


dotenv.load_dotenv()

PATH_DOWNLOAD_CHROME = os.getenv("PATH_DOWNLOAD_CHROME")

Linkedin_user = os.getenv("linkedin_user")
Linkedin_senha = os.getenv("linkedin_senha")


def create_chrome_driver() -> webdriver:
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option('prefs', {
        'download.default_directory': PATH_DOWNLOAD_CHROME,
        'download.prompt_for_download': False,  # Evita que o Chrome pergunte onde salvar os downloads
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True  # Ativa a verificação de segurança para downloads
    })
    chromeOptions.add_argument("--disable-save-password-bubble")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chromeOptions)
    return driver

def quit_chrome(driver: webdriver)->None:
    print('Fechando Navegador...')
    driver.close()
    driver.quit()

def insert_key(driver: webdriver, xpath: str, key: str) -> None: 
    driver.find_element(By.XPATH, xpath).send_keys(key)
    sleep(1)

def click(driver: webdriver, xpath: str) -> None: 
    driver.find_element(By.XPATH, xpath).click()
    sleep(1)



def fazendo_login(driver: webdriver):
    print("Abrindo navegador...")
    driver.get("https://www.linkedin.com/")

    print("Fazendo login...")
    click(driver, '//*[@id="main-content"]/section[1]/div/div/a')
    sleep(2)
    insert_key(driver, '//*[@id="username"]', Linkedin_user)
    sleep(2)
    insert_key(driver, '//*[@id="password"]', Linkedin_senha)
    sleep(2)
    click(driver, '//*[@id="organic-div"]/form/div[4]/button')
    sleep(4)
    


links_user = []
links_user.append('https://www.linkedin.com/in/thiago-berberich/')
links_user.append('https://www.linkedin.com/in/p-ricardo-lima/')
links_user.append('https://www.linkedin.com/in/antonioemj/')
links_user.append('https://www.linkedin.com/in/daniel-carlos-viana/')
links_user.append('https://www.linkedin.com/in/jonathan-bryan-ca/')
links_user.append('https://www.linkedin.com/in/estevao-boaventura/')



def extracao_dados(driver: webdriver, links_user):
    fazendo_login(driver)  # Certifique-se de que está autenticado
    
    dados_user = []

    for link in links_user:
        try:
            sleep(5)
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(link)

            sleep(3)  # Espera um pouco para garantir que a página carregue

            nome_elemento = driver.find_element(By.TAG_NAME, "h1")  # Captura o primeiro <h1>
            nome = nome_elemento.text.strip()
            print('Nome:', nome)

            info_elemento = driver.find_element(By.CLASS_NAME, "text-body-medium.break-words")
            informacoes = info_elemento.text.strip()
            print('Informações:', informacoes)


            sobre_elemento = driver.find_element(By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[3]/div[3]/div/div/div')
            sobre_texto = sobre_elemento.text.strip()
            print('Sobre:', sobre_texto)

            

            dados = {
                'nome': nome,
                'link_usuario': link,
                'informacoes': informacoes,
                'sobre': sobre_texto
                    }
            
            dados_user.append(dados)

        except Exception as e:
            print(f"Erro ao extrair dados do link {link}: {e}")

        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    df_usuarios = pd.DataFrame(dados_user)
    
    return df_usuarios  


print('Inicializando o Selenium')
driver = create_chrome_driver()
df_usuarios = extracao_dados(driver, links_user)

df_usuarios.to_csv('dados_usuarios.csv')