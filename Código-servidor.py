from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Carpeta de descargas en el escritorio
DOWNLOAD_FOLDER = os.path.expanduser("~/Desktop/descargas_youtube")
progreso_global = {"progreso": 0, "estado": "esperando"}
historial = []

@app.route('/')
def home():
    historial_html = "<ul>" + "".join([
        f"<li>{item['nombre_archivo']} - {item['fecha']}</li>" for item in historial
    ]) + "</ul>"
    
    return f'''
    <h2>Descargar vídeo de YouTube</h2>
    <form action="/descargar" method="post">
        <input name="url" type="text" placeholder="URL de YouTube" required>
        <button type="submit">Descargar</button>
    </form>
    <br>
    <progress id="barra" value="0" max="100"></progress>
    <p id="estado"></p>
    
    <h3>Historial de descargas</h3>
    {historial_html}
    
    <script>
        setInterval(() => {{
            fetch('/progreso')
                .then(res => res.json())
                .then(data => {{
                    document.getElementById("barra").value = data.progreso;
                    document.getElementById("estado").innerText = data.estado;
                }});
        }}, 1000);
    </script>
    '''

@app.route('/progreso')
def progreso():
    return jsonify(progreso_global)

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "No se proporcionó una URL"}), 400

    nombre_archivo = f"{uuid.uuid4()}.mp4"
    ruta_archivo = os.path.join(DOWNLOAD_FOLDER, nombre_archivo)

    def hook(d):
        if d['status'] == 'downloading':
            porcentaje = d.get('_percent_str', '0.0%').replace('%', '').strip()
            progreso_global["estado"] = "Descargando..."
            try:
                progreso_global["progreso"] = float(porcentaje)
            except:
                progreso_global["progreso"] = 0
        elif d['status'] == 'finished':
            progreso_global["estado"] = "Procesando..."
            progreso_global["progreso"] = 100

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': ruta_archivo,
        'merge_output_format': 'mp4',
        # Esta opción fuerza a FFmpeg a recodificar el vídeo a MP4 (lo que sí hace recodificación solo de vídeo)
        'recodevideo': 'mp4',
        # Con postprocessor_args forzamos a FFmpeg a recodificar el audio a AAC
        'postprocessor_args': ['-c:a', 'aac'],
        'progress_hooks': [hook],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        progreso_global["estado"] = "Error"
        progreso_global["progreso"] = 0
        return jsonify({"error": str(e)}), 500

    progreso_global["estado"] = "Completado"

    # Añadimos la descarga al historial
    historial.append({
        "nombre_archivo": nombre_archivo,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    response = send_file(ruta_archivo, as_attachment=True)

    @response.call_on_close
    def limpiar():
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        progreso_global["estado"] = "esperando"
        progreso_global["progreso"] = 0

    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
