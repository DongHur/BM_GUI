import os
import numpy as np

#import pyqt tools
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox

class Behaviors_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.setup_table()
        self.setup_connection()

    # ***** exec function *****
    def setup_connection(self):
        self.parent.Delete_Beh_Data_Button.clicked.connect(self.delete_row)
        self.parent.Beh_Export_Button.clicked.connect(self.export_data) 
    def setup_table(self):
        self.parent.Behavior_Table.clearContents()
        self.parent.Behavior_Table.setRowCount(0)
        (num_row, num_col) = self.parent.beh_df.shape
        for row_idx in range(num_row):
            self._add_row(
                FolderKey=self.parent.beh_df.loc[row_idx, 'folder_key'],
                Cluster_id=self.parent.beh_df.loc[row_idx, 'cluster_id'],
                Behavior=self.parent.beh_df.loc[row_idx, 'behavior'], 
                Fr_Start=self.parent.beh_df.loc[row_idx, 'start_fr'], 
                Fr_Stop=self.parent.beh_df.loc[row_idx, 'stop_fr'], 
                Comment=self.parent.beh_df.loc[row_idx, 'comment'])

    # ***** event listener function *****
    def export_data(self):
        dir_csv = os.getcwd() + "/behavior.csv"
        filepath = QFileDialog.getSaveFileName(self.parent, "Export Behavior Data", dir_csv ,"CSV(*.csv)")[0]
        if filepath != "":
            self.parent.beh_df.to_csv(filepath)
    def delete_row(self):
        # verify if user wants to delete
        choice = QMessageBox.question(self.parent, 'Delete Rows', "Are you sure you want to delete these rows?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            # delete rows and data points
            indices = self.parent.Behavior_Table.selectionModel().selectedRows() 
            for index in sorted(indices, reverse=True):
                self.parent.Behavior_Table.removeRow(index.row())
                self.parent.beh_df.drop(index.row(), inplace=True)
            self.parent.beh_df.reset_index(drop=True, inplace=True)
    
    # ***** helper function *****   
    def _add_row(self, FolderKey, Cluster_id, Behavior, Fr_Start, Fr_Stop, Comment):
        # DataKey - string; NumFrames - int; FolderPath - string
        row_idx = self.parent.Behavior_Table.rowCount()
        self.parent.Behavior_Table.insertRow(row_idx)
        self.parent.Behavior_Table.setItem(row_idx, 0, QTableWidgetItem(FolderKey))
        self.parent.Behavior_Table.setItem(row_idx, 1, QTableWidgetItem(str(Cluster_id)))
        self.parent.Behavior_Table.setItem(row_idx, 2, QTableWidgetItem(Behavior))
        self.parent.Behavior_Table.setItem(row_idx, 3, QTableWidgetItem(str(Fr_Start)))
        self.parent.Behavior_Table.setItem(row_idx, 4, QTableWidgetItem(str(Fr_Stop)))
        self.parent.Behavior_Table.setItem(row_idx, 5, QTableWidgetItem(Comment))
    
    
            
                
                
