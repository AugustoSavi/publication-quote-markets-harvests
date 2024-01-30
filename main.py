from VideoEditor import VideoEditor
from WebPageScreenshotter import WebPageScreenshotter

if __name__ == "__main__":
    # Usando a classe WebPageScreenshotter
    url = "https://www.noticiasagricolas.com.br/cotacoes/mercado-fisico-safras-e-mercado"
    screenshotter = WebPageScreenshotter(url)
    screenshotter.setup_driver()
    screenshotter.capture_screenshots("box-cotacoes")

    # Usando a classe VideoEditor
    editor = VideoEditor()
    editor.edit_video()
    editor.render_video()
