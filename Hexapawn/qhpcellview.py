# This Python file uses the following encoding: utf-8
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets


class QHpCellView(QtWidgets.QGraphicsView):
    click_signal = pyqtSignal(int)

    def __init__(self, parent):
        super(QHpCellView, self).__init__(parent)
        self.__cell_value = -1

    def set_cell_value(self, cell_val):
        self.__cell_value = cell_val

    def mousePressEvent(self, event):
        self.click_signal.emit(self.__cell_value)
