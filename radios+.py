import speech_recognition as sr
import threading
from pydub import AudioSegment, silence

# Crear un objeto recognizer
r = sr.Recognizer()

# Crear un objeto mic para la entrada de audio
mic = sr.Microphone()

# Definir los parámetros de silencio
MIN_SILENCE_LEN = 10000  # Duración mínima del silencio en ms (10 segundos)
SILENCE_THRESH = -50  # Umbral de silencio en dBFS (decibeles de escala completa)

# Función para transcribir el audio y guardar en un archivo separado
def transcribir_audio(filename):
    with sr.AudioFile(filename) as source:
        audio = r.record(source)  # Leer el archivo de audio
    try:
        texto = r.recognize_google(audio, language="es-ES") # Reconocer el audio usando Google Speech Recognition
        print("Transcripción: " + texto)
        with open(f"transcripcion-{filename}.txt", "w") as file:
            file.write(texto) # Escribir la transcripción en el archivo
    except sr.UnknownValueError:
        print("No se ha podido reconocer el audio")
    except sr.RequestError as e:
        print("Error al conectarse al servicio de reconocimiento de voz: {0}".format(e))

# Función para detectar silencio y dividir el audio en archivos separados
def dividir_audio(filename):
    audio = AudioSegment.from_file(filename, format="wav")
    chunks = silence.split_on_silence(audio, min_silence_len=MIN_SILENCE_LEN, silence_thresh=SILENCE_THRESH)
    for i, chunk in enumerate(chunks):
        chunk.export(f"audio-{filename}-{i}.wav", format="wav")  # Exportar cada chunk a un archivo separado
        threading.Thread(target=transcribir_audio, args=(f"audio-{filename}-{i}.wav",)).start()  # Iniciar la transcripción en un hilo separado

# Iniciar la escucha en segundo plano
with mic as source:
    r.adjust_for_ambient_noise(source) # Ajustar el nivel de ruido
    audio_stream = r.listen_in_background(source, dividir_audio)

# Detener la escucha después de 10 minutos(no funciona .stop)
#audio_stream.stop(600)
