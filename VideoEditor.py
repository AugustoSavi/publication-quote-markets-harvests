import numpy as np
from os import listdir
from os.path import isfile, join
from PIL import ImageFont, ImageDraw, Image
from pilmoji import Pilmoji
from pydub import AudioSegment
import random, os, configparser, time, datetime
from moviepy.audio.fx import audio_fadein, audio_fadeout
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, ImageClip, ColorClip, TextClip

class VideoEditor:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.outputDir = self.config["General"]["OutputDirectory"]
        self.image_clip_duration = 5
        self.startTime = time.time()
        self.imagens_dir = 'imagens'
        self.screen_shot_files = []
        self.bgDir = self.config["General"]["BackgroundDirectory"]
        self.bgPrefix = self.config["General"]["BackgroundFilePrefix"]
        self.bgFiles = [f for f in listdir(self.bgDir) if isfile(join(self.bgDir, f))]
        self.bgCount = len(self.bgFiles)
        self.bgIndex = random.randint(1, self.bgCount-1)
        self.backgroundVideo = VideoFileClip(
            filename=f"{self.bgDir}/{self.bgPrefix}{self.bgIndex}.mp4", 
            audio=False).subclip(0, len(self.screen_shot_files) * self.image_clip_duration)
        self.w, self.h = self.backgroundVideo.size
        self.margin_size = int(self.config["Video"]["MarginSize"])
        self.final = None

    def load_screen_shot_files(self):
        if os.path.exists(self.imagens_dir) and os.path.isdir(self.imagens_dir):
            for filename in os.listdir(self.imagens_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.screen_shot_files.append(os.path.join(self.imagens_dir, filename))

    def create_clip(self, screen_shot_file):
        image_clip = ImageClip(
            screen_shot_file,
            duration=self.image_clip_duration
        ).set_position(("center", "center"))
        image_clip = image_clip.resize(width=(self.w - self.margin_size))
        image_clip.fps = 1
        return image_clip

    def edit_video(self):
        self.load_screen_shot_files()
        clip_duration = len(self.screen_shot_files) * self.image_clip_duration
        clips = []

        for screenshot in self.screen_shot_files:
            clips.append(self.create_clip(screenshot))

        content_overlay = concatenate_videoclips(clips).set_position(("center", "center"))

        videoClipToComposite = VideoFileClip(
            filename=f"{self.bgDir}/{self.bgPrefix}{self.bgIndex}.mp4", 
            audio=False).subclip(0, clip_duration)

        # ------------------- incio adição dos textos e emojis -------------------
        data_atual = datetime.date.today()
        self.data_formatada = data_atual.strftime("%d/%m/%Y")

        # Crie um clip de texto. Ajuste o fontsize conforme necessário.
        txt_clip = TextClip(f"Cotação {self.data_formatada}", fontsize=36, color='black', stroke_color='black', stroke_width=3)

        # Determine o tamanho do vídeo
        largura_video, altura_video = self.backgroundVideo.size

        # Determine o tamanho do texto
        largura_texto, altura_texto = txt_clip.size

        # Calcule as coordenadas para o posicionamento
        x_text = (largura_video - largura_texto) / 2
        y_text = (altura_video - altura_texto) / 2 - (altura_video * 0.30)

        # Calcule as coordenadas para o posicionamento
        x_emoji = (largura_video - largura_texto) / 2 + (largura_video * 0.07)
        y_emoji = (altura_video - altura_texto) / 2 - (altura_video * 0.27)

        # Defina a duração do clipe de texto e a posição, se necessário.
        txt_clip = txt_clip.set_duration(clip_duration).set_position((x_text, y_text))

        # Crie um ColorClip branco para o fundo
        fundo_branco_text = ColorClip(size=(largura_texto + 10, altura_texto + 10), color=(255, 255, 255)).set_duration(clip_duration).set_position((x_text - 5, y_text - 7))

        # Crie um ColorClip branco para o fundo
        fundo_branco_emoji = ColorClip(size=(310, altura_texto + 40), color=(255, 255, 255)).set_duration(clip_duration).set_position((x_text + 40, y_text + 24))

        emoji_clip = ImageClip(self.make_emoji_image("🌾🐔🐖🐃🌽🫛", "./utils/Noto_Color_Emoji/NotoColorEmoji-Regular.ttf", 48)).set_duration(clip_duration).set_start(0).set_position((x_emoji, y_emoji))

        # -------------------------------------------------------------------------

        self.final = CompositeVideoClip(
            clips=[videoClipToComposite, content_overlay, fundo_branco_text, fundo_branco_emoji, txt_clip , emoji_clip], 
            size=self.backgroundVideo.size)
        self.final.fps = self.backgroundVideo.fps


    def make_emoji_image(self, emoji, font_path, font_size):
        emoji_font = ImageFont.truetype(font_path, font_size)
        text_size = emoji_font.getsize(emoji.strip())
        image = Image.new("RGBA", text_size, (0, 0, 0, 0))
        with Pilmoji(image) as pilmoji:
            pilmoji.text((0, 0), emoji.strip(), (0, 0, 0), emoji_font)
        return np.array(image)


    def render_video(self):
        output_file = f"{self.outputDir}/{datetime.datetime.now()}.mp4"
        bitrate = self.config["Video"]["Bitrate"]
        threads = self.config["Video"]["Threads"]
        self.final.write_videofile(
            output_file, 
            codec='libx264',
            threads=threads, 
            bitrate=bitrate
        )
        print(f"Video completed in {time.time() - self.startTime}")
        print(f"Cotação {self.data_formatada} 🌾🐔🐖🐃🌽🫛 #Agricultura #MercadoAgrícola #Cotações #AgriculturaSustentável #PreçosAgrícolas #Agronegócio #Cultivos #Agropecuária #ProduçãoAgrícola #TendênciasAgrícolas")

if __name__ == "__main__":
    
    editor = VideoEditor()
    editor.edit_video()
    editor.render_video()
