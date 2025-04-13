import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1)

# Captura de video
cap = cv2.VideoCapture(0)

# Posición inicial del objeto virtual
obj_x, obj_y = 300, 300
sujetando = False

# Suavizado de movimientos
filtro_suavizado = 0.2
obj_x_f, obj_y_f = obj_x, obj_y

def detectar_gesto(hand_landmarks):
    # Obtener coordenadas de los dedos índice y pulgar
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    
    # Calcular distancias entre puntos clave
    distancia_thumb_index = np.linalg.norm([thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y])
    distancia_index_middle = np.linalg.norm([index_tip.x - middle_tip.x, index_tip.y - middle_tip.y])
    
    # Determinar si es un gesto de "agarre" o "soltar" con mayor precisión
    if distancia_thumb_index < 0.05 and distancia_index_middle < 0.05:
        return "agarre"
    else:
        return "soltar"
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Voltear la imagen para efecto espejo
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesar la imagen con MediaPipe Hands
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extraer coordenadas del dedo índice
            h, w, _ = frame.shape
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            
            # Detectar gesto
            gesto = detectar_gesto(hand_landmarks)
            if gesto == "agarre":
                sujetando = True
            elif gesto == "soltar":
                sujetando = False
            
            # Mover el objeto si está sujeto con suavizado de movimientos
            if sujetando:
                obj_x_f = filtro_suavizado * cx + (1 - filtro_suavizado) * obj_x_f
                obj_y_f = filtro_suavizado * cy + (1 - filtro_suavizado) * obj_y_f
                obj_x, obj_y = int(obj_x_f), int(obj_y_f)
