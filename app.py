from flask import Flask, render_template, Response
import cv2
from gevent.pywsgi import WSGIServer
import webbrowser
from threading import Timer

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Ler o frame da câmera
        success, frame = camera.read()
        if not success:
            break
        else:
            # Codificar o frame como JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        # Enviar o frame como resposta
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    # return render_template('main.html')
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    http_server = WSGIServer(("127.0.0.1", 8080), app)
    http_server.start()
    
    # Abrir a página web automaticamente
    webbrowser.open('http://127.0.0.1:8080')

    http_server.serve_forever()
    app.run(debug=True)
  
