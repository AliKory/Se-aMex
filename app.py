from flask import Flask, render_template, jsonify, request, url_for
import cv2
import mediapipe as mp
import numpy as np
import pickle
import base64
import random
import os
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Cargar el modelo
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
labels_dict = {
    0: ' ', 1: ' ', 2: 'Saludos', 3: 'Me', 4: 'Llamo', 5: 'a', 6: 'b', 7: 'c', 8: 'd',
    9: 'e', 10: 'f', 11: 'g', 12: 'h', 13: 'i', 14: 'j', 15: 'k', 16: 'l', 17: 'm', 18: 'n',
    19: 'ene', 20: 'o', 21: 'p', 22: 'q', 23: 'r', 24: 's', 25: 't', 26: 'u', 27: 'v', 28: 'w',
    29: 'y', 30: 'Yo', 31: 'Tu', 32: 'Nosotros', 33: 'Ustedes', 34: 'Ella', 35: 'Hola',36:'Gracias',
    37: 'Porfavor', 38: 'Sonreir'
}

# Configuración de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Lista de imágenes de signos
sign_images = [None,None,'Saludos.jpg','Me.jpg','Llamo.jpg','a.jpeg', 'b.jpeg', 'c.jpeg', 'd.jpeg', 'e.jpeg', 'f.jpeg', 'g.jpeg', 'h.jpeg', 
               'i.jpeg', 'j.jpeg', 'k.jpeg', 'l.jpeg', 'm.jpeg', 'n.jpeg', 'ene.jpeg', 'o.jpeg', 
               'p.jpeg', 'q.jpeg', 'r.jpeg', 's.jpeg', 't.jpeg', 'u.jpeg', 'v.jpeg', 'w.jpeg', 
               'y.jpeg','Yo.jpg','Tu.jpg','Nosotros.jpg',None,None,None,'Gracias.jpg','Porfavor.jpg','Sonreir.jpg']

# Filtrar solo gestos con imágenes disponibles
valid_indices = [i for i in range(len(sign_images)) if sign_images[i] is not None]

def new_random_image():
    random_index = random.choice(valid_indices)
    random_image = sign_images[random_index]
    target_label = labels_dict[random_index]
    return random_image, target_label

current_image, current_target = new_random_image()

@app.route('/gestos')
def index():
    return render_template('deteccion.html')

@app.route('/gestos/get_current_image')
def get_current_image():
    try:
        image_url = url_for('static', filename=f'sign_images/alfabeto/{current_image}', _external=True)
        checkmark_url = url_for('static', filename='check_image/checkmark.png', _external=True)
        return jsonify({
            'image_url': image_url,
            'target': current_target,
            'status': 'success',
            'checkmark_url': checkmark_url
        })
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/gestos/skip', methods=['POST'])
def skip_image():
    global current_image, current_target
    try:
        # Cambiar a una nueva imagen aleatoria
        current_image, current_target = new_random_image()
        return jsonify({
            'status': 'success',
            'message': 'Seña cambiada exitosamente',
            'image_url': url_for('static', filename=f'sign_images/alfabeto/{current_image}', _external=True),
            'target': current_target
        })
    except Exception as e:
        print(f"Error al cambiar la seña: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/gestos/predict', methods=['POST'])
def predict():
    global current_image, current_target
    data = request.get_json()
    frame_base64 = data.get('frame')

    if not frame_base64:
        return jsonify({'prediction': 'No se recibió ningún frame'})

    try:
        # Decodificar el frame base64
        frame_bytes = base64.b64decode(frame_base64)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        # Procesar el frame con MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            data_aux = []
            x_ = []
            y_ = []

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))

            # Asegurarse de que data_aux tenga exactamente 100 características
            if len(data_aux) < 100:
                data_aux.extend([0] * (100 - len(data_aux)))
            elif len(data_aux) > 100:
                data_aux = data_aux[:100]

            data_aux = np.asarray(data_aux)
            prediction = model.predict([data_aux])
            predicted_index = int(prediction[0])
            predicted_character = labels_dict.get(predicted_index, "Desconocido")

            is_correct = predicted_character.strip().lower() == current_target.strip().lower()
            
            if is_correct:
                current_image, current_target = new_random_image()

            return jsonify({
                'is_correct': is_correct,
                'target': current_target
            })


    except Exception as e:
        print("Error al procesar el frame:", e)
        return jsonify({'prediction': f'Error al procesar el frame: {str(e)}'})

if __name__ == '__main__':
    app.run(port=5000)