# Servidor-descarga-YT-a-mp4-en-local
Proyecto que permite ejecutar en una red local un servidor que descarga videos de Youtube en mp4. Este servidor simplemente te permite pegar la dirección URL de un vídeo de Youtube, te muestra una barrita con el progreso de la descarga, al terminar descarga el vídeo y además tiene un historial de descargas. 

#Requisitos
Python 3
pip
FFmpeg
Un navegador web 
Sistema Operativo (Cualquier distribución de Linux, yo he usado Kali)

#Pasos:
1. Descargar el código del servidor.py
2. Crear un entrono virtual (ej: python3 -m venv venv; source venv/bin/activate)
3. Instala lo Flask y ffmpeg (pip install Flask yt-dlp; sudo apt install ffmpeg -y)
4. Crea una carpeta para las descargas (La ruta que está en el servidor.py es ~/Desktop/descargas_youtube)
5. Ejecuta el servidor (python3 servidor.py)
6. Usar con http://localhost:5000 o desde otro dispositivo que esté en la misma red local pegando en el navegador el url que te de el servidor python

IMPORTANTE: En caso de usar máquina virtual, asegurate que tienes la configuración de red en modo puente (briedged adapter)

#Resultado: 
![image](https://github.com/user-attachments/assets/792b05a5-ce1e-4d2a-9a36-82233fb4aa5b)

