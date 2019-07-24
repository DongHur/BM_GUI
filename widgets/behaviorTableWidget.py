import numpy as np
import scipy.io as sio

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QCursor, QFont, QColor
from PyQt5.QtWidgets import (QAbstractItemView, QTableWidgetItem)

class behaviorTableWidget(QtWidgets.QTableWidget):
    def __init__(self, con, *args, **kwargs):
        super(behaviorTableWidget, self).__init__()
        self.data = {}
        self.tSNE = None
        self.filepath = None
        self.num_frame = 0
        self.con = con
        self.initialize()

    def initialize(self):
        self.setGeometry(QRect(990, 420, 430, 341))
        self.setLayoutDirection(Qt.LeftToRight)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setObjectName("behaviorTable")
        self.setColumnCount(4)
        self.setRowCount(0)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QColor(108, 108, 108))
        self.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QColor(108, 108, 108))
        self.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QColor(108, 108, 108))
        self.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QColor(108, 109, 108))
        self.setHorizontalHeaderItem(3, item)
        self.horizontalHeader().setDefaultSectionSize(102)
        # set text
        item = self.horizontalHeaderItem(0)
        item.setText("Behavior")
        item = self.horizontalHeaderItem(1)
        item.setText("# Entry")
        item = self.horizontalHeaderItem(2)
        item.setText("tsne x (mean)")
        item = self.horizontalHeaderItem(3)
        item.setText("tsne y (mean)")
        pass

    def set_newfile(self, filepath):
        self.filepath = filepath
        self.tSNE = sio.loadmat(filepath)['embed_values_i'] # (frame x 2)
        self.num_frame = self.tSNE.shape[0]
        pass

    def add_row(self, behavior, startFr, stopFr):
        if self.tSNE is not None:
            # format incoming data
            frame_i = int(startFr)
            frame_f = int(stopFr)
            num_row = self.rowCount() 
            (tsneX, tsneY) = np.mean(self.tSNE[frame_i:frame_f,:], axis=0)
            # update sql data
            with self.con:
                cur = self.con.cursor()
                cur.execute("PRAGMA table_info('{}')".format(behavior))
                table = cur.fetchall()
                if not table:
                    cur.execute("CREATE TABLE '{}'(id INTEGER PRIMARY KEY, filename VARCHAR, startFr INT, stopFr INT, tsneX REAL, tsneY REAL)".format(behavior))
                cur.execute("INSERT INTO '{}'(filename, startFr, stopFr, tsneX, tsneY) VALUES(?,?,?,?,?)"
                    .format(behavior), (self.filepath, frame_i, frame_f, tsneX, tsneY))
            # update table based on sqlite data
            self.update_all_table()
        else:
            print(" - Please Upload File")

    def update_all_table(self):
        self.setRowCount(0);
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            beh_list = cur.fetchall()
            for idx, behavior in enumerate(beh_list):
                # fetch data for specific behavior
                cur.execute("SELECT tsneX, tsneY FROM '{}'".format(behavior[0]))
                rows = cur.fetchall()
                tsneX, tsneY = 0, 0
                for row in rows:
                    if row[0] is not None and row[1] is not None:
                        tsneX += row[0]
                        tsneY += row[1]
                # add item
                beh_item = QTableWidgetItem(behavior[0])
                entry_item = QTableWidgetItem(str(len(rows)))
                tsneX_item = QTableWidgetItem(format(tsneX/len(rows),'.4f'))
                tsneY_item = QTableWidgetItem(format(tsneY/len(rows),'.4f'))
                self.insertRow(self.rowCount())
                self.setItem(self.rowCount()-1,0,beh_item)
                self.setItem(self.rowCount()-1,1,entry_item)
                self.setItem(self.rowCount()-1,2,tsneX_item)
                self.setItem(self.rowCount()-1,3,tsneY_item)








