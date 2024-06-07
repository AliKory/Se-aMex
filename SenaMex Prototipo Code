import cv2
import mediapipe as mp
import numpy as np
import pyttsx3  # Para la síntesis de voz

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

def distancia_euclidiana(p1, p2):
    d = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return d

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)  # Cambia el índice si es necesario

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Estado para detectar la seña "ELLA"
ella_etapa = 0

with mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as holistic, mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(frame_rgb)
        hands_results = hands.process(frame_rgb)

        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # Detección y dibujo de cuerpo
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1)
            )

            # Obtener la coordenada del pecho (esternón) o hombro derecho
            chest_landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
            chest_coords = (int(chest_landmark.x * frame.shape[1]), int(chest_landmark.y * frame.shape[0]))

            # Obtener la coordenada de la mejilla (usando el ojo izquierdo)
            cheek_landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE]
            cheek_coords = (int(cheek_landmark.x * frame.shape[1]), int(cheek_landmark.y * frame.shape[0]))

        # Detección y dibujo de manos
        if hands_results.multi_hand_landmarks:
            for num, hand_landmarks in enumerate(hands_results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1)
                )

                index_finger_tip = (int(hand_landmarks.landmark[8].x * frame.shape[1]),
                                    int(hand_landmarks.landmark[8].y * frame.shape[0]))
                index_finger_pip = (int(hand_landmarks.landmark[6].x * frame.shape[1]),
                                    int(hand_landmarks.landmark[6].y * frame.shape[0]))
                
                thumb_tip = (int(hand_landmarks.landmark[4].x * frame.shape[1]),
                             int(hand_landmarks.landmark[4].y * frame.shape[0]))
                thumb_pip = (int(hand_landmarks.landmark[2].x * frame.shape[1]),
                             int(hand_landmarks.landmark[2].y * frame.shape[0]))
                
                middle_finger_tip = (int(hand_landmarks.landmark[12].x * frame.shape[1]),
                                     int(hand_landmarks.landmark[12].y * frame.shape[0]))
                pinky_tip = (int(hand_landmarks.landmark[20].x * frame.shape[1]),
                             int(hand_landmarks.landmark[20].y * frame.shape[0]))
                pinky_pip = (int(hand_landmarks.landmark[18].x * frame.shape[1]),
                             int(hand_landmarks.landmark[18].y * frame.shape[0]))  # Definir pinky_pip

                # Detectar señas
                if thumb_pip[1] - thumb_tip[1] > 0 and thumb_pip[1] - index_finger_tip[1] < 0 \
                    and thumb_pip[1] - middle_finger_tip[1] < 0 and thumb_pip[1] - pinky_tip[1] < 0:
                    cv2.putText(frame, 'BIEN', (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (0, 255, 0), 2) 
                    engine.say('Bien')
                    engine.runAndWait()
                elif thumb_pip[1] - thumb_tip[1] < 0 and thumb_pip[1] - index_finger_tip[1] > 0 \
                    and thumb_pip[1] - middle_finger_tip[1] > 0 and thumb_pip[1] - pinky_tip[1] > 0:
                    cv2.putText(frame, 'MAL', (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (0, 0, 255), 2)
                    engine.say('Mal')
                    engine.runAndWait()
                elif results.pose_landmarks and distancia_euclidiana(index_finger_tip, chest_coords) < 50:  # Umbral de distancia para la seña "YO"
                    cv2.putText(frame, 'YO', (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (255, 0, 0), 2)
                    engine.say('Yo')
                    engine.runAndWait()
                elif abs(index_finger_tip[1] - index_finger_pip[1]) < 10 and abs(index_finger_tip[0] - index_finger_pip[0]) > 50:  # Señal horizontal
                    cv2.putText(frame, 'EL', (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (255, 255, 0), 2)
                    engine.say('El')
                    engine.runAndWait()
                elif ella_etapa == 0 and distancia_euclidiana(index_finger_tip, cheek_coords) < 50:  # Umbral de distancia para tocar la mejilla
                    ella_etapa = 1  # Tocar la mejilla
                elif ella_etapa == 1 and abs(index_finger_tip[1] - index_finger_pip[1]) < 10 and abs(index_finger_tip[0] - index_finger_pip[0]) > 50:  # Señal horizontal después de tocar la mejilla
                    cv2.putText(frame, 'ELLA', (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (255, 0, 255), 2)
                    engine.say('Ella')
                    engine.runAndWait()
                    ella_etapa = 0  # Reiniciar estado de "ELLA"
                
        # Voltear la imagen horizontalmente para una vista de espejo
        frame = cv2.flip(frame, 1)

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Presiona 'Esc' para salir
            break

cap.release()
cv2.destroyAllWindows()
