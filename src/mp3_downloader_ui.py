import tkinter as tk
from mp3_downloader import Mp3Downloader
from tkinter import filedialog
import os
import threading
import webbrowser


class Mp3DownloaderUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MP3 Downloader")

        # Width for input fields
        input_width = 50

        # URL entry
        url_label = tk.Label(self.root, text="Enter URLs (comma-separated):")
        url_label.pack()
        self.url_entry = tk.Entry(self.root, width=input_width)
        self.url_entry.pack()

        # Output directory entry
        output_label = tk.Label(self.root, text="Select Output Directory:")
        output_label.pack()
        self.output_entry = tk.Entry(self.root, width=input_width)
        self.output_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))
        self.output_entry.pack()

        # Browse button for output directory
        browse_button = tk.Button(
            self.root, text="Browse", command=self.browse_output_directory
        )
        browse_button.pack()

        site_button = tk.Button(self.root, text="Open Site", command=self.open_url)
        site_button.pack()

        # Run button
        run_button = tk.Button(
            self.root, text="Run Download", command=self.run_download
        )
        run_button.pack()

        # Clear Log button
        clear_log_button = tk.Button(
            self.root, text="Clear Log", command=self.clear_log
        )
        clear_log_button.pack()

        # Output log text widget
        self.log_text = tk.Text(self.root, height=10, width=input_width)
        self.log_text.pack()

    def browse_output_directory(self):
        output_directory = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, output_directory)

    def run_download(self):
        urls = self.url_entry.get().split(",")
        output_directory = self.output_entry.get()

        download_thread = threading.Thread(
            target=self.download_files, args=(urls, output_directory)
        )
        download_thread.start()

    def download_files(self, urls, output_directory):
        self.update_log(f"Downloading MP3s from {urls} to {output_directory}")

        Mp3Downloader(self).start_download(urls=urls, download_dir=output_directory)

        self.update_log("Download operation complete!")

    def update_log(self, message):
        # Display log message in the text widget
        self.log_text.insert(tk.END, message + "\n")
        # Automatically scroll to the bottom to show the latest log messages
        self.log_text.yview(tk.END)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def open_url(self):
        webbrowser.open_new("https://downloads.khinsider.com/")

    def start_ui(self):
        self.root.mainloop()
