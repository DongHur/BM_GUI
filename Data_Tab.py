import sqlite3
import os
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

class Data_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.setup_connection()
        self.setup()
    def setup(self):
        for row_idx in range(len(self.parent.main_df)):
            self.add_row(
                FolderKey=self.parent.main_df.loc[row_idx,'folder_key'], 
                NumFrames=self.parent.main_df.loc[row_idx,'num_frames'], 
                FolderPath=self.parent.main_df.loc[row_idx,'folder_path']
            )
        pass
    def setup_connection(self):
        self.parent.Data_Import_Button.clicked.connect(self.import_data_clicked)
        pass
    def import_data_clicked(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())
        if folder:
            for (dirpath, dirnames, filenames) in os.walk(folder):
                # extact proper file types
                npy_files = list(filter(lambda x: '.npy' in x, filenames))
                h5_files = list(filter(lambda x: '.h5' in x, filenames))
                fig_files = list(filter(lambda x: '.fig' in x, filenames))
                if len(npy_files)==0 or len(h5_files)==0 or len(fig_files)==0:
                    continue
                # extract proper data from specifc files
                FolderKey = os.path.basename(dirpath)
                NumFrames = 100000
                FolderPath = dirpath
                self.add_row(FolderKey, NumFrames, FolderPath)
                # save data to main dataframe
                self.parent.main_df = self.parent.main_df.append(
                    {'folder_key':FolderKey, 'num_frames': NumFrames,'folder_path': dirpath}, 
                    ignore_index=True
                )
                # print(dirnames)
                # print(filenames)
                # print(npy_files)
                # print(h5_files)
                # print(fig_files)
                # print()
            print(self.parent.main_df)
            # self.con = sqlite3.connect(filepath)
            # cur = self.con.cursor()
            # cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            # beh_list = np.array(cur.fetchall()).flatten()
            # print("BEHAVIORS: ", beh_list)
        else:
            print('FILE DOES NOT EXIST')
    def add_row(self, FolderKey, NumFrames, FolderPath):
        # FolderKey - string; NumFrames - int; FolderPath - string
        row_idx = self.parent.Data_Table.rowCount()
        self.parent.Data_Table.insertRow(row_idx)
        self.parent.Data_Table.setItem(row_idx, 0, QTableWidgetItem(FolderKey))
        self.parent.Data_Table.setItem(row_idx, 1, QTableWidgetItem(str(NumFrames)))
        self.parent.Data_Table.setItem(row_idx, 2, QTableWidgetItem(FolderPath))
        pass
