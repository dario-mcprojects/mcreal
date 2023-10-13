# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
# from PyQt5 import uic
# from PyQt5.QtGui import QIcon

# class MainApp(QMainWindow, QWidget):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("UI.FILE", self)  # ui file load
#         #self.setWindowIcon(QIcon("PATH_ICON"))  # Icon Loading

#         #self.BUTTON_NAME.clicked.connect(self.DEF)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     appMain = MainApp()
#     appMain.show()

#     try:
#         sys.exit(app.exec_())
#     except SystemExit:
#         print('Exiting...')

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsDropShadowEffect
from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QIcon

import os
import easygui
import threading
import urllib.request as request

from src import config as cfg
from src import msg_ui

from json import loads as jsn

# Debug mode
# is_Debug = True
#

# Loading config
# cfg = open('config.toml', 'r').read()
# cfg = tml(cfg)
#

# Loading theme list
theme_folder = 'src/themes/'

theme_list = open(theme_folder + 'list.json', 'r').read()
theme_list = jsn(theme_list)
#

# Adding shadow effect
shadow_effect = QGraphicsDropShadowEffect()
shadow_effect.setBlurRadius(5)
shadow_effect.setOffset(2, 2)
#

def _get_converted_stylesheet(theme_index):
    # Loading theme stylesheet
    f   = theme_list[theme_index]['file']
    vf  = theme_list[theme_index]['varfile']
    n   = theme_list[theme_index]['name']
    opt = theme_list[theme_index]['opt']

    if opt == "":
        o = False
    else:
        o = True
    
    print('Loading Theme: ' + n + " [{}]".format(f))
    if o:
        print('OPT: {}'.format(opt))

    varsf = open(theme_folder + vf, 'r').read()
    varsf = jsn(varsf)

    style = open(theme_folder + f, 'r').read()

    if o:
        style_opt = open(theme_folder + opt, 'r').read()
    
    for var in varsf: # Replacing vars in variable file
        style = style.replace(var, varsf[var])

        if o:
            style_opt = style_opt.replace(var, varsf[var])

    # if is_Debug:
    #     if o:
    #         open('STYLE.RESULT.--debug.css', 'w').write(style + "\n" + style_opt)
    #     else:
    #         open('STYLE.RESULT.--debug.css', 'w').write(style)

    if o:
        return style + "\n" + style_opt
    else:
        return style


class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/window.ui', self)  # ui file load

        # - Theme system
        self.theme_index = 0
        #self.__theme_change()
        #

        # - Set shadow effect
        self.frame.setGraphicsEffect(shadow_effect)
        #

        # - Set titlebar removing
        self.set_titlebar_transparent()
        #

        # - Set frame moving
        self.titlebar_frame.mouseMoveEvent = self.MoveWindow
        #

        # - Set label logo pixmap
        self.logo_img = QtGui.QPixmap('src/images/mcreal.png')
        self.pic_logo.setPixmap(self.logo_img)

        # - Set titlebar name
        self.titlebar_title.setText('Minecraft MC-Real Mod-pack Installer')
        #
        
        # - Set button functionality
        self.quit_button.clicked.connect(self.close) # Title bar close button
        #self.installbtn.clicked.connect(self._start_thread) # Install button start install thread
        self.installbtn.clicked.connect(self._test_out_progressbar)
        self.browse_dir.clicked.connect(self._browse_dir) # Install button browse file

        self.progressBar.hide()

        #


    def _test_out_progressbar(self):
        self.installbtn.hide()
        self.progressBar.show()
        x = threading.Thread(target=self._test_out_progressbar_thread)
        x.start()

    def _test_out_progressbar_thread(self):
        while True:
            if self.progressBar.value() >= 100:
                break
            self.progressBar.setValue(100)


    def __interactionManager(self, bool):
        self.frame.setEnabled(bool)

    def MoveWindow(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.isMaximized() == False:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
                pass

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        pass

    def set_titlebar_transparent(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setStyleSheet("background:transparent;")

    def _browse_dir(self):
        path = easygui.diropenbox(msg='Select Install Directory')

        if path == None or path == ' ':
            print('Cancelled')
            return
        
        self.installdir.setText(path)

    def _start_thread(self):
        x = threading.Thread(target=self.start_install)

        self.__interactionManager(False)

        x.start()

        x.join()
        self.open_msg_window('Finished Installation!')

    
    def start_install(self):
        if self.installdir.text() == '' or self.installdir.text() == ' ':
            self.__interactionManager(True)
            return
        
        save_dir = self.installdir.text() + "\\"
        save_loc = save_dir + '_tmp.download'

        #self.Download(save_loc)


        self.__interactionManager(True)
        #self.__interactionManager(True)
        pass

    def Handle_Progress(self, blocknum, blocksize, totalsize):
 
        ## calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(round(download_percentage))
            #QApplication.processEvents()
            print(download_percentage)
        
        if download_percentage >= 100:
            #self.progressBar.setValue(100)
            if download_percentage >= 200:
                self.progressBar.setValue(100)

 
    # method to download any file using urllib
    def Download(self, saveloc):
        # - Set Url to download
        down_url = cfg.download_link
        save_loc = saveloc

        # specify save location where the file is to be saved
        
        print('Save location: %s' % save_loc)

        # Downloading using urllib
        request.urlretrieve(down_url,save_loc, self.Handle_Progress)

    def open_msg_window(self, msg):
        self.msgUI = msg_ui.MainApp

        self.msgUI(msg).show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()
    style = _get_converted_stylesheet(appMain.theme_index)
    appMain.setStyleSheet(style)

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')