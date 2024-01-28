from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = "https://www.noticiasagricolas.com.br/cotacoes/mercado-fisico-safras-e-mercado"
driver.get(url)

try:
    # Remover elementos com a classe 'ver-outras'
    driver.execute_script("""
    var elements = document.querySelectorAll('.ver-outras');
    elements.forEach(function(el) {
        el.parentNode.removeChild(el);
    });
    """)

    # Encontrar todos os elementos com a classe 'box-cotacoes'
    box_cotacoes_elements = driver.find_elements(By.CLASS_NAME, "box-cotacoes")
    
    # Verificar se elementos foram encontrados
    if box_cotacoes_elements:
        print(f"Encontrados {len(box_cotacoes_elements)} elementos com a classe 'box-cotacoes'.")

        # Tirar um print de cada elemento encontrado
        for i, box_cotacao in enumerate(box_cotacoes_elements, start=1):
            filename = f"box_cotacao_{i}.png"
            box_cotacao.screenshot(filename)
            print(f"Screenshot salvo: {filename}")
    else:
        print("Nenhum elemento com a classe 'box-cotacoes' foi encontrado.")
        
finally:
    driver.quit()
