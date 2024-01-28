from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import random, os, configparser, time, datetime
from os import listdir
from os.path import isfile, join

config = configparser.ConfigParser()
config.read('config.ini')
outputDir = config["General"]["OutputDirectory"]

startTime = time.time()

image_clip_duration = 5

# Caminho para a pasta 'imagens'
imagens_dir = 'imagens'

# Lista para armazenar os nomes dos arquivos screenShotFile
screen_shot_files = []

# Verifique se o diretório 'imagens' existe
if os.path.exists(imagens_dir) and os.path.isdir(imagens_dir):
    # Liste todos os arquivos na pasta 'imagens'
    for filename in os.listdir(imagens_dir):
        # Verifique se o arquivo tem uma extensão de imagem (por exemplo, .jpg, .jpeg, .png)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Adicione o nome do arquivo à lista de screenShotFiles
            screen_shot_files.append(os.path.join(imagens_dir, filename))


# Setup background clip
bgDir = config["General"]["BackgroundDirectory"]
bgPrefix = config["General"]["BackgroundFilePrefix"]
bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))]
bgCount = len(bgFiles)
bgIndex = random.randint(0, bgCount-1)
backgroundVideo = VideoFileClip(
    filename=f"{bgDir}/{bgPrefix}{bgIndex}.mp4", 
    audio=False).subclip(0, len(screen_shot_files) * image_clip_duration)
w, h = backgroundVideo.size

def create_clip(screen_shot_file, margin_size, image_duration):
    image_clip = ImageClip(
        screen_shot_file,
        duration=image_duration
    ).set_position(("center", "center"))
    image_clip = image_clip.resize(width=(w - margin_size))
    image_clip.fps = 1
    return image_clip


# Create video clips
print("Editing clips together...")
clips = []
margin_size = int(config["Video"]["MarginSize"])
for screenshot in screen_shot_files:
    clips.append(create_clip(screenshot, margin_size, image_clip_duration))

# Merge clips into a single track
content_overlay = concatenate_videoclips(clips).set_position(("center", "center"))

# Compose background/foreground
final = CompositeVideoClip(
    clips=[backgroundVideo, content_overlay], 
    size=backgroundVideo.size)
    
    # .set_audio(content_overlay.audio)
# final.duration = 45  # Definindo a duração final como 45 segundos
final.fps = backgroundVideo.fps


# Escreva a saída em um arquivo
print("Rendering final video...")
bitrate = config["Video"]["Bitrate"]
threads = config["Video"]["Threads"]
output_file = f"{outputDir}/{datetime.datetime.now()}.mp4"
final.write_videofile(
    output_file, 
    codec='libx264',
    threads=threads, 
    bitrate=bitrate
)
print(f"Video completed in {time.time() - startTime}")
