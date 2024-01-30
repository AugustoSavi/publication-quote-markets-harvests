from moviepy.editor import VideoFileClip

# Carregue o vídeo original
video_path = 'background.mp4'
video_clip = VideoFileClip(video_path)

# Redimensione o vídeo para a resolução desejada
video_clip = video_clip.rotate(90)

# Duração desejada para cada segmento (2 minutos = 120 segundos)
segment_duration = 120

# Inicialize o contador de segmentos
segment_counter = 1

# Defina o ponto de início inicial
start_time = 0

# Configure a taxa de bits para controlar a qualidade do vídeo (ajuste conforme necessário)
bitrate = "8000k"  # Exemplo de taxa de bits alta

# Enquanto houver tempo restante no vídeo
while start_time < video_clip.duration:
    # Defina o ponto de término do segmento
    end_time = min(start_time + segment_duration, video_clip.duration)
    
    # Corte o segmento
    segment_clip = video_clip.subclip(start_time, end_time)
    
    # Salve o segmento com a taxa de bits configurada
    output_path = f'segment_{segment_counter}.mp4'
    segment_clip.write_videofile(output_path, codec='libx264', bitrate=bitrate, threads=4)
    
    print(f"Segmento {segment_counter} criado com sucesso em:", output_path)
    
    # Atualize o ponto de início para o próximo segmento
    start_time = end_time
    segment_counter += 1
