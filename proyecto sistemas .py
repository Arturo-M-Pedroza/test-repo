import cv2
from twilio.rest import Client

# Cargar cascadas Haar preentrenadas
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

def detect_and_capture():
    cap = cv2.VideoCapture(0)  # Usar cámara
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 22)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
                # Tomar captura
                img_path = "smile_capture.jpg"
                cv2.imwrite(img_path, frame)
                send_message(img_path)  # Llamar función de envío
                break  # Salir al detectar sonrisa

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def send_message(img_path):
    account_sid = 'TU_ACCOUNT_SID'
    auth_token = 'TU_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="¡Sonrisa detectada! Aquí está la imagen.",
        from_='TU_NUMERO_TWILIO',
        to='NUMERO_DESTINATARIO',
        media_url=[f'https://path/to/{img_path}']
    )
    print(f"Mensaje enviado: {message.sid}")
