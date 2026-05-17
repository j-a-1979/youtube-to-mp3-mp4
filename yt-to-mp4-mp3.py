import tkinter as tk
from tkinter import messagebox
from pytubefix import YouTube
from pytubefix.cli import on_progress

def download():
    video_url = url_link.get()
    

    if not video_url:
        messagebox.showerror('Error', 'Please enter a URL.')
        return

    try:
        
        yt = YouTube(video_url, on_progress_callback=on_progress)
               
        print(f"Downloading: {yt.title}")
        
        # Get the highest resolution progressive stream (contains both audio and video)
        ys = yt.streams.get_highest_resolution()
        
        # Download the video to the current working directory
        ys.download()
        success = tk.Label(window, fg='BLACK' ,text='DOWNLOAD COMPLETED SUCCESSFULLY!')
        success.pack()
        print("\nDownload completed successfully!")
    
    except Exception as e:
        messagebox.showerror('Error','An error ocurred please enter a valid URL.' )
        print(f"An error occurred: {e}")


def mp3():

    video_url = url_link.get()

    try:
        
        yt = YouTube(video_url, on_progress_callback=on_progress)
               
        print(f"Downloading: {yt.title}")
        
        # Get the highest resolution progressive stream (contains both audio and video)
        ys = yt.streams.get_audio_only()
        
        # Download the video to the current working directory
        ys.download()

        messagebox.showinfo('Awesome!', 'Download completed successfully!')
        print("\nDownload completed successfully!")

    except Exception as e:

        messagebox.showerror('Error', 'An error ocurred please enter a valid URL.' )
        print(f"An error occurred: {e}")        
  







window = tk.Tk()
window.title("mp4tool")
window.geometry('600x300')
window.resizable(False, False)
window.configure(bg='BLACK')

enter_url = tk.Label(window, bg='BLACK', fg='WHITE', text='ENTER YOUR URL: ', font='Helvetica')
enter_url.pack(pady=20)

url_link = tk.Entry(window, bg='GRAY', fg='BLACK', width=44)
url_link.pack(pady=10)

download_btn = tk.Button(window, bg='BLACK', fg='WHITE', text='DOWNLOAD MP4', command=download)
download_btn.pack(pady=10)

mp3_btn = tk.Button(window, bg='BLACK', fg='WHITE', text='DOWNLOAD MP3', command=mp3)
mp3_btn.pack(pady=10)















window.mainloop()


