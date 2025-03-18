from flask import Flask, render_template, jsonify, request, url_for
import cv2
import mediapipe as mp
import numpy as np
import pickle
import base64
import random
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Cargar modelos
model_dict = pickle.load(open('./model/model.p', 'rb'))  
model = model_dict['model']

models_dict = pickle.load(open('./model/models.p', 'rb'))
models = models_dict['model']

# Diccionarios de etiquetas
labels_dict = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j',10:'k',11:'l',12:'ll',13:'m',14:'n',15:'ñ',16:'o',17:'p',18:'q',19:'r',20:'rr',21:'s',22:'t',23:'u',24:'v',25:'w',26:'x',27:'y',28:'z'}
labels_dicts = { 0: 'Hola', 1: 'Buenos dias', 2: 'Buenas tardes', 3: 'Buenas noches', 4: '¿Como estas?',}

# Configuración de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Listas de imágenes y videos
sign_images = ['a.jpeg','b.jpeg','c.jpeg','d.jpeg','e.jpeg','f.jpeg','g.jpeg','h.jpeg','i.jpeg','j.jpeg','k.jpeg','l.jpeg','ll.jpeg','m.jpeg','n.jpeg','ñ.jpeg','o.jpeg','p.jpeg','q.jpeg','r.jpeg','rr.jpeg','s.jpeg','t.jpeg','u.jpeg','v.jpeg','w.jpeg','x.jpeg','y.jpeg','z.jpeg']
sign_videos = ['hola.mp4', 'buenos_dias.mp4', 'buenas_tardes.mp4', 'buenas_noches.mp4', 'comoestas.mp4']


# Obtener índices válidos
valid_indices = list(range(len(sign_images)))
valids_indices = list(range(len(sign_videos)))

def new_random_image():
    random_index = random.choice(valid_indices)
    return sign_images[random_index], labels_dict[random_index]

# Variables globales de estado
current_image, current_target = new_random_image()

current_video_index = 0

@app.route('/gestos')
def gestos():
    return render_template('deteccion.html')

@app.route('/gestos/saludos')
def gestos_saludos():
    return render_template('deteccionsaludos.html')

# Inicializamos current_target en None para evitar valores residuales
current_image, current_target = None, None
current_video, current_target = None, None

@app.route('/gestos/get_current_image')
def get_current_image():
    global current_image, current_target
    current_image, current_target = new_random_image()  # Siempre obtiene una nueva imagen
    try:
        image_url = url_for('static', filename=f'sign_images/alphabet/{current_image}', _external=True)
        return jsonify({'image_url': image_url, 'target': current_target, 'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def new_ordered_video():
    global current_video_index
    if current_video_index < len(sign_videos):
        video = sign_videos[current_video_index]
        target = labels_dicts[current_video_index]
        current_video_index += 1
        return video, target
    else:
        # Reiniciar el índice si se llega al final
        current_video_index = 0
        return sign_videos[current_video_index], labels_dicts[current_video_index]
    
@app.route('/gestos/saludos/get_current_video')
def get_current_video():
    global current_video, current_target
    current_video, current_target = new_ordered_video()  # Obtener el siguiente video en orden
    try:
        video_url = url_for('static', filename=f'videos/greetings/{current_video}', _external=True)
        return jsonify({'video_url': video_url, 'target': current_target, 'status': 'success', 'is_last': current_video_index >= len(sign_videos)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/gestos/skip', methods=['POST'])
def skip_image():
    global current_image, current_target
    current_image, current_target = new_random_image()
    return jsonify({'status': 'success', 'image_url': url_for('static', filename=f'sign_images/alphabet/{current_image}', _external=True), 'target': current_target})

@app.route('/gestos/saludos/skip', methods=['POST'])
def skip_video():
    global current_video, current_target
    current_video, current_target = new_ordered_video()  # Obtener el siguiente video en orden
    return jsonify({'status': 'success', 'video_url': url_for('static', filename=f'videos/greetings/{current_video}', _external=True), 'target': current_target})

@app.route('/gestos/predict', methods=['POST'])
def predict():
    return process_prediction(model, labels_dict)

@app.route('/gestos/saludos/predict', methods=['POST'])
def predict_saludos():
    return process_prediction(models, labels_dicts)  # Usar el modelo de videos

def process_prediction(model_used, labels):
    data = request.get_json()
    frame_base64 = data.get('frame')

    if not frame_base64:
        return jsonify({'prediction': 'No se recibió ningún frame'})
    try:
        frame_bytes = base64.b64decode(frame_base64)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            data_aux = []
            x_, y_ = [], []

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x, y = hand_landmarks.landmark[i].x, hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)
                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))
                if len(data_aux) > 42:
                    data_aux = data_aux[:42]
            
            prediction = model_used.predict([data_aux])
            predicted_index = int(prediction[0])
            predicted_character = labels.get(predicted_index, "Desconocido")
            is_correct = predicted_character.strip().lower() == current_target.strip().lower()

            return jsonify({'prediction': predicted_character, 'is_correct': is_correct, 'target': current_target})
        return jsonify({'prediction': 'No se detectó ninguna mano'})
    except Exception as e:
        return jsonify({'prediction': f'Error: {str(e)}'})


if __name__ == '__main__':
    app.run(port=5000)