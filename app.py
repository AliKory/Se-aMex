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
    0: ' ', 1: ' ', 2: 'a', 3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'f', 8: 'g',
    9: 'h', 10: 'i', 11: 'j', 12: 'k', 13: 'l', 14: 'll', 15: 'm', 16: 'n', 17: 'ñ', 18: 'o',
    19: 'p', 20: 'q', 21: 'r', 22: 'rr', 23: 's', 24: 't', 25: 'u', 26: 'v', 27: 'w', 28: 'x',
    29: 'y', 30: 'z'
}

# Configuración de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Lista de imágenes de signos
sign_images = [
    None,  # Índice 0
    None,  # Índice 1
    'a.jpeg',  # Índice 2
    'b.jpeg',  # Índice 3
    'c.jpeg',  # Índice 4
    'd.jpeg',  # Índice 5
    'e.jpeg',  # Índice 6
    'f.jpeg',  # Índice 7
    'g.jpeg',  # Índice 8
    'h.jpeg',  # Índice 9
    'i.jpeg',  # Índice 10
    'j.jpeg',  # Índice 11
    'k.jpeg',  # Índice 12
    'l.jpeg',  # Índice 13
    'll.jpeg',  # Índice 14 (si tienes una imagen para "ll")
    'm.jpeg',  # Índice 15
    'n.jpeg',  # Índice 16
    'ñ.jpeg',  # Índice 17 (si tienes una imagen para "ñ")
    'o.jpeg',  # Índice 18
    'p.jpeg',  # Índice 19
    'q.jpeg',  # Índice 20
    'r.jpeg',  # Índice 21
    'rr.jpeg',  # Índice 22 (si tienes una imagen para "rr")
    's.jpeg',  # Índice 23
    't.jpeg',  # Índice 24
    'u.jpeg',  # Índice 25
    'v.jpeg',  # Índice 26
    'w.jpeg',  # Índice 27
    'x.jpeg',  # Índice 28
    'y.jpeg',  # Índice 29
    'z.jpeg'   # Índice 30
]

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
        # Actualizar la ruta para apuntar a la carpeta "alphabet"
        image_url = url_for('static', filename=f'sign_images/alphabet/{current_image}', _external=True)
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
            'image_url': url_for('static', filename=f'sign_images/alphabet/{current_image}', _external=True),
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

            print("Predicción generada:", predicted_character)
            return jsonify({
                'prediction': predicted_character,
                'is_correct': is_correct,
                'target': current_target
            })
        return jsonify({'prediction': 'No se detectó ninguna mano'})
    except Exception as e:
        print("Error al procesar el frame:", e)
        return jsonify({'prediction': f'Error al procesar el frame: {str(e)}'})

if __name__ == '__main__':
    app.run(port=5000)