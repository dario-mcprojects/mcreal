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
from PyQt5 import uic
from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QIcon

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
    def __init__(self, msg):
        super().__init__()
        uic.loadUi('src/msg.ui', self)  # ui file load

        # - Theme system
        self.theme_index = 0
        #self.__theme_change()
        self.shstyle = _get_converted_stylesheet(self.theme_index)
        self.setStyleSheet(self.shstyle)
        #

        # - Set text
        self.label_msg.setText(msg)
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

        # - Set titlebar name
        self.titlebar_title.setText('Minecraft MC-Real Modpack Installer')
        #
        
        # - Set button functionality
        self.quit_button.clicked.connect(self.close) # Title bar close button
        self.btn_ok.clicked.connect(self.close) # Ok button close button
        #

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp('sex')
    appMain.show()
    style = _get_converted_stylesheet(appMain.theme_index)
    appMain.setStyleSheet(style)

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')