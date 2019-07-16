import numpy as np
import scipy.io as sio


from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets

class behaviorTableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(behaviorTableWidget, self).__init__()
        self.data = {}
        self.tSNE = None
        self.num_frame = 0
        self.initialize()

    def initialize(self):
        self.setGeometry(QtCore.QRect(990, 420, 430, 341))
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setObjectName("behaviorTable")
        self.setColumnCount(4)
        self.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(108, 108, 108))
        self.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(108, 108, 108))
        self.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(108, 108, 108))
        self.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(108, 109, 108))
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
        self.tSNE = sio.loadmat(filepath)['embed_values_i'] # (frame x 2)
        self.num_frame = self.tSNE.shape[0]
        pass

    def add_row(self, behavior, startFr, stopFr):
        if self.tSNE is not None:
            frame_i = int(startFr)
            frame_f = int(stopFr)
            num_row = self.rowCount() 
            if behavior in self.data:
                data = self.data[behavior]
                frame_list = np.concatenate((data['frame_list'],[(frame_i, frame_f)]), axis=0)
                self.data[behavior]['entry'] = data['entry']+1
                self.data[behavior]['frame_list'] = frame_list
                # update tsne values
                (tsneX, tsneY) = self.tsne_mean(behavior)
                self.data[behavior]['tsneX_item'] = tsneX
                self.data[behavior]['tsneY_item'] = tsneY
            else:
                self.setRowCount(num_row+1)
                # compute tsne mean
                tsne_mean = np.mean(self.tSNE[frame_i:frame_f,:], axis=0)
                # update data
                self.data[behavior] = {
                    "row_idx": num_row,
                    "entry": 1,
                    "tsneX_item": tsne_mean[0],
                    "tsneY_item": tsne_mean[1],
                    "frame_list": [(frame_i, frame_f)]
                }
            # create item
            beh_item = QtWidgets.QTableWidgetItem(behavior)
            entry_item = QtWidgets.QTableWidgetItem(str(self.data[behavior]['entry']))
            tsneX_item = QtWidgets.QTableWidgetItem(format(self.data[behavior]['tsneX_item'],'.4f'))
            tsneY_item = QtWidgets.QTableWidgetItem(format(self.data[behavior]['tsneY_item'],'.4f'))
            # add item
            row = self.data[behavior]['row_idx']
            self.setItem(row,0,beh_item)
            self.setItem(row,1,entry_item)
            self.setItem(row,2,tsneX_item)
            self.setItem(row,3,tsneY_item)
        else:
            print("Please Upload File")
        print(self.data)
        pass

    def tsne_mean(self, behavior):
        tsneX, tsneY = 0.0, 0.0
        num_fr = 0.0
        for (frame_i, frame_f) in self.data[behavior]['frame_list']:
            print("i", frame_i)
            print("f", frame_f)
            data = np.sum(self.tSNE[frame_i:frame_f+1,:], axis=0)
            tsneX, tsneY = data[0], data[1]
            num_fr += frame_f-frame_i+1
        return tsneX/num_fr, tsneY/num_fr








