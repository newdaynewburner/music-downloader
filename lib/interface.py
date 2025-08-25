"""
lib/interface.py

Contains various UI components
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class GUI(object):
    """ Contains the program's tkinter-based graphical user
    interface and it's components

    Methods:
        __init__() - Initialize the object
        create_video_download_tab() - Create a tab for video downloads
        create_playlist_download_tab() - Create a tab for playlist downloads
    """

    def __init__(self, download_manager):
        """ Initialize the object

        Arguments:
            self - object - This object

        Returns:
            None
        """

        # Store arguments locally
        self.download_manager = download_manager

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Music Downloader")
        self.root.geometry("500x300")

        # Initialize Tkinter variables with default values
        self.url_var = tk.StringVar()
        self.outdir_var = tk.StringVar(value=self.download_manager.outdir)
        self.format_var = tk.StringVar(value=self.download_manager.preferred_format)

        # Initialize the status bar message
        self.status_message = tk.StringVar()
        self.status_message.set("Ready")

        # Create tkinter notebook and initialize tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.init_video_download_tab()
        self.init_playlist_download_tab()

        # Create the status bar
        self.status_label = tk.Label(self.root, textvariable=self.status_message, relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

        # Start the main loop
        self.root.mainloop()

    def init_video_download_tab(self):
        """ Create a tab for video downloads

        Arguments:
            self - object - This object

        Returns:
            None
        """

        # Initialize the tab
        self.video_download_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.video_download_tab, text="Video Download")

        # URL input section
        tk.Label(self.video_download_tab, text="Video URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.video_url_entry = tk.Entry(self.video_download_tab, textvariable=self.url_var, width=40)
        self.video_url_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.video_download_tab, text="Paste", command=lambda: self.paste_clipboard(self.video_url_entry)).grid(row=0, column=2, padx=5)

        # Format selection section
        tk.Label(self.video_download_tab, text="Format:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Radiobutton(self.video_download_tab, text="MP3", variable=self.format_var, value="mp3").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self.video_download_tab, text="M4A", variable=self.format_var, value="m4a").grid(row=1, column=1)
        tk.Radiobutton(self.video_download_tab, text="WAV", variable=self.format_var, value="wav").grid(row=1, column=1, sticky="e")

        # Download location section
        tk.Label(self.video_download_tab, text="Destination:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.download_location_entry = tk.Entry(self.video_download_tab, textvariable=self.outdir_var, width=40)
        self.download_location_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.video_download_tab, text="Browse", command=lambda: self.browse_folder(self.download_location_entry)).grid(row=2, column=2, padx=5)

        # Download and Exit buttons
        tk.Button(self.video_download_tab, text="Download", width=10, command=self.download_video).grid(row=3, column=1, sticky="w", pady=10)
        tk.Button(self.video_download_tab, text="Exit", width=10, command=self.root.destroy).grid(row=3, column=1, sticky="e", pady=10)


    def init_playlist_download_tab(self):
        """ Create a tab for playlist downloads

        Arguments:
            self - object - This object

        Returns:
            None
        """

        # Initialize the tab
        self.playlist_download_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.playlist_download_tab, text="Playlist Download")

        # URL input section
        tk.Label(self.playlist_download_tab, text="Playlist URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.playlist_url_entry = tk.Entry(self.playlist_download_tab, textvariable=self.url_var, width=40)
        self.playlist_url_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.playlist_download_tab, text="Paste", command=lambda: self.paste_clipboard(self.playlist_url_entry)).grid(row=0, column=2, padx=5)

        # Format selection section
        tk.Label(self.playlist_download_tab, text="Format:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Radiobutton(self.playlist_download_tab, text="MP3", variable=self.format_var, value="mp3").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self.playlist_download_tab, text="M4A", variable=self.format_var, value="m4a").grid(row=1, column=1)
        tk.Radiobutton(self.playlist_download_tab, text="WAV", variable=self.format_var, value="wav").grid(row=1, column=1, sticky="e")

        # Download location section
        tk.Label(self.playlist_download_tab, text="Destination:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.playlist_download_location_entry = tk.Entry(self.playlist_download_tab, textvariable=self.outdir_var, width=40)
        self.playlist_download_location_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.playlist_download_tab, text="Browse", command=lambda: self.browse_folder(self.playlist_download_location_entry)).grid(row=2, column=2, padx=5)

        # Download and Exit buttons
        tk.Button(self.playlist_download_tab, text="Download", width=10, command=self.download_playlist).grid(row=3, column=1, sticky="w", pady=10)
        tk.Button(self.playlist_download_tab, text="Exit", width=10, command=self.root.destroy).grid(row=3, column=1, sticky="e", pady=10)

    def download_video(self):
        """ Download a video

        Arguments:
            self - object - This object

        Returns:
            None
        """

        # Update download location and format within the download manager object
        self.download_manager.outdir = self.outdir_var.get()
        self.download_manager.preferred_format = self.format_var.get()

        # Set status message and begin download
        self.status_message.set("Starting video download thread...")
        self.root.update_idletasks()
        self.download_manager.download_video(self.url_var.get())
        self.status_message.set("...Done! Thread started!")

        # Clear the URL field
        self.video_url_entry.delete(0, tk.END)
        self.video_url_entry.insert(0, "")

    def download_playlist(self):
        """ Download a playlist

        Arguments:
            self - object - This object

        Returns:
            None
        """

        # Update download location and format within the download manager object
        self.download_manager.outdir = self.outdir_var.get()
        self.download_manager.preferred_format = self.format_var.get()

        # Set status message and begin download
        self.status_message.set("Starting playlist download thread...")
        self.root.update_idletasks()
        self.download_manager.download_playlist(self.url_var.get())
        self.status_message.set("...Done! Thread started!")

        # Clear the URL field
        self.playlist_url_entry.delete(0, tk.END)
        self.playlist_url_entry.insert(0, "")

    def browse_folder(self, entry):
        """ Choose a folder to download to

        Arguments:
            self - object - This object
            entry - Tkinter Entry object - Entry for the download location

        Returns:
            None
        """
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry.delete(0, tk.END)
            entry.insert(0, folder_selected)

    def paste_clipboard(self, entry):
        """ Paste URL from clipboard

        Arguments:
            self - object - This object
            entry - Tkinter Entry object - Entry for the URL field

        Returns:
            None
        """

        try:
            entry.delete(0, tk.END)
            entry.insert(0, self.root.clipboard_get())
        except tk.TclError:
            messagebox.showerror("Error", "Clipboard is empty or invalid!")

