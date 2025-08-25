"""
lib/download.py

Handle downloads
"""

import os
import sys
import threading
import yt_dlp

class DownloadThread(object):
    """ Represents video and playlist download threads

    Methods:
        __init__() - Initialize the object
        progress_hook() - Progress tracking hook for yt_dlp
    """

    def __init__(self, thread_object, thread_type, url, dl_opts):
        """ Initialize the object

        Arguments:
            self - object - This object
            thread_object - Thread object - Active Thread object instance
            thread_type - string - Type of download thread, either 'video' or 'playlist'
            url - string - URL to the video or playlist the thread is downloading from YouTube
            dl_opts - dictionary - Download options passed to yt_dlp upon download

        Returns:
            None
        """

        # Store arguments locally
        self.thread_object = thread_object
        self.thread_type = thread_type
        self.url = url
        self.dl_opts = dl_opts

        # Initialize the download status
        self.status = {
            "status": "queued"
        }

    def progress_hook(self, download_status):
        """ Progress tracking hook for yt_dlp

        Arguments:
            self - object - This object
            download_status - dictionary - Progress message from yt_dlp

        Returns:
            None
        """

        # Update the download status
        self.status = download_status

class DownloadManager(object):
    """ Handle downloads of videos and playlists

    Methods:
        __init__() - Initialize the object
        download_video() - Download a video
        download_playlist() - Download a playlist
        download_statuses() - Return the progress of all downloads
    """

    def __init__(self, debug, config):
        """ Initialize the object

        Arguments:
            self - object - This object
            debug - boolean - Enable/disble debugging output
            config - ConfigParser object - Readable configuration file data

        Returns:
            None
        """

        # Store arguments locally
        self.debug = debug
        self.config = config

        # Extract some values from the configuration file
        self.outdir = self.config["DEFAULT"]["download_location"]
        self.preferred_format = self.config["DEFAULT"]["preferred_format"]

        # Initialize some empty lists to hold download threads
        self.download_threads = []

    def download_video(self, video_url):
        """ Download a video

        Arguments:
            self - object - This object
            video_url - string - YouTube video URL

        Returns:
            download_path - filepath - Path to the download
        """

        def progress_hook(download_status):
            """ Progress tracking hook for yt_dlp
            """
            download_thread.progress_hook(download_status)

        def download(dl_opts, video_url):
            """ Download thread
            """

            # Begin video download
            with yt_dlp.YoutubeDL(dl_opts) as downloader:
                downloader.download([video_url])

        # Expand outdir if necessary
        if "~" in self.outdir:
            self.outdir = os.path.expanduser(self.outdir)

        # Specify the download options
        dl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(self.outdir, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": self.preferred_format,
                "preferredquality": "192"
            }],
            "noplaylist": True,
            "progress_hooks": [progress_hook]
        }

        # Create a new child thread for the download
        new_thread = threading.Thread(target=download, args=(dl_opts, video_url))

        # Create a new DownloadThread object for the new thread and add it to the object's download thread list
        download_thread = DownloadThread(new_thread, "video", video_url, dl_opts)
        self.download_threads.append(download_thread)

        # Start the thread
        new_thread.start()


    def download_playlist(self, playlist_url):
        """ Download a playlist

        Arguments:
            self - object - This object
            playlist_url - string - YouTube playlist URL

        Returns:
            download_path - Dirpath to the directory containing the downloads
        """

        def progress_hook(download_status):
            """ Progress tracking hook for yt_dlp
            """
            download_thread.progress_hook(download_status)

        def download_thread(dl_opts, playlist_url):
            """ Download thread
            """

            # Begin playlist download
            with yt_dlp.YoutubeDL(dl_opts) as downloader:
                downloader.download([playlist_url])

        # Expand outdir if necessary
        if "~" in self.outdir:
            self.outdir = os.path.expanduser(self.outdir)

        # Specify the download options
        dl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(self.outdir, "%(uploader)s - %(playlist_title)s/%(playlist_index)s. %(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": self.preferred_format,
                "preferredquality": "192"
            }],
            "noplaylist": False,
            "progress_hooks": [progress_hook]
        }

        # Create a new child thread for the download
        new_thread = threading.Thread(target=download_thread, args=(dl_opts, playlist_url))

        # Create a new DownloadThread object for the new thread and add it to the object's download thread list
        download_thread = DownloadThread(new_thread, "playlist", playlist_url, dl_opts)
        self.download_threads.append(download_thread)

        # Start the thread
        new_thread.start()

    def get_statuses(self):
        """ Return the progress of all downloads

        Arguments:
            self - object - This object

        Returns:
            video_downloads - list - Status of all video downloads
            playlist_downloads - list - Status of all playlist downloads
        """

        # Initialize lists for video and playlist downloads respectively
        video_downloads = []
        playlist_downloads = []

        # Loop through the list of download threads and sort them by type
        for download_thread in self.download_threads:
            if download_thread.thread_type == "video":
                video_downloads.append((download_thread.url, download_thread.status))
            elif download_thread.thread_type == "playlist":
                playlist_downloads.append((download_thread.url, download_thread.status))
            else:
                raise Exception("Error! Invalid thread_type for DownloadThread object!")

        # Return the list of statuses
        return video_downloads, playlist_downloads


