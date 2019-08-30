import sqlite3
import os
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

class Behaviors_Tab():
    def __init__(self, parent):
        self.parent = parent
    def setup(self):
        for folder_key in list(self.parent.Behavior_Store.keys()):
            df = self.parent.Behavior_Store[folder_key]
            print("df:", df)
            for row_idx in range(len(df)):
                self.add_row(
                    FolderKey=folder_key,
                    Behavior=df.loc[row_idx, 'behavior'], 
                    Fr_Start=df.loc[row_idx, 'fr_start'], 
                    Fr_Stop=df.loc[row_idx, 'fr_stop'], 
                    tSNE_X=df.loc[row_idx, 'tsne_x'], 
                    tSNE_Y=df.loc[row_idx, 'tsne_y'], 
                    Comment=df.loc[row_idx, 'comment']
                    )

        pass
    def add_row(self, FolderKey, Behavior, Fr_Start, Fr_Stop, tSNE_X, tSNE_Y, Comment):
        # DataKey - string; NumFrames - int; FolderPath - string
        row_idx = self.parent.Behavior_Table.rowCount()
        self.parent.Behavior_Table.insertRow(row_idx)
        self.parent.Behavior_Table.setItem(row_idx, 0, QTableWidgetItem(FolderKey))
        self.parent.Behavior_Table.setItem(row_idx, 1, QTableWidgetItem(Behavior))
        self.parent.Behavior_Table.setItem(row_idx, 2, QTableWidgetItem(str(Fr_Start)))
        self.parent.Behavior_Table.setItem(row_idx, 3, QTableWidgetItem(str(Fr_Stop)))
        self.parent.Behavior_Table.setItem(row_idx, 4, QTableWidgetItem(str(tSNE_X)))
        self.parent.Behavior_Table.setItem(row_idx, 5, QTableWidgetItem(str(tSNE_Y)))
        self.parent.Behavior_Table.setItem(row_idx, 6, QTableWidgetItem(Comment))
        pass