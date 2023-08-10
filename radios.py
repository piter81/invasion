#solo probando git, dspues se puede borrar esta linea
import speech_recognition as sr

# Crear un objeto recognizer
r = sr.Recognizer()

# Crear un objeto mic para la entrada de audio
mic = sr.Microphone()

# Crear un archivo para guardar la transcripción
file = open("transcripcion.txt", "w")

# Definir la duración máxima de la grabación
DURACION_MAXIMA_GRABACION = 30

# Función para transcribir el audio
def transcribir_audio():
    with mic as source:
        r.adjust_for_ambient_noise(source) # Ajustar el nivel de ruido
        audio = r.listen(source, phrase_time_limit=DURACION_MAXIMA_GRABACION) # Escuchar la entrada de audio
    try:
        texto = r.recognize_google(audio, language="es-ES") # Reconocer el audio usando Google Speech Recognition
        print("Transcripción: " + texto)
        file.write(texto) # Escribir la transcripción en el archivo
    except sr.UnknownValueError:
        print("No se ha podido reconocer el audio")
    except sr.RequestError as e:
        print("Error al conectarse al servicio de reconocimiento de voz: {0}".format(e))

# Bucle para escuchar la entrada de audio en tiempo real
while True:
    transcribir_audio()
