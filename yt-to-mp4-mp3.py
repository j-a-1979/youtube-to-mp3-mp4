import tkinter as tk
from tkinter import messagebox
from pytubefix import YouTube
from pytubefix import Playlist
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













def playlist_download():
    # Hide the main window
    window.withdraw()
    
    # Create the second window
    second_window = tk.Toplevel()
    second_window.title("mp4tool")
    second_window.geometry('600x500')
    second_window.resizable(False, False)
    second_window.configure(bg='BLACK')
    

    def playlist():

        video_url = url_link.get()

        if not video_url:
            messagebox.showerror('Error', 'Please enter a playlist URL.')
            return

        try:
            pl = Playlist(video_url)
            video_urls = list(pl.video_urls) if hasattr(pl, 'video_urls') else [video.watch_url for video in pl.videos]

            if not video_urls:
                raise ValueError('No videos found in playlist.')

            for index, item_url in enumerate(video_urls, start=1):
                yt = YouTube(item_url, on_progress_callback=on_progress)
                print(f"Downloading [{index}/{len(video_urls)}]: {yt.title}")
                ys = yt.streams.get_highest_resolution()
                ys.download()

            success = tk.Label(second_window, fg='BLACK', text='PLAYLIST DOWNLOAD COMPLETED SUCCESSFULLY!')
            success.pack(pady=5)
            messagebox.showinfo('Awesome!', 'Playlist download completed successfully!')
            print("\nPlaylist download completed successfully!")

        except Exception as e:
            messagebox.showerror('Error', 'An error occurred while downloading the playlist. Please enter a valid URL.')
            print(f"An error occurred: {e}")

    def playlist_mp3():

        video_url = url_link.get()

        if not video_url:
            messagebox.showerror('Error', 'Please enter a playlist URL.')
            return

        try:
            pl = Playlist(video_url)
            video_urls = list(pl.video_urls) if hasattr(pl, 'video_urls') else [video.watch_url for video in pl.videos]

            if not video_urls:
                raise ValueError('No videos found in playlist.')

            for index, item_url in enumerate(video_urls, start=1):
                yt = YouTube(item_url, on_progress_callback=on_progress)
                print(f"Downloading audio [{index}/{len(video_urls)}]: {yt.title}")
                ys = yt.streams.get_audio_only()
                ys.download()

            success = tk.Label(second_window, fg='BLACK', text='PLAYLIST MP3 DOWNLOAD COMPLETED SUCCESSFULLY!')
            success.pack(pady=5)
            messagebox.showinfo('Awesome!', 'Playlist MP3 download completed successfully!')
            print("\nPlaylist MP3 download completed successfully!")

        except Exception as e:
            messagebox.showerror('Error', 'An error occurred while downloading the playlist audio. Please enter a valid URL.')
            print(f"An error occurred: {e}")


    enter_url = tk.Label(second_window, bg='BLACK', fg='WHITE', text='ENTER YOUR URL: ', font='Helvetica')
    enter_url.pack(pady=20)

    url_link = tk.Entry(second_window, bg='GRAY', fg='BLACK', width=44)
    url_link.pack(pady=10)

    download_btn = tk.Button(second_window, bg='BLACK', fg='WHITE', text='DOWNLOAD MP4', command=playlist)
    download_btn.pack(pady=10)

    mp3_btn = tk.Button(second_window, bg='BLACK', fg='WHITE', text='DOWNLOAD MP3', command=playlist_mp3)
    mp3_btn.pack(pady=10)








    # Function to go back to the main menu
    def go_back():
        second_window.destroy()
        window.deiconify() # Restore the main window
        
    # Placeholder label for the second menu
    menu2_label = tk.Label(second_window, bg='BLACK', fg='WHITE', text='playlist downloader', font='Helvetica')
    menu2_label.pack(pady=20)
    
    # Button to go back
    back_btn = tk.Button(second_window, bg='BLACK', fg='WHITE', text='download mp3/mp4', command=go_back)
    back_btn.pack(pady=10)







































window = tk.Tk()
window.title("mp4tool")
window.geometry('600x500')
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

# NEW BUTTON TO NAVIGATE TO SECOND MENU
next_menu_btn = tk.Button(window, bg='BLACK', fg='WHITE', text='playlist downloader', command=playlist_download)
next_menu_btn.pack(pady=10)

window.mainloop()