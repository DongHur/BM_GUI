# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SaveFileGUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(371, 213)
        self.savedBehaviorEntryLabel = QtWidgets.QLabel(Form)
        self.savedBehaviorEntryLabel.setGeometry(QtCore.QRect(280, 10, 60, 16))
        self.savedBehaviorEntryLabel.setObjectName("savedBehaviorEntryLabel")
        self.frameLabel2 = QtWidgets.QLabel(Form)
        self.frameLabel2.setGeometry(QtCore.QRect(70, 70, 41, 16))
        self.frameLabel2.setObjectName("frameLabel2")
        self.saveBehaviorStartBox = QtWidgets.QLineEdit(Form)
        self.saveBehaviorStartBox.setEnabled(True)
        self.saveBehaviorStartBox.setGeometry(QtCore.QRect(130, 70, 61, 21))
        self.saveBehaviorStartBox.setText("")
        self.saveBehaviorStartBox.setObjectName("saveBehaviorStartBox")
        self.saveBehaviorStartBox.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.savedBehaviorComboBox = QtWidgets.QComboBox(Form)
        self.savedBehaviorComboBox.setGeometry(QtCore.QRect(0, 30, 211, 26))
        self.savedBehaviorComboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.savedBehaviorComboBox.setObjectName("savedBehaviorComboBox")
        self.tSNE_XmeanLabel = QtWidgets.QLabel(Form)
        self.tSNE_XmeanLabel.setGeometry(QtCore.QRect(20, 100, 321, 16))
        self.tSNE_XmeanLabel.setObjectName("tSNE_XmeanLabel")
        self.savedBehaviorLabel = QtWidgets.QLabel(Form)
        self.savedBehaviorLabel.setGeometry(QtCore.QRect(60, 10, 101, 16))
        self.savedBehaviorLabel.setObjectName("savedBehaviorLabel")
        self.saveBehaviorStopBox = QtWidgets.QLineEdit(Form)
        self.saveBehaviorStopBox.setGeometry(QtCore.QRect(220, 70, 61, 21))
        self.saveBehaviorStopBox.setText("")
        self.saveBehaviorStopBox.setObjectName("saveBehaviorStopBox")
        self.saveBehaviorStopBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.saveDashLabel = QtWidgets.QLabel(Form)
        self.saveDashLabel.setGeometry(QtCore.QRect(200, 70, 16, 16))
        self.saveDashLabel.setObjectName("saveDashLabel")
        self.saveFilenameBox = QtWidgets.QLineEdit(Form)
        self.saveFilenameBox.setGeometry(QtCore.QRect(10, 180, 241, 21))
        self.saveFilenameBox.setObjectName("saveFilenameBox")
        self.saveFilenameBox.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.saveFilenameButton = QtWidgets.QPushButton(Form)
        self.saveFilenameButton.setGeometry(QtCore.QRect(260, 170, 111, 41))
        self.saveFilenameButton.setObjectName("saveFilenameButton")
        self.entryNoComboBox = QtWidgets.QComboBox(Form)
        self.entryNoComboBox.setGeometry(QtCore.QRect(250, 30, 121, 26))
        self.entryNoComboBox.setObjectName("entryNoComboBox")
        self.tSNE_YmeanLabel = QtWidgets.QLabel(Form)
        self.tSNE_YmeanLabel.setGeometry(QtCore.QRect(20, 120, 321, 16))
        self.tSNE_YmeanLabel.setObjectName("tSNE_YmeanLabel")
        self.saveFilenameLabel = QtWidgets.QLabel(Form)
        self.saveFilenameLabel.setGeometry(QtCore.QRect(20, 160, 231, 16))
        self.saveFilenameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.saveFilenameLabel.setObjectName("saveFilenameLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.savedBehaviorEntryLabel.setText(_translate("Form", "Entry No."))
        self.frameLabel2.setText(_translate("Form", "Frame:"))
        self.tSNE_XmeanLabel.setText(_translate("Form", "tSNE X (mean): NaN"))
        self.savedBehaviorLabel.setText(_translate("Form", "Saved Behavior"))
        self.saveDashLabel.setText(_translate("Form", "-"))
        self.saveFilenameButton.setText(_translate("Form", "Save"))
        self.tSNE_YmeanLabel.setText(_translate("Form", "tSNE Y (mean): NaN"))
        self.saveFilenameLabel.setText(_translate("Form", "Filename"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
