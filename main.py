from VideoEditor import VideoEditor
from WebPageScreenshotter import WebPageScreenshotter

if __name__ == "__main__":
    # Usando a classe WebPageScreenshotter
    urls = [
        'https://www.noticiasagricolas.com.br/cotacoes/arroz',
        'https://www.noticiasagricolas.com.br/cotacoes/soja',
        'https://www.noticiasagricolas.com.br/cotacoes/boi-gordo',
        'https://www.noticiasagricolas.com.br/cotacoes/trigo',
        'https://www.noticiasagricolas.com.br/cotacoes/algodao',
        'https://www.noticiasagricolas.com.br/cotacoes/leite',
        'https://www.noticiasagricolas.com.br/cotacoes/amendoim',
        'https://www.noticiasagricolas.com.br/cotacoes/feijao',
        'https://www.noticiasagricolas.com.br/cotacoes/cafe',
        'https://www.noticiasagricolas.com.br/cotacoes/cacau',
        'https://www.noticiasagricolas.com.br/cotacoes/suinos',
        'https://www.noticiasagricolas.com.br/cotacoes/frango',
        'https://www.noticiasagricolas.com.br/cotacoes/frutas',
        'https://www.noticiasagricolas.com.br/cotacoes/laranja',
        'https://www.noticiasagricolas.com.br/cotacoes/latex',
        'https://www.noticiasagricolas.com.br/cotacoes/legumes',
        'https://www.noticiasagricolas.com.br/cotacoes/mandioca',
        'https://www.noticiasagricolas.com.br/cotacoes/mercado-financeiro',
        'https://www.noticiasagricolas.com.br/cotacoes/milho',
        'https://www.noticiasagricolas.com.br/cotacoes/ovos',
        'https://www.noticiasagricolas.com.br/cotacoes/silvicultura',
        'https://www.noticiasagricolas.com.br/cotacoes/sorgo',
        'https://www.noticiasagricolas.com.br/cotacoes/sucroenergetico',
        'https://www.noticiasagricolas.com.br/cotacoes/verduras'
    ]
    for url in urls:
        screenshotter = WebPageScreenshotter(url)
        screenshotter.setup_driver()
        screenshotter.capture_screenshots("cotacao")

    # Usando a classe VideoEditor
    editor = VideoEditor()
    editor.edit_video()
    editor.render_video()
