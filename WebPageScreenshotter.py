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

            # Remover elementos com a classe 'ver-outras'
            self.driver.execute_script("""
            var elements = document.querySelectorAll('.ver-outras');
            elements.forEach(function(el) {
                el.parentNode.removeChild(el);
            });
            """)

            # Encontrar todos os elementos com a classe fornecida
            elements = self.driver.find_elements(By.CLASS_NAME, element_class)

            # Verificar se elementos foram encontrados
            if elements:
                print(f"Encontrados {len(elements)} elementos com a classe '{element_class}'.")

                # Tirar um print de cada elemento encontrado
                for i, element in enumerate(elements, start=1):
                    filename = f"imagens/{element_class}_{i}.png"
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
