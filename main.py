import os 
import sys
import time
import pytube
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

font = QFont("Century Gothic", 20)
label = QFont("Century Gothic", 13)
clearButtonFont = QFont("Century Gothic", 10)

class Main(QWidget):

     def __init__(self):
        super().__init__()

        self.setWindowTitle("afDownloader")
        self.setGeometry(200, 200, 700, 350)
        self.setFixedSize(700,350)
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
        self.videoDownloadAlert.move(600,20)
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
        self.playListDownloadAlert.move(600, 175)
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
        self.videoLink.clear()
     
     def clearPlayListData(self):
         self.playListDownloadAlert.setText("")
         self.chooseDirPlayListLabel.setText("")
         self.playListLink.setText("")

     def chooseDirVideo(self):
        self.videoDir = QFileDialog.getExistingDirectory(os.getenv("Desktop"))
        if self.videoDir:
            self.chooseDirVideoLabel.setText(f"Directory Selected: {self.videoDir}")
        """else:
            self.chooseDirVideoLabel.setText("Directory not Selected.")"""       
     
     def chooseDirPlaylist(self):
        self.playListDir = QFileDialog.getExistingDirectory(os.getenv("Desktop"))
        if self.playListDir:
            self.chooseDirPlayListLabel.setText(f"Directory Selected: {self.playListDir}")
        else:
            self.chooseDirPlayListLabel.setText("Directory not Selected.")
       
     def videoDownload(self):
         self.link = self.videoLink.text()

         youtube = pytube.YouTube(self.link)
         video = youtube.streams.get_highest_resolution()
         video.download(self.videoDir + "/")
         self.videoDownloadAlert.setText("Done!")

     def playListDownload(self):
        self.playList = self.playListLink.text()
        youtube_playlist = pytube.Playlist(self.playList)

        for playlist in youtube_playlist:
                video = pytube.YouTube(playlist)
                stream = video.streams.get_highest_resolution()
                stream.download(self.playListDir + "/")
                self.playListDownloadAlert.setText("Done!")
             
if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    app = Main()
    sys.exit(uygulama.exec_())