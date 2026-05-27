from tkinter import messagebox
import os
import subprocess
from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
import customtkinter as ctk

def output_folder():
    folder_selected = ctk.filedialog.askdirectory(title="Select Download Folder")
    if folder_selected:
        os.chdir(folder_selected)
        folder_label.config(text='folder: ' + folder_selected)


def download():

    video_url = url_link.get()
    
    if not video_url:
        messagebox.showerror('Error', 'Please enter a URL.')
        return

    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        print(f"Downloading MP4: {yt.title}")
        
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path=os.getcwd())
        
        success = ctk.CTkLabel(window, fg_color='black', text='DOWNLOAD COMPLETED SUCCESSFULLY!')
        success.pack()
        print("\nDownload completed successfully!")
    
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')
        print(f"An error occurred: {e}")

def mp3():
    video_url = url_link.get()

    if not video_url:
        messagebox.showerror('Error', 'Please enter a URL.')
        return

    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        print(f"Downloading Audio: {yt.title}")
        
        ys = yt.streams.get_audio_only()
        out_file = ys.download(output_path=os.getcwd())
        
        # Get the file names ready
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        
        print(f"Converting to REAL MP3: {new_file}")
        

        subprocess.run(['ffmpeg', '-i', out_file, '-vn', '-b:a', '320k', new_file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        

        os.remove(out_file)

        messagebox.showinfo('Awesome!', 'Download and conversion completed successfully!')
        print("\nConversion completed successfully!")

    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')
        print(f"An error occurred: {e}")        

def playlist_download():
    window.withdraw()

    second_window = ctk.CTkToplevel()
    second_window.title("mp4tool")
    second_window.geometry('600x500')
    second_window.resizable(False, False)
    second_window.configure(bg='BLACK')
    
    def playlist():
        url = url_link2.get()
        if not url:
            messagebox.showerror('Error', 'Please enter a URL.')
            return

        try:
            pl = Playlist(url)
            print(f'Downloading MP4 playlist: {pl.title}')

            for video in pl.videos:
                try:
                    ys = video.streams.get_highest_resolution()
                    ys.download(output_path=os.getcwd())
                    print(f"Success: {video.title}")
                except Exception as ve:
                    print(f"Skipped video due to error: {ve}")

            success = ctk.CTkLabel(second_window, fg_color='black', text='DOWNLOAD COMPLETED SUCCESSFULLY!')
            success.pack()
            print("\nPlaylist download completed!")
            
        except Exception as pe:
            messagebox.showerror('Error', f'Playlist error: {pe}')

    def mp3_playlist():
        url = url_link2.get()
        if not url:
            messagebox.showerror('Error', 'Please enter a URL.')
            return

        try:
            pl = Playlist(url)
            print(f'Downloading and converting MP3 playlist: {pl.title}')

            for video in pl.videos:
                try:
                    ys = video.streams.get_audio_only()
                    out_file = ys.download(output_path=os.getcwd())
                    
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    
                    print(f"Converting: {video.title}")
                    
                    subprocess.run(['ffmpeg', '-i', out_file, '-vn', '-b:a', '320k', new_file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                    

                    os.remove(out_file)
                    
                    print(f"Success REAL MP3: {video.title}")
                except Exception as ve:
                    print(f"Skipped video due to error: {ve}")

            success = ctk.CTkLabel(second_window, fg_color='black', text='DOWNLOAD COMPLETED SUCCESSFULLY!')
            success.pack()
            print("\nPlaylist conversion completed!")
            
        except Exception as pe:
            messagebox.showerror('Error', f'Playlist error: {pe}')

    enter_url = ctk.CTkLabel(second_window, text='ENTER YOUR URL: ', font=('Helvetica', 14))
    enter_url.pack(pady=0)

    url_link2 = ctk.CTkEntry(second_window, width=440)
    url_link2.pack(pady=10)

    download_btn = ctk.CTkButton(second_window, text='DOWNLOAD MP4', command=playlist)
    download_btn.pack(pady=10)

    mp3_btn = ctk.CTkButton(second_window, text='DOWNLOAD MP3', command=mp3_playlist)
    mp3_btn.pack(pady=10)

    def go_back():
        second_window.destroy()
        window.deiconify() 
        
    menu2_label = ctk.CTkLabel(second_window, text='playlist downloader', font=('Helvetica', 14))
    menu2_label.pack(pady=20)
    
    back_btn = ctk.CTkButton(second_window, text='download mp3/mp4', command=go_back)
    back_btn.pack(pady=10)

# --- MAIN WINDOW ---
window = ctk.CTk()
window.title("m")
window.geometry('600x500')
window.resizable(False, False)
window.configure(bg='BLACK')

btn_folder = ctk.CTkButton(window, text='Select Download Folder', command=output_folder)
btn_folder.pack(pady=10)

folder_label = ctk.CTkLabel(window, text='folder: ' + os.getcwd(), font=('Helvetica', 14))
folder_label.pack(pady=10)


enter_url = ctk.CTkLabel(window, text='ENTER YOUR URL: ', font=('Helvetica', 14))
enter_url.pack(pady=20)

url_link = ctk.CTkEntry(window, width=440)
url_link.pack(pady=10)

download_btn = ctk.CTkButton(window, text='DOWNLOAD MP4', command=download)
download_btn.pack(pady=10)

mp3_btn = ctk.CTkButton(window, text='DOWNLOAD MP3', command=mp3)
mp3_btn.pack(pady=10)

next_menu_btn = ctk.CTkButton(window, text='playlist downloader', command=playlist_download)
next_menu_btn.pack(pady=10)

window.mainloop()