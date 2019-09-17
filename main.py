import numpy as np
import sqlite3
import sys
import os
import pandas as pd

from PyQt5.QtCore import QTimer, QDir, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QShortcut
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from UI.Ui_MainWindow import Ui_MainWindow

from widgets.tsne_Graph import tsne_Graph
# from widgets.density_Graph import density_Graph
from widgets.Behavior_Table import Behavior_Table

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from Data_Tab import Data_Tab
from Label_Tab import Label_Tab
from Behaviors_Tab import Behaviors_Tab
from Preview_Tab import Preview_Tab

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.BM_Main_Path = None
        self.Main_Store = None
        self.main_df = None
        self.BM_Behavior_Path = None
        self.Behavior_Store = None
        self.setupUi(self)
        self.setup_data()
        self.setup_tab()
        self.setup_shortcut()
        self.show()
    def setup_data(self):
        # Parse Main Data
        self.BM_Main_Path = os.getcwd()+"/BM_MAIN_DATA.h5"
        self.Main_Store = pd.HDFStore(self.BM_Main_Path, mode='a')
        if '/main' in self.Main_Store.keys():
            # load main frame if it exist
            self.main_df = self.Main_Store['main']
            print(self.main_df)
        else:
            # create main frame if it doesn't exist
            self.main_df = pd.DataFrame(columns=['folder_key', 'num_frames', 'folder_path'])
            self.Main_Store.put(key='main', value=self.main_df)
        
        # Parse Behavior Data
        self.BM_Behavior_Path = os.getcwd()+"/BM_BEHAVIOR_DATA.h5"
        self.Behavior_Store = pd.HDFStore(self.BM_Behavior_Path, mode='a')
        
        # TODO: add check up to see if this file exist in the first place in the main database
        # for row_idx in range(len(self.main_df)):
        #     if os.path.isdir(self.main_df.loc[row_idx, 'folder_path']):

        # TODO: create a tool function converting h5 (2D) to numpy array (3D)
        print(":: finished updating database")
        pass
    def setup_tab(self):
        self.DataTab = Data_Tab(self)
        self.LabelTab = Label_Tab(self)
        self.BehaviorsTab = Behaviors_Tab(self)
        # self.PreviewTab = Preview_Tab(self)
        pass
    def setup_shortcut(self):
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self.centralwidget, self.save_app)
        pass
    def save_app(self):
        # save app data
        print(":: SAVING ALL DATA")
        print(self.main_df)
        self.Main_Store.put(key='main', value=self.main_df)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
