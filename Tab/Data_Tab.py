import sqlite3
import os
import numpy as np
import pandas as pd
import scipy.io as sio

#import pyqt tools
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox

class Data_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.setup_connection()
        self.setup_table()
    
    # ***** exec function *****
    def setup_connection(self):
        self.parent.Data_Import_Button.clicked.connect(self.import_data_clicked)
        self.parent.Delete_Data_Button.clicked.connect(self.delete_row_clicked)
    def setup_table(self):
        for row_idx in range(len(self.parent.main_df)):
            self._add_row(
                FolderKey=self.parent.main_df.loc[row_idx,'folder_key'], 
                NumFrames=self.parent.main_df.loc[row_idx,'num_frames'], 
                FolderPath=self.parent.main_df.loc[row_idx,'folder_path'])
    
    # ***** event listener function *****
    def import_data_clicked(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())
        if folder:
            for (dirpath, dirnames, filenames) in os.walk(folder):
                # required files
                h5_file = list(filter(lambda x: '.h5' in x, filenames))
                embed_npy_file = self._format_embed_file(dirpath, filenames)
                if len(h5_file)==0  or len(embed_npy_file)==0: continue
                # extract data info
                FolderKey = os.path.basename(dirpath)
                NumFrames = np.load(embed_npy_file[0]).shape[0]
                FolderPath = dirpath
                self._add_row(FolderKey, NumFrames, FolderPath)
                # save data
                self.parent.main_df = self.parent.main_df.append(
                    {'folder_key':FolderKey, 'num_frames': NumFrames,'folder_path': dirpath}, 
                    ignore_index=True)
            # update label tab
            self.parent.LabelTab.update_widgets()
        else:
            QMessageBox.warning(None,"warning","Can't decipher your data directory. Make sure the data tree format is correct.")
    def delete_row_clicked(self):
        # verify if user wants to delete
        choice = QMessageBox.question(self.parent, 'Delete Rows',
            "Are you sure you want to delete these rows? \nWarning!",
            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            # delete rows
            indices = self.parent.Data_Table.selectionModel().selectedRows() 
            for index in sorted(indices, reverse=True):
                self.parent.Data_Table.removeRow(index.row())
                self.parent.main_df.drop(index.row(), inplace=True)
            self.parent.main_df.reset_index(drop=True, inplace=True)
    
    # ***** helper function *****   
    def _format_embed_file(self, dirpath, filenames):
        embed_npy_exist = len(list(filter(lambda x: 'EMBED.npy' in x, filenames))) != 0
        embed_mat_exist = len(list(filter(lambda x: 'EMBED.mat' in x, filenames))) != 0
        embed_npy_file = []
        # if .mat exist create .npy file
        if embed_npy_exist:
            embed_npy_file = [dirpath+"/EMBED.npy"]
        elif embed_mat_exist and not embed_npy_exist:
            np.save(dirpath+"/EMBED.npy", sio.loadmat(dirpath+"/EMBED.mat")['embed_values_i'])
            embed_npy_file = [dirpath+"/EMBED.npy"]
        return embed_npy_file
    def _add_row(self, FolderKey, NumFrames, FolderPath):
        # FolderKey - string; NumFrames - int; FolderPath - string
        row_idx = self.parent.Data_Table.rowCount()
        self.parent.Data_Table.insertRow(row_idx)
        self.parent.Data_Table.setItem(row_idx, 0, QTableWidgetItem(FolderKey))
        self.parent.Data_Table.setItem(row_idx, 1, QTableWidgetItem(str(NumFrames)))
        self.parent.Data_Table.setItem(row_idx, 2, QTableWidgetItem(FolderPath))








