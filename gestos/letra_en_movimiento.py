import cv2
import mediapipe as mp
from Funciones.normalizacionCords import obtenerAngulos

lectura_actual = 0

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)
wCam, hCam = 1280, 720
cap.set(3, wCam)
cap.set(4, hCam)

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.75) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            angulos_id, pinky = obtenerAngulos(results, width, height)

            dedos = [int(angle > 90) for angle in angulos_id[:5]]  # Lista de comprensión para dedos

            TotalDedos = dedos.count(1)

            pinky_suma = pinky[1] + pinky[0]
            resta = pinky_suma - lectura_actual
            lectura_actual = pinky_suma

            print(abs(resta), pinky_suma, lectura_actual)

            if abs(resta) > 30:
                print("Jota en movimiento")
                mostrar_letra(frame, 'J')

            if dedos == [0, 0, 1, 0, 0]:
                print("Letra I")
                mostrar_letra(frame, 'I')

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()

def mostrar_letra(frame, letra):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
    cv2.putText(frame, letra, (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
    print(letra)
