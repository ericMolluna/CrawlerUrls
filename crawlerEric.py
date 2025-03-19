import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

# Configuració del WebDriver per Firefox
options = Options()
options.headless = True  # Mode sense capçalera per rendiment

# Inicialitzar el driver
try:
    driver = webdriver.Firefox(options=options)
except Exception as e:
    print(f"Error iniciant WebDriver: {e}")
    exit()

visited_urls = set()
error_urls = []
max_urls = 50  # Limitar el nombre de pàgines a explorar

def get_links(url):
    """Obté tots els enllaços d'una pàgina donada."""
    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        time.sleep(1)  # Petita pausa per garantir que el contingut es carregui completament
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:  
                links.add(full_url)
        return links
    except Exception as e:
        print(f"Error obtenint enllaços de {url}: {e}")
        return set()

def check_url(url, referer):
    """Comprova l'estat HTTP d'una URL i registra errors 4XX."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=3)
        time.sleep(1.5)  
        if 400 <= response.status_code < 500:
            print(f"Error {response.status_code}: {url}")
            error_urls.append([url, response.status_code, referer])
    except requests.RequestException as e:
        print(f"Error accedint a {url}: {e}")
        error_urls.append([url, 'Timeout/Error', referer])

def crawl(url, depth=2):
    """Explora un lloc web recursivament fins a una profunditat definida."""
    if len(visited_urls) >= max_urls or depth == 0 or url in visited_urls:
        return
    
    print(f"Explorant: {url}")
    visited_urls.add(url)
    time.sleep(1)  
    links = get_links(url)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for link in links:
            if len(visited_urls) >= max_urls:
                return
            executor.submit(check_url, link, url)
            crawl(link, depth - 1)  # Recursió

def save_report():
    """Guarda les URLs amb error en un fitxer CSV."""
    with open('errors_4xx_report.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Codi d'error", "Referència"])
        writer.writerows(error_urls)
    print("✅ Informe generat: errors_4xx_report.csv")

if __name__ == "__main__":
    start_url = "https://bookpricetracker.risusapp.com/" 
    crawl(start_url)
    save_report()
    driver.quit()