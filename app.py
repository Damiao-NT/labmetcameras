import cv2
import os
from flask import Flask, render_template, Response

app = Flask(__name__)

cameras = [
    {
        'username': 'admin',
        'password': 'portariaM1',
        'ip': '150.165.37.23',
        'port': '554',
        'url': 'rtsp://admin:portariaM1@150.165.37.23:554/onvif1'
    },
    {
        'username': 'admin_password',
        'password': 'tlJwpbo6_channel=1_stream=0.sdp?real_stream',
        'ip': '150.165.37.14',
        'port': '554',
        'url': 'rtsp://150.165.37.14:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
    }
]

# Define o tamanho desejado para o vídeo
VIDEO_WIDTH = 440
VIDEO_HEIGHT = 280

# Só roda se for ffmpeg
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

def generate_frames(camera):
    url = camera['url']
    print('Conectando com: ' + url)
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

    # Configura o tamanho do vídeo capturado
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:

            # Redimensiona o frame para o tamanho desejado
            frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))

            # Codifica o frame com as faces detectadas como JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_with_faces = buffer.tobytes()

            # Envia o frame com as faces detectadas como resposta
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_with_faces + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed/<int:camera_id>')
def video_feed(camera_id):
    if camera_id < 0 or camera_id >= len(cameras):
        return 'Invalid camera ID'
    return Response(generate_frames(cameras[camera_id]), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
