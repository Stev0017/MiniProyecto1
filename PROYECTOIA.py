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

