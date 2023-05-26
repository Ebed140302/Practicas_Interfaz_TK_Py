import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import pytube
from PIL import Image, ImageTk
import requests

# Función para descargar el video
def download_video():
    url = entry_url.get()
    quality = combo_quality.get()
    audio_only = var_audio_only.get()

    try:
        # Obtener objeto de video de YouTube
        video = pytube.YouTube(url)

        if audio_only:
            # Descargar solo el audio
            stream = video.streams.filter(only_audio=True).first()
        else:
            # Descargar video con la calidad seleccionada
            stream = video.streams.filter(progressive=True, file_extension='mp4', resolution=quality).first()

        # Descargar el video o el audio
        file_path = stream.download()

        messagebox.showinfo('Éxito', 'Descarga completada.\nArchivo guardado en: ' + file_path)

    except Exception as e:
        messagebox.showerror('Error', str(e))

    # Limpiar la entrada
    entry_url.delete(0, tk.END)


# Función para cargar la miniatura del video
def load_thumbnail():
    url = entry_url.get()

    try:
        # Obtener objeto de video de YouTube
        video = pytube.YouTube(url)

        # Obtener la miniatura del video
        thumbnail_url = video.thumbnail_url
        thumbnail_image = Image.open(requests.get(thumbnail_url, stream=True).raw)
        thumbnail_image = thumbnail_image.resize((200, 150), Image.ANTIALIAS)
        thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)

        # Mostrar la miniatura en el widget Label
        label_thumbnail.config(image=thumbnail_photo)
        label_thumbnail.image = thumbnail_photo

    except Exception as e:
        messagebox.showerror('Error', str(e))


# Crear la ventana principal
window = tk.Tk()
window.title('Descargar videos de YouTube')

# Crear elementos de la interfaz
label_url = tk.Label(window, text='URL del video de YouTube:')
label_url.pack()

entry_url = tk.Entry(window)
entry_url.pack()

button_load_thumbnail = tk.Button(window, text='Cargar miniatura', command=load_thumbnail)
button_load_thumbnail.pack()

label_thumbnail = tk.Label(window)
label_thumbnail.pack()

label_quality = tk.Label(window, text='Calidad:')
label_quality.pack()

combo_quality = tk.ttk.Combobox(window, values=['720p', '480p', '360p', '240p', '144p'])
combo_quality.pack()

var_audio_only = tk.BooleanVar()
check_audio_only = tk.Checkbutton(window, text='Descargar solo audio', variable=var_audio_only)
check_audio_only.pack()

button_download = tk.Button(window, text='Descargar', command=download_video)
button_download.pack()

progress_bar = Progressbar(window, orient='horizontal', length=200, mode='indeterminate')
progress_bar.pack()

# Ejecutar la ventana
window.mainloop()
