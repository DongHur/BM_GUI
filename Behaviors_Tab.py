import sqlite3
import os
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

class Behaviors_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.setup()
        self.setup_connection()
        
    def setup(self):
        (num_row, num_col) = self.parent.beh_df.shape
        for row_idx in range(num_row):
            self.add_row(
                FolderKey=self.parent.beh_df.loc[row_idx, 'folder_key'],
                Behavior=self.parent.beh_df.loc[row_idx, 'behavior'], 
                Fr_Start=self.parent.beh_df.loc[row_idx, 'start_fr'], 
                Fr_Stop=self.parent.beh_df.loc[row_idx, 'stop_fr'], 
                Comment=self.parent.beh_df.loc[row_idx, 'comment']
            )
        pass
    def setup_connection(self):
        self.parent.Delete_Beh_Data_Button.clicked.connect(self.delete_row)
        pass
    def add_row(self, FolderKey, Behavior, Fr_Start, Fr_Stop, Comment):
        # DataKey - string; NumFrames - int; FolderPath - string
        print("Comment: ", Comment)
        row_idx = self.parent.Behavior_Table.rowCount()
        self.parent.Behavior_Table.insertRow(row_idx)
        self.parent.Behavior_Table.setItem(row_idx, 0, QTableWidgetItem(FolderKey))
        self.parent.Behavior_Table.setItem(row_idx, 1, QTableWidgetItem(Behavior))
        self.parent.Behavior_Table.setItem(row_idx, 2, QTableWidgetItem(str(Fr_Start)))
        self.parent.Behavior_Table.setItem(row_idx, 3, QTableWidgetItem(str(Fr_Stop)))
        self.parent.Behavior_Table.setItem(row_idx, 4, QTableWidgetItem(Comment))
        pass
    def delete_row(self):
        indices = self.parent.Behavior_Table.selectionModel().selectedRows() 
        for index in sorted(indices, reverse=True):
            self.parent.Behavior_Table.removeRow(index.row())
            self.parent.beh_df.drop(index.row(), inplace=True)
        self.parent.beh_df.reset_index(drop=True, inplace=True)
        pass
