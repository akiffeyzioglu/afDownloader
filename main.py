import os
import sys

import pytube
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pytube import Stream

font = QFont("Century Gothic", 20)
label = QFont("Century Gothic", 13)
buttonFont = QFont("Century Gothic", 10)

keyList = ["@","#","₺", "_","&","-","+","(",")","/","*","'",":",";","!","?","~","`","|","•","√","π","÷","×","¶","∆","¢","^","=","{","}","%","©","®","™","✓"," ",'"']

class Main(QWidget):

     def __init__(self):
        super().__init__()
        self.filesize = 0
        self.setWindowTitle("afDownloader")
        self.setGeometry(200, 200, 800, 400)
        self.setFixedSize(800,400)
        self.setWindowIcon(QIcon('./assets/youtube-dl-gui.png'))

        # Background color palatte 
        self.setAutoFillBackground(True)
        defaultColorPalette = self.palette()
        # Set default background color
        defaultColorPalette.setColor(self.backgroundRole(), Qt.cyan)
        self.setPalette(defaultColorPalette)

        self.content()
        self.center()
        self.show()
        
     def content(self):
        # Single Video
        videoText = QLabel("Video Link:", self)
        videoText.move(15,45)
        videoText.setFont(font)
        
        self.videoLink = QLineEdit(self)
        self.videoLink.setGeometry(190,40,460,50)
        self.videoLink.setFont(font)

        self.pbarVideo = QProgressBar(self)
        self.pbarVideo.setGeometry(450,7,200,25)

        self.pbarVideoLabel = QLabel("Progress Bar:", self)
        self.pbarVideoLabel.move(320,7)
        self.pbarVideoLabel.resize(120,20)
        self.pbarVideoLabel.setFont(label)

        videoDownloadButton = QPushButton("", self)
        videoDownloadButton.setGeometry(730,40,60,30)
        videoDownloadButton.clicked.connect(self.videoDownload)
        videoDownloadButton.setIcon(QIcon('./assets/cloud_download_32px.png'))

        chooseVideoDirectory = QPushButton("", self)
        chooseVideoDirectory.setGeometry(665,40,60,30)
        chooseVideoDirectory.setIcon(QIcon('./assets/folder_32px.png'))
        chooseVideoDirectory.clicked.connect(self.chooseDirVideo)

        clearData = QPushButton("Clear Video Data", self)
        clearData.setGeometry(665,75,125,30)
        clearData.clicked.connect(self.clearVideoData)
        clearData.setFont(buttonFont)

        self.videoInfoText = QLabel("", self)
        self.videoInfoText.move(15,110)
        self.videoInfoText.resize(700,50)
        self.videoInfoText.setFont(label)
        
        self.videoSearchButton = QPushButton("Search",self)
        self.videoSearchButton.setGeometry(665,110,125,30)
        self.videoSearchButton.setFont(label)
        self.videoSearchButton.clicked.connect(self.searchVideo)

        self.videoDownloadAlert = QLabel("", self)
        self.videoDownloadAlert.move(665,7)
        self.videoDownloadAlert.resize(50,20)
        self.videoDownloadAlert.setFont(label)

        self.chooseDirVideoLabel = QLabel("", self)
        self.chooseDirVideoLabel.move(15,90)
        self.chooseDirVideoLabel.resize(700,40)
        self.chooseDirVideoLabel.setFont(label)
        
        #download file type
        self.fileType = QComboBox(self)
        self.fileType.addItem("MP4")
        self.fileType.addItem("MP3")
        self.fileType.setGeometry(190,5,100,30)
        self.fileType.setFont(buttonFont)

        # Playlist 
        playlistText = QLabel("Playlist Link:", self)
        playlistText.move(15,200)
        playlistText.setFont(font)
        
        self.playListLink = QLineEdit(self)
        self.playListLink.setGeometry(190,190,460,50)
        self.playListLink.setFont(font)

        self.pbarPlayList = QProgressBar(self)
        self.pbarPlayList.setGeometry(450,155,200,25)

        self.pbarVideoLabel = QLabel("Progress Bar:", self)
        self.pbarVideoLabel.move(320,155)
        self.pbarVideoLabel.resize(120,20)
        self.pbarVideoLabel.setFont(label)
        
        self.playListInfoText = QLabel("", self)
        self.playListInfoText.move(15,260)
        self.playListInfoText.resize(700,85)
        self.playListInfoText.setFont(label)
        
        self.playListsearchButton = QPushButton("Search",self)
        self.playListsearchButton.setGeometry(665,260,125,30)
        self.playListsearchButton.setFont(label)
        self.playListsearchButton.clicked.connect(self.searchPlaylist)
 
        playListDownloadButton = QPushButton("", self)
        playListDownloadButton.setGeometry(730,190,60,30)
        playListDownloadButton.setIcon(QIcon('./assets/cloud_download_32px.png'))
        playListDownloadButton.clicked.connect(self.playListDownload)

        choosePlayListDirectory = QPushButton("", self)
        choosePlayListDirectory.setGeometry(665,190,60,30)
        choosePlayListDirectory.setIcon(QIcon('./assets/folder_32px.png'))
        choosePlayListDirectory.clicked.connect(self.chooseDirPlaylist)

        clearPlayListDataButton = QPushButton("Clear Playlist Data", self)
        clearPlayListDataButton.setGeometry(665,225,125,30)
        clearPlayListDataButton.clicked.connect(self.clearPlayListData)
        clearPlayListDataButton.setFont(buttonFont)

        self.playListDownloadAlert = QLabel("", self)
        self.playListDownloadAlert.move(665, 160)
        self.playListDownloadAlert.resize(50,20)
        self.playListDownloadAlert.setFont(label)
       
        self.chooseDirPlayListLabel = QLabel("", self)
        self.chooseDirPlayListLabel.move(15,250)
        self.chooseDirPlayListLabel.resize(700,40)
        self.chooseDirPlayListLabel.setFont(label)

        # Color button section
        changeColorButton = QPushButton("Change Background Color", self)
        changeColorButton.setGeometry(590,350,200,30)
        changeColorButton.setFont(buttonFont)
        changeColorButton.clicked.connect(self.paintBackground)

     def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
     
     def paintBackground(self):
        self.setAutoFillBackground(True)
        colorPalette = self.palette()

        color = QColorDialog.getColor()
        colorPalette.setColor(self.backgroundRole(), color)
        self.setPalette(colorPalette)

     def clearVideoData(self):
        self.videoDownloadAlert.setText("")
        self.chooseDirVideoLabel.setText("")
        self.videoLink.setText("")
        self.pbarVideo.setValue(0)
        self.videoInfoText.setText("")
     
     def clearPlayListData(self):
         self.playListDownloadAlert.setText("")
         self.chooseDirPlayListLabel.setText("")
         self.playListLink.setText("")
         self.pbarPlayList.setValue(0)
         self.playListInfoText.setText("")

     def chooseDirVideo(self):
        self.videoDir = QFileDialog.getExistingDirectory(os.getenv("Desktop"))
        if self.videoDir:
            self.chooseDirVideoLabel.setText(f"Dir: {self.videoDir}")
        else:
            self.chooseDirVideoLabel.setText("Directory not selected.")
     
     def chooseDirPlaylist(self):
        self.playListDir = QFileDialog.getExistingDirectory(os.getenv("Desktop"))
        if self.playListDir:
            self.chooseDirPlayListLabel.setText(f"Dir: {self.playListDir}")
        else:
            self.chooseDirPlayListLabel.setText("Directory not selected.")
      
     def on_progressVideo(self,streams = None, chunk=None, remaining=None):
        bytes_received = self.filesize - remaining
        percent = round(100.0 * bytes_received / float(self.filesize), 1)
        self.pbarVideo.setValue(int(percent))
    
     def on_progressPlayList(self, stream=None, chunk=None, remaining=None):
        bytes_received = self.filesize - remaining
        percent = round(100.0 * bytes_received / float(self.filesize), 1)
        self.pbarPlayList.setValue(int(percent))

     def videoDownload(self):
          try:
          	self.link = self.videoLink.text()
          	
          	if self.fileType.currentText() == "MP4":
          		youtube = pytube.YouTube(self.link, on_progress_callback=self.on_progressVideo)
          		video = youtube.streams.get_highest_resolution()
          		self.filesize = video.filesize
          		video.download(self.videoDir + "/")
          		self.videoDownloadAlert.setText("Done!")
          		
          	elif self.fileType.currentText() == "MP3":
          		youtube = pytube.YouTube(self.link,on_progress_callback=self.on_progressVideo)
          		music=youtube.streams.filter(only_audio = True).first()
          		self.filesize = music.filesize
          		
          		fileNameTitle = ""
          		
          		for i in youtube.title:
          			if i in keyList:
          				continue
          				
          			else:
          				fileNameTitle += i
          		
          		music.download(self.videoDir + "/",filename = fileNameTitle)
          		
          		mp4File = self.videoDir + "/"+ fileNameTitle+".mp4"
          		mp3File = self.videoDir + "/"+ fileNameTitle+".mp3"          
          		
          		self.videoDownloadAlert.setText("Done!")
          		os.rename(mp4File,mp3File)
  	        
          except:
          	if self.videoLink.text() == "":
     	    		self.errorMessage = QMessageBox.warning(self,"Error","Please Write A Video Url")
     	    		
     	    	else:
     	    		self.errorMessage = QMessageBox.warning(self,"Error","Video Not Found")
         
     def searchVideo(self):
     	try:
	     	self.search = self.videoLink.text()
	     	self.videoInfo = pytube.YouTube(self.search)
	     	self.videoTitle = self.videoInfo.title
	     	
	     	if self.fileType.currentText() == "MP4":
	     			     	video = self.videoInfo.streams.get_highest_resolution()
	     			     	self.filesize = video.filesize
	     			     	
	     			     	self.videoInfoText.setText("Video Title: " + self.videoTitle+"\nFile Size: "+str(round((self.filesize/1048576),2))+" MB")
	     	elif self.fileType.currentText() == "MP3":
	     		music=self.videoInfo.streams.filter(only_audio = True).first()
	     		self.filesize = music.filesize
	     		self.videoInfoText.setText("Video Title: " + self.videoTitle+"\nFile Size: "+str(round((self.filesize/1048576),2))+" MB")
     	
     	except:
     	    	if self.videoLink.text() == "":
     	    		self.errorMessage = QMessageBox.warning(self,"Error","Please Write A Video Url")
     	    		
     	    	else:
     	    		self.errorMessage = QMessageBox.warning(self,"Error","Video Not Found")
          	
     def searchPlaylist(self):
      	try:
      		self.search = self.playListLink.text()
      		self.playListInfo = pytube.Playlist(self.search)
      		self.playlistTitle = self.playListInfo.title
      		self.playListInfoText.setText("Playlist Title: " + self.playlistTitle)
      		
      		self.fileSize = 0
      		self.videoSize = 0
      		
      		for playlist in self.playListInfo:
      			
      			video = pytube.YouTube(playlist)
      			video = video.streams.get_highest_resolution()
      			self.filesize += video.filesize
      			self.videoSize += 1
      			
      		self.playListInfoText.setText("PlayList Title: " + self.playlistTitle+"\nFile Size: "+str(round((self.filesize/1048576),2))+" MB\n"+str(self.videoSize)+" Video")
      			
      	except:
      	   		if self.videoLink.text() == "":
      	   			self.errorMessage = QMessageBox.warning(self,"Error","Please Write A Playlist Url")
      	   			
      	   		else:
      	   			self.errorMessage = QMessageBox.warning(self,"Error","Playlist Not Found!")
     	
     def playListDownload(self):
         try:
         	self.playList = self.playListLink.text()
         	youtube_playlist = pytube.Playlist(self.playList)
         	
         	self.lengList = str(len(youtube_playlist))
         	self.downloadList = 0
         	
         	
         	for playlist in youtube_playlist:
         	       self.playListDownloadAlert.setText(str(self.downloadList)+"/"+self.lengList+" Done")
         	       video = pytube.YouTube(playlist, on_progress_callback=self.on_progressPlayList)
         	       stream = video.streams.get_highest_resolution()
         	       self.filesize = stream.filesize
         	       stream.download(self.playListDir + "/")
         	       self.downloadList += 1
         	       
         	self.playListDownloadAlert.setText(str(self.downloadList)+"/"+self.lengList+" Done")
         	self.downloadList = 0
	         
         except:
          		if self.videoLink.text() == "":
          			self.errorMessage = QMessageBox.warning(self,"Error","Please Write A Playlist Url")
          			
          		else:
          		 self.errorMessage = QMessageBox.warning(self,"Error","Playlist Not Found")
             
if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    app = Main()
    sys.exit(uygulama.exec_())
   