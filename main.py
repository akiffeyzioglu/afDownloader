import os
import sys

import pytube
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pytube import Stream

font = QFont("Century Gothic", 20)
label = QFont("Century Gothic", 13)
clearButtonFont = QFont("Century Gothic", 10)

class Main(QWidget):

     def __init__(self):
        super().__init__()
        self.filesize = 0
        self.setWindowTitle("afDownloader")
        self.setGeometry(200, 200, 700, 330)
        self.setFixedSize(700,330)
        self.setWindowIcon(QIcon('./assets/youtube-dl-gui.png'))

        self.content()
        self.center()
        self.show()
        
     def content(self):
        # Single Video
        videoText = QLabel("Video Link:", self)
        videoText.move(20,45)
        videoText.setFont(font)
        
        self.videoLink = QLineEdit(self)
        self.videoLink.setGeometry(160,40,400,50)
        self.videoLink.setFont(font)

        self.pbarVideo = QProgressBar(self)
        self.pbarVideo.setGeometry(400,7,200,25)

        self.pbarVideoLabel = QLabel("Progress Bar:", self)
        self.pbarVideoLabel.move(290,7)
        self.pbarVideoLabel.resize(100,20)
        self.pbarVideoLabel.setFont(label)

        downloadButton = QPushButton("", self)
        downloadButton.setGeometry(630,40,50,30)
        downloadButton.clicked.connect(self.videoDownload)
        downloadButton.setIcon(QIcon('./assets/cloud_download_32px.png'))

        chooseDirectory = QPushButton("", self)
        chooseDirectory.setGeometry(575,40,50,30)
        chooseDirectory.setIcon(QIcon('./assets/folder_32px.png'))
        chooseDirectory.clicked.connect(self.chooseDirVideo)

        clearData = QPushButton("Clear Video Data", self)
        clearData.setGeometry(575,75,105,30)
        clearData.clicked.connect(self.clearVideoData)
        clearData.setFont(clearButtonFont)

        self.videoDownloadAlert = QLabel("", self)
        self.videoDownloadAlert.move(600,7)
        self.videoDownloadAlert.resize(50,20)
        self.videoDownloadAlert.setFont(label)

        self.chooseDirVideoLabel = QLabel("", self)
        self.chooseDirVideoLabel.move(20,90)
        self.chooseDirVideoLabel.resize(500,40)
        self.chooseDirVideoLabel.setFont(label)

        # Playlist 
        playlistText = QLabel("Playlist Link:", self)
        playlistText.move(20,200)
        playlistText.setFont(font)
        
        self.playListLink = QLineEdit(self)
        self.playListLink.setGeometry(170,190,400,50)
        self.playListLink.setFont(font)

        self.pbarPlayList = QProgressBar(self)
        self.pbarPlayList.setGeometry(400,155,200,25)

        self.pbarVideoLabel = QLabel("Progress Bar:", self)
        self.pbarVideoLabel.move(290,155)
        self.pbarVideoLabel.resize(100,20)
        self.pbarVideoLabel.setFont(label)

        downloadButton1 = QPushButton("", self)
        downloadButton1.setGeometry(640,190,50,30)
        downloadButton1.setIcon(QIcon('./assets/cloud_download_32px.png'))
        downloadButton1.clicked.connect(self.playListDownload)

        chooseDirectory1 = QPushButton("", self)
        chooseDirectory1.setGeometry(580,190,50,30)
        chooseDirectory1.setIcon(QIcon('./assets/folder_32px.png'))
        chooseDirectory1.clicked.connect(self.chooseDirPlaylist)

        clearPlayListDataButton = QPushButton("Clear Playlist Data", self)
        clearPlayListDataButton.setGeometry(580,225,110,30)
        clearPlayListDataButton.clicked.connect(self.clearPlayListData)
        clearPlayListDataButton.setFont(clearButtonFont)

        self.playListDownloadAlert = QLabel("", self)
        self.playListDownloadAlert.move(600, 160)
        self.playListDownloadAlert.resize(50,20)
        self.playListDownloadAlert.setFont(label)
       
        self.chooseDirPlayListLabel = QLabel("", self)
        self.chooseDirPlayListLabel.move(20,250)
        self.chooseDirPlayListLabel.resize(500,40)
        self.chooseDirPlayListLabel.setFont(label)

     def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
     
     def clearVideoData(self):
        self.videoDownloadAlert.setText("")
        self.chooseDirVideoLabel.setText("")
        self.videoLink.setText("")
        self.pbarVideo.setValue(0)
     
     def clearPlayListData(self):
         self.playListDownloadAlert.setText("")
         self.chooseDirPlayListLabel.setText("")
         self.playListLink.setText("")
         self.pbarPlayList.setValue(0)

     def chooseDirVideo(self):
        self.videoDir = QFileDialog.getExistingDirectory(os.getenv("Desktop"))
        if self.videoDir:
            self.chooseDirVideoLabel.setText(f"Directory selected: {self.videoDir}")
        else:
            self.chooseDirVideoLabel.setText("Directory not selected.")
     
     def chooseDirPlaylist(self):
        self.playListDir = QFileDialog.getExistingDirectory(os.getenv("Desktop"))
        if self.playListDir:
            self.chooseDirPlayListLabel.setText(f"Directory selected: {self.playListDir}")
        else:
            self.chooseDirPlayListLabel.setText("Directory not selected.")
      
     def on_progressVideo(self, stream=None, chunk=None, remaining=None):
        bytes_received = self.filesize - remaining
        percent = round(100.0 * bytes_received / float(self.filesize), 1)
        self.pbarVideo.setValue(int(percent))
    
     def on_progressPlayList(self, stream=None, chunk=None, remaining=None):
        bytes_received = self.filesize - remaining
        percent = round(100.0 * bytes_received / float(self.filesize), 1)
        self.pbarPlayList.setValue(int(percent))

     def videoDownload(self):
         self.link = self.videoLink.text()

         youtube = pytube.YouTube(self.link, on_progress_callback=self.on_progressVideo)
         video = youtube.streams.get_highest_resolution()
         self.filesize = video.filesize
         video.download(self.videoDir + "/")
         self.videoDownloadAlert.setText("Done!")

     def playListDownload(self):
        self.playList = self.playListLink.text()
        youtube_playlist = pytube.Playlist(self.playList)

        for playlist in youtube_playlist:
                video = pytube.YouTube(playlist, on_progress_callback=self.on_progressPlayList)
                stream = video.streams.get_highest_resolution()
                self.filesize = stream.filesize
                stream.download(self.playListDir + "/")
                self.playListDownloadAlert.setText("Done!")
             
if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    app = Main()
    sys.exit(uygulama.exec_())