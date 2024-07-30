import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class WebPageScreenshotter:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def setup_driver(self):
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def capture_screenshots(self, element_class):
        try:
            self.driver.get(self.url)
            
            parsed_url = urlparse(self.url)
            path_segments = parsed_url.path.split("/")
            # Pegue a última parte do caminho
            last_path_segment = path_segments[-1]

            # Remover elementos com a classe 'mostrar-historico'
            self.driver.execute_script("""
            var elements = document.querySelectorAll('.mostrar-historico');
            elements.forEach(function(el) {
                el.parentNode.removeChild(el);
            });
            """)

            # Remover elementos com a classe 'mostrar-historico'
            self.driver.execute_script("""
            var elementosDeTexto = document.querySelectorAll("tr, td");
            elementosDeTexto.forEach(function(elemento) {
                elemento.style.fontWeight = "bold";
            });
            """)

            # Encontrar todos os elementos com a classe fornecida
            elements = self.driver.find_elements(By.CLASS_NAME, element_class)

            # Verificar se elementos foram encontrados
            if elements:
                print(f"Encontrados {len(elements)} elementos com a classe '{element_class}'.")

                # Tirar um print de cada elemento encontrado
                for i, element in enumerate(elements, start=1):
                    filename = f"imagens/{last_path_segment}_{element_class}_{i}.png"
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
                    time.sleep(1)
                    element.screenshot(filename)
                    print(f"Screenshot salvo: {filename}")
            else:
                print(f"Nenhum elemento com a classe '{element_class}' foi encontrado.")
        
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    url = "https://www.noticiasagricolas.com.br/cotacoes/mercado-fisico-safras-e-mercado"
    screenshotter = WebPageScreenshotter(url)
    screenshotter.setup_driver()
    screenshotter.capture_screenshots("box-cotacoes")
