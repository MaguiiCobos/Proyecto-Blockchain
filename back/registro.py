import cv2
import face_recognition as fr

print("Bienvenid@ al sistema de registro de asistencia de Invictus")
opcion = input("Quieres registrarte? (S/N): ").strip().upper()

if opcion == "S":
    print("Validaremos tu imagen con nuestra base de datos de empleados")
    captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    exito, imagen = captura.read()
    if exito:
        print("Te has registrado correctamente.")
elif opcion == "N":
    print("Has elegido no registrarte.")
else:
    print("Opcion no valida. Por favor, elige 'S' o 'N'.")
