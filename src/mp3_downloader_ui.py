import tkinter as tk
from mp3_downloader import Mp3Downloader
from tkinter import filedialog
import threading


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
        self.output_entry.pack()

        # Browse button for output directory
        browse_button = tk.Button(
            self.root, text="Browse", command=self.browse_output_directory
        )
        browse_button.pack()

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

        # Create a thread to run the download
        download_thread = threading.Thread(
            target=self.download_files, args=(urls, output_directory)
        )
        download_thread.start()

    def download_files(self, urls, output_directory):

        # Example log messages
        self.update_log(f"Downloading MP3s from {urls} to {output_directory}")

        # Replace the following line with your existing code and capture any log messages
        log_message = "Download operation in progress...\n"

        # Example log message during the download process
        self.update_log(log_message)

        Mp3Downloader(self).start_download(urls=urls, download_dir=output_directory)

        # Example completion message
        self.update_log("Download operation complete!")

    def update_log(self, message):
        # Display log message in the text widget
        self.log_text.insert(tk.END, message + "\n")
        # Automatically scroll to the bottom to show the latest log messages
        self.log_text.yview(tk.END)

    def clear_log(self):
        # Clear the log text widget
        self.log_text.delete(1.0, tk.END)

    def start_ui(self):
        self.root.mainloop()
