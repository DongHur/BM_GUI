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
        self.parent.Delete_Data_Button.clicked.connect(self.delete_row)
        pass
    def import_data_clicked(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())
        if folder:
            for (dirpath, dirnames, filenames) in os.walk(folder):
                # conditions to include data
                video_file = list(filter(lambda x: '.avi' in x, filenames))
                h5_file = list(filter(lambda x: '.h5' in x, filenames))
                cluster_file = list(filter(lambda x: 'cluster.npy' in x, filenames))
                embed_file = list(filter(lambda x: 'EMBED.mat' in x, filenames))
                # fig_files = list(filter(lambda x: '.fig' in x, filenames))
                if len(video_file)==0 or len(h5_file)==0 or len(cluster_file)==0 or len(embed_file)==0:
                    continue
                # extract proper data from specifc files
                FolderKey = os.path.basename(dirpath)
                NumFrames = np.load(dirpath+"/cluster.npy").shape[0]
                FolderPath = dirpath
                self.add_row(FolderKey, NumFrames, FolderPath)
                # save data to main dataframe
                self.parent.main_df = self.parent.main_df.append(
                    {'folder_key':FolderKey, 'num_frames': NumFrames,'folder_path': dirpath}, 
                    ignore_index=True
                )
            self.parent.LabelTab.update_widgets()
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
    def delete_row(self):
        indices = self.parent.Data_Table.selectionModel().selectedRows() 
        for index in sorted(indices, reverse=True):
            self.parent.Data_Table.removeRow(index.row())
            self.parent.main_df.drop(index.row(), inplace=True)
        self.parent.main_df.reset_index(drop=True, inplace=True)
        pass








