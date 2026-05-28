import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox
from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
from PIL import Image

def output_folder():
    folder_selected = ctk.filedialog.askdirectory(title="Select Download Folder")
    if folder_selected:
        os.chdir(folder_selected)
        folder_label.configure(text='folder: ' + folder_selected)

def download():
    video_url = url_link.get()
    if not video_url:
        messagebox.showerror('Error', 'Please enter a URL.')
        return
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path=os.getcwd())
        messagebox.showinfo('Success', 'Download completed!')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def mp3():
    video_url = url_link.get()
    if not video_url:
        messagebox.showerror('Error', 'Please enter a URL.')
        return
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()
        out_file = ys.download(output_path=os.getcwd())
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        subprocess.run(['ffmpeg', '-i', out_file, '-vn', '-b:a', '320k', new_file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.remove(out_file)
        messagebox.showinfo('Awesome!', 'Conversion completed!')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def playlist_download():
    window.withdraw()
    second_window = ctk.CTkToplevel()
    second_window.title("dubbedcat")
    second_window.geometry('450x450')
    second_window.resizable(False, False)
    second_window.configure(fg_color='BLACK')
    
    btn_style = {
        "corner_radius": 0, "fg_color": "#000000", "border_width": 1,
        "border_color": "#FFFFFF", "text_color": "#FFFFFF",
        "hover_color": "#333333", "height": 40, "font": ("Courier New", 16)
    }

    def playlist_action():
        url = url_link2.get()
        if not url: return
        pl = Playlist(url)
        for video in pl.videos:
            video.streams.get_highest_resolution().download(output_path=os.getcwd())
        messagebox.showinfo('Success', 'Playlist downloaded!')

    def mp3_playlist_action():
        url = url_link2.get()
        if not url: return
        pl = Playlist(url)
        for video in pl.videos:
            out_file = video.streams.get_audio_only().download(output_path=os.getcwd())
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            subprocess.run(['ffmpeg', '-i', out_file, '-vn', '-b:a', '320k', new_file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            os.remove(out_file)
        messagebox.showinfo('Success', 'Playlist converted!')

    ctk.CTkLabel(second_window, text='playlist url:', font=('Courier New', 16)).pack(pady=(20, 10))
    url_link2 = ctk.CTkEntry(second_window, width=400, height=35, corner_radius=0)
    url_link2.pack(pady=10)
    ctk.CTkButton(second_window, text='TO MP4', command=playlist_action, **btn_style).pack(pady=10)
    ctk.CTkButton(second_window, text='TO MP3', command=mp3_playlist_action, **btn_style).pack(pady=10)
    ctk.CTkButton(second_window, text='BACK', command=lambda: [second_window.destroy(), window.deiconify()], **btn_style).pack(pady=20)



window = ctk.CTk()
window.title("dubbedcat (yt-to)")
window.geometry('450x450')
window.resizable(False, False)
window.configure(fg_color='BLACK')



btn_style = {
    "corner_radius": 0, "fg_color": "#000000", "border_width": 1,
    "border_color": "#FFFFFF", "text_color": "#FFFFFF",
    "hover_color": "#333333", "height": 40, "font": ("Courier New", 16)
}

ctk.CTkButton(window, text='OUTPUT FOLDER', command=output_folder, **btn_style).pack(pady=10)
folder_label = ctk.CTkLabel(window, text='folder: ' + os.getcwd(), font=('Courier New', 14))
folder_label.pack(pady=10)
ctk.CTkLabel(window, text='url:', font=('Courier New', 16)).pack(pady=10)
url_link = ctk.CTkEntry(window, width=400, height=35, corner_radius=0)
url_link.pack(pady=10)
ctk.CTkButton(window, text='TO MP4', command=download, **btn_style).pack(pady=10)
ctk.CTkButton(window, text='TO MP3', command=mp3, **btn_style).pack(pady=10)
ctk.CTkButton(window, text='PLAYLIST DOWNLOADER', command=playlist_download, **btn_style).pack(pady=10)

footer = ctk.CTkFrame(window, height=30, fg_color="black", corner_radius=0)
footer.pack(side="bottom", fill="x")

# Agrega el texto dentro del footer
status_label = ctk.CTkLabel(
    footer, 
    text="DUBBEDCAT - YT-TO (v1.0)", 
    font=("Courier New", 10), 
    text_color="#FFFFFF"
)
status_label.pack(pady=5)

logo_image = ctk.CTkImage(
    light_image=Image.open("cat.png"),
    dark_image=Image.open("cat.png"),
    size=(50, 50)
)


image_label = ctk.CTkLabel(window, image=logo_image, text="")
image_label.pack(pady=20)

window.mainloop()