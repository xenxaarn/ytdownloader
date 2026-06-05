import sys
import threading
import os
import customtkinter as ctk
from tkinter import messagebox

# Verify dependencies exist before starting
try:
    from yt_dlp import YoutubeDL
    import imageio_ffmpeg
    from plyer import notification
except ImportError as e:
    print(f"CRITICAL ERROR: Missing dependencies. Please run: pip install -r requirements.txt")
    print(f"Details: {e}")
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Missing Dependencies", "Required libraries are missing. Please run: pip install -r requirements.txt")
    sys.exit(1)

# ==========================================
# 2.         YTDOWNLOADER GUI 
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class UltraFriendlyDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ytdownloader")
        self.geometry("580x520")
        self.resizable(False, False)

        self.title_label = ctk.CTkLabel(self, text="⚡ Quick Media Downloader", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        self.url_label = ctk.CTkLabel(self, text="Paste YouTube Link:", font=("Arial", 12, "bold"))
        self.url_label.pack(pady=2)
        
        self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.url_frame.pack(pady=5)
        
        self.url_entry = ctk.CTkEntry(self.url_frame, width=340, placeholder_text="https://www.youtube.com/watch?v=...")
        self.url_entry.pack(side="left", padx=5)
        
        self.paste_btn = ctk.CTkButton(self.url_frame, text="📋 Paste", width=90, fg_color="#242424", command=self.paste_from_clipboard)
        self.paste_btn.pack(side="left", padx=5)

        self.dest_label = ctk.CTkLabel(self, text="Where to Save:", font=("Arial", 12, "bold"))
        self.dest_label.pack(pady=2)
        
        self.dest_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dest_frame.pack(pady=5)
        
        self.dest_entry = ctk.CTkEntry(self.dest_frame, width=340)
        self.dest_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))
        self.dest_entry.pack(side="left", padx=5)
        
        self.browse_btn = ctk.CTkButton(self.dest_frame, text="Browse", width=90, command=self.browse_folder)
        self.browse_btn.pack(side="left", padx=5)

        self.format_label = ctk.CTkLabel(self, text="Choose Format:", font=("Arial", 12, "bold"))
        self.format_label.pack(pady=5)
        
        self.format_option = ctk.CTkOptionMenu(self, width=250, values=["MP4 (Standard Video)", "MKV (HD Video)", "MP3 (Audio Only)", "M4A (High Quality Audio)"])
        self.format_option.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="System ready.", font=("Arial", 12), text_color="#a3a3a3")
        self.status_label.pack(pady=(25, 5))

        self.progress_bar = ctk.CTkProgressBar(self, width=440)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.download_btn = ctk.CTkButton(self, text="Download Now", font=("Arial", 16, "bold"), height=45, width=440, command=self.start_download_thread)
        self.download_btn.pack(pady=25)

    def paste_from_clipboard(self):
        try:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, self.clipboard_get())
        except: pass

    def browse_folder(self):
        folder = ctk.filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, folder)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                self.progress_bar.set(d.get('downloaded_bytes', 0) / total)
        elif d['status'] == 'finished':
            self.progress_bar.set(1.0)

    def start_download_thread(self):
        self.download_btn.configure(state="disabled")
        threading.Thread(target=self.execute_download, daemon=True).start()

    def execute_download(self):
        url = self.url_entry.get().strip()
        path = self.dest_entry.get().strip()
        fmt = self.format_option.get()
        
        opts = {'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(), 'progress_hooks': [self.progress_hook], 'outtmpl': os.path.join(path, '%(title)s.%(ext)s')}
        if "MP3" in fmt: opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]})
        elif "MKV" in fmt: opts.update({'format': 'bestvideo+bestaudio/best', 'merge_output_format': 'mkv'})
        else: opts.update({'format': 'bestvideo*[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'merge_output_format': 'mp4'})

        try:
            with YoutubeDL(opts) as ydl: ydl.download([url])
            notification.notify(title="Success!", message="Download finished.", timeout=5)
            self.status_label.configure(text="Complete!", text_color="green")
        except:
            self.status_label.configure(text="Error occurred.", text_color="red")
        self.download_btn.configure(state="normal")

if __name__ == "__main__":
    UltraFriendlyDownloader().mainloop()