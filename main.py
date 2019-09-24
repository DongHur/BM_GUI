import numpy as np
import sqlite3
import sys
import os
import pandas as pd
import atexit

from PyQt5.QtCore import QTimer, QDir, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QShortcut, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from UI.Ui_MainWindow import Ui_MainWindow

from widgets.tsne_Graph import tsne_Graph
from widgets.Behavior_Table import Behavior_Table
from widgets.Total_Canvas import Total_Canvas

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
        self.setup_connection()
        self.setup_shortcut()
        self.show()
    def setup_data(self):
        # Parse Main Data
        self.BM_Main_Path = os.getcwd()+"/BM_MAIN_DATA.h5"
        self.Main_Store = pd.HDFStore(self.BM_Main_Path)
        if '/main' in self.Main_Store.keys():
            # load main frame if it exist
            self.main_df = self.Main_Store['main']
            print(self.main_df)
        else:
            # create main frame if it doesn't exist
            self.main_df = pd.DataFrame(columns=['folder_key', 'num_frames', 'folder_path'])
            self.Main_Store.put(key='main', value=self.main_df)
        # get behavior table
        if '/behavior' in self.Main_Store.keys():
            self.beh_df = self.Main_Store['behavior']
            print(self.beh_df)
        else:
            self.beh_df = pd.DataFrame(
                columns=['folder_key', 'behavior', 'start_fr', 'stop_fr', 'comment'])
            self.Main_Store.put(key='behavior', value=self.beh_df)
        # get behaivor key table
        if '/behavior_key' in self.Main_Store.keys():
            # load behavior frame if it exist
            self.beh_key_df = self.Main_Store['behavior_key']
            print(self.beh_key_df)
        else:
            # create behavior frame if it doesn't exist
            self.beh_key_df = pd.DataFrame(columns=['behavior'])
            self.Main_Store.put(key='behavior_key', value=self.beh_key_df)
        print(":: finished updating database")
        # append total density plot
        self.TotDensityCanvas = Total_Canvas()
        self.Label_Population_Layout.addWidget(self.TotDensityCanvas)
        self.setup_tot_plot()
        pass
    def setup_tab(self):
        self.DataTab = Data_Tab(self)
        self.LabelTab = Label_Tab(self)
        self.BehaviorsTab = Behaviors_Tab(self)
        self.PreviewTab = Preview_Tab(self)
        pass
    def setup_connection(self):
        self.actionSave.triggered.connect(self.save_app)
        self.Label_Population_ComboBox.activated.connect(self.update_tot_plot)
        pass
    def setup_shortcut(self):
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self.centralwidget, self.save_app)
        pass
    def setup_tot_plot(self):
        tot_dir = self.main_df['folder_path'].to_numpy()
        self.TotDensityCanvas.setup_canvas(tot_dir=tot_dir)
        pass
    def update_behavior_tabs(self):
        self.BehaviorsTab.setup()
        self.PreviewTab.update_widgets()
        pass
    def update_tot_plot(self):
        Label_Population_Mode = self.Label_Population_ComboBox.currentText()
        if Label_Population_Mode == "HDBSCAN Cluster":
            self.TotDensityCanvas.update_canvas(mode="HDBSCAN Cluster")
        elif Label_Population_Mode == "Density":
            self.TotDensityCanvas.update_canvas(mode="Density")
        else:
            print(":: No Total tSNE Plot Mode")
        pass
    def save_app(self):
        # save app data
        print(":: SAVING ALL DATA")
        print(self.main_df)
        print(self.beh_df)
        print(self.beh_key_df)
        self.Main_Store.put(key='main', value=self.main_df)
        self.Main_Store.put(key='behavior', value=self.beh_df)
        self.Main_Store.put(key='behavior_key', value=self.beh_key_df)

def close():
    # verify if user wants to delete
    choice = QMessageBox.question(None, 'Save Data?',"Do you want to save your work?",
        QMessageBox.Yes | QMessageBox.No)
    if choice == QMessageBox.Yes:
        mainWin.save_app()
    pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    atexit.register(close)
    sys.exit(app.exec_())
