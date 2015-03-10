import sys
import vlc
from PyQt4 import QtGui, QtCore
import ScoreMatrix as SM
import FindMusicFiles as FMF
import random as rd

icon_dir="/usr/share/icons/Mint-X/actions/24/"

class Player(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        #initiating list of songs
        self.initiate_songs_list()

        #initating score matrix
        self.score_matrix=SM.ScoreMatrix()

        #creating a basic vlc instance
        self.instance = vlc.Instance()
        #creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        #setting indexes of current and previous songs
        self.previous_song_index=-1
        self.listened_song_index=-1

        self.createUI()
        self.isPaused = False

    def initiate_songs_list(self):
        D=FMF.DocumentSearch()
        self.songs_list=D.get_song_files()

    def createUI(self):
        
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # Slider position
        self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        # PLay button
        self.hbuttonbox = QtGui.QHBoxLayout()
        self.playbutton = QtGui.QPushButton("Play")
        self.playbutton.setIcon(QtGui.QIcon(icon_dir+"media-playback-start.png"))
        self.hbuttonbox.addWidget(self.playbutton)
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),self.PlayPause)

        # Stop button
        self.stopbutton = QtGui.QPushButton("Stop")
        self.stopbutton.setIcon(QtGui.QIcon(icon_dir+"media-playback-stop.png"))
        self.hbuttonbox.addWidget(self.stopbutton)
        self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                     self.Stop)

        # Next button
        self.nextbutton=QtGui.QPushButton("Next")
        self.nextbutton.setIcon(QtGui.QIcon(icon_dir+"media-skip-forward.png"))
        self.hbuttonbox.addWidget(self.nextbutton)
        self.connect(self.nextbutton, QtCore.SIGNAL("clicked()"),self.Next)


        # Volume
        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        open = QtGui.QAction("&Open", self)
        self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def Play_random_song(self):
        index=rd.choice(range(0,len(self.songs_list)))
        self.listened_song_index=index
        self.OpenFile(self.songs_list[index])

    def PlayPause(self):
        """Toggle play/pause status
        """
        self.stop_will=False
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.playbutton.setIcon(QtGui.QIcon(icon_dir+"media-playback-start.png"))
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.Play_random_song()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.playbutton.setIcon(QtGui.QIcon(icon_dir+"media-playback-pause.png"))
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.stop_will=True
        self.playbutton.setText("Play")
        self.playbutton.setIcon(QtGui.QIcon(icon_dir+"media-playback-start.png"))
        self.score_matrix.save_score_matrix()

    def Next(self):
        """Select the next song
        """
        self.stop_will=False
        #une chanson a deja ete ecoutee
        if self.previous_song_index!=-1:
            self.previous_song_index=self.listened_song_index
            #calcul du pourcentage d'ecoute
            time_rate=0
            try:
                time_rate=self.mediaplayer.get_time()/self.media.get_duration()
            except:
                pass
            #actualisation du score de la matrix
            self.score_matrix.update_score(time_rate,self.listened_song_index,self.previous_song_index)
            #selectionne la musique suivante
            self.listened_song_index=self.score_matrix.select_score(self.listened_song_index)
            next_music=self.songs_list[self.listened_song_index]
            #lance la lecture de la musique suivante
            self.OpenFile(next_music)
            
        #on a passe la premiere chanson    
        else:
            self.previous_song_index=self.listened_song_index
            self.Play_random_song()

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File")
        if not filename:
            return

        # create the media
        self.media = self.instance.media_new((filename))
        # put the media in the media player
        self.mediaplayer.set_media(self.media)
        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))
        self.PlayPause()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the song finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                if self.stop_will:
                    self.Stop()
                else:
                    self.Next()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())