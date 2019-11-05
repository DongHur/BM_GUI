import numpy as np
import pandas as pd
import sys, os, atexit
from UI.Ui_MainWindow import Ui_MainWindow

#import pyqt tools
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QMessageBox,QFileDialog

# import tab pages
from Tab.Data_Tab import Data_Tab
from Tab.Label_Tab import Label_Tab
from Tab.Behaviors_Tab import Behaviors_Tab
from Tab.Preview_Tab import Preview_Tab

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.Main_Store = None
        self.main_df = None
        self.setupUi(self)
        self.setup_connection()
        self.setup_shortcut()
        self.show()
    
    # ***** exec function *****
    def setup_connection(self):
        self.actionNew.triggered.connect(self._new_app)
        self.actionSave.triggered.connect(self._save_app)
        self.actionOpen.triggered.connect(self._open_app)
        pass
    def setup_shortcut(self):
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self.centralwidget, self._save_app)
        pass
    
    # ***** helper function *****    
    def _new_app(self):
        data_path = QFileDialog.getSaveFileName(None, "New Data", os.getcwd()+"/BM.h5" ,"h5(BM.h5)")[0]
        if data_path != "":
            print(data_path)
            self.Main_Store = pd.HDFStore(data_path)
            # create main frame
            self.main_df = pd.DataFrame(columns=['folder_key', 'num_frames', 'folder_path'])
            self.Main_Store.put(key='main', value=self.main_df)
            # create behavior frame
            self.beh_df = pd.DataFrame(columns=['folder_key', 'behavior', 'start_fr', 'stop_fr', 'comment'])
            self.Main_Store.put(key='behavior', value=self.beh_df)
            # create behavior key frame
            self.beh_key_df = pd.DataFrame(columns=['behavior'])
            self.Main_Store.put(key='behavior_key', value=self.beh_key_df)
            # setup tab pages
            self.DataTab = Data_Tab(self)
            self.LabelTab = Label_Tab(self)
            self.BehaviorsTab = Behaviors_Tab(self)
            # self.PreviewTab = Preview_Tab(self)
            # save new app
            self._save_app()
        else:
            QMessageBox.warning(None,"warning","Select a valid 'BM.h5' file")
    def _save_app(self):
        if self.Main_Store != None:
            print(":: SAVING ALL DATA", self.main_df, self.beh_df, self.beh_key_df)
            self.Main_Store.put(key='main', value=self.main_df)
            self.Main_Store.put(key='behavior', value=self.beh_df)
            self.Main_Store.put(key='behavior_key', value=self.beh_key_df)
        else:
            QMessageBox.warning(None,"warning","Could not save the files")
    def _open_app(self):
        data_path = QFileDialog.getOpenFileName(None, "Select BM.h5", os.getcwd(), "h5 files (BM.h5)")[0]
        if data_path:
            self.Main_Store = pd.HDFStore(data_path)
            self.main_df = self.Main_Store['main'] # get main table
            self.beh_df = self.Main_Store['behavior'] # get behavior table
            self.beh_key_df = self.Main_Store['behavior_key'] # get behaivor key table
            # setup tab pages
            self.DataTab = Data_Tab(self)
            self.LabelTab = Label_Tab(self)
            self.BehaviorsTab = Behaviors_Tab(self)
            # self.PreviewTab = Preview_Tab(self)
        else:
            QMessageBox.warning(None,"warning","Select a valid 'BM.h5' file")

def close():
    # verify to save unsaved work
    choice = QMessageBox.question(None, 'Save Data?',"Do you want to save your work?",
        QMessageBox.Yes | QMessageBox.No)
    if choice == QMessageBox.Yes:
        mainWin._save_app()
    pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    atexit.register(close)
    sys.exit(app.exec_())
