# This Python file uses the following encoding: utf-8
import sys
import hpengine

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene, QMessageBox
from PyQt6 import QtGui, QtCore

from ui_form import Ui_QHpWidget
import rc_hpres

class QHpWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_QHpWidget()
        self.ui.setupUi(self)
        self.__cell_list = [self.ui.hpgv_0, self.ui.hpgv_1, self.ui.hpgv_2, self.ui.hpgv_3, self.ui.hpgv_4, self.ui.hpgv_5, self.ui.hpgv_6, self.ui.hpgv_7, self.ui.hpgv_8]
        for cell_num in range(len(self.__cell_list)):
            self.__cell_list[cell_num].set_cell_value(cell_num)
            self.__cell_list[cell_num].click_signal.connect(self.cell_click)
        self.__game_finished = False
        self.__turn = 0
        self.__player_select = -1
        self.__controller = hpengine.HexapawnController()
        self.__timer = QtCore.QTimer(self)
        self.__timer.setInterval(1000)
        self.__timer.timeout.connect(self.on_timer)
        self.new_game()

    def cell_click(self, value):
        if not self.__game_finished:
            board_data = self.__controller.board_data
            if board_data[value] == 1:
                self.__player_select = value
                self.paint_cells()
            if (board_data[value] == 0 or board_data[value] == 2) and self.__player_select != -1:
                test = self.__controller.player_step(self.__player_select + 1, value + 1)
                if test == 0:
                    self.__player_select = -1
                    self.paint_cells()
                    self.check_result()
                    self.change_side()
        else:
            self.new_game()

    def new_game(self):
        self.__game_finished = False
        self.__turn = 0
        self.__player_select = -1
        self.__controller.init_board()
        self.__controller.init_ai()
        self.paint_cells()
        self.__timer.start()

    def paint_cells(self):
        board_data = self.__controller.board_data
        for cell_num in range(len(self.__cell_list)):
            scene = QGraphicsScene()
            pen = QtGui.QPen()
            brush = QtGui.QBrush()
            pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            pen.setWidth(1)
            if cell_num % 2 == 0:
                pen.setColor(QtCore.Qt.GlobalColor.white)
                brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
                brush.setColor(QtCore.Qt.GlobalColor.white)
            else:
                pen.setColor(QtCore.Qt.GlobalColor.lightGray)
                brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
                brush.setColor(QtCore.Qt.GlobalColor.lightGray)
            if cell_num == self.__player_select:
                pen.setColor(QtCore.Qt.GlobalColor.red)
            scene.addRect(0, 0, self.__cell_list[cell_num].width() - 1, self.__cell_list[cell_num].height() - 1, pen, brush)
            if board_data[cell_num] == 0:
                pixmap = QtGui.QPixmap(":/hp/images/blank.png")
                pixmap = pixmap.scaled(self.__cell_list[cell_num].width(), self.__cell_list[cell_num].height())
                scene.addPixmap(pixmap)
            if board_data[cell_num] == 1:
                pixmap = QtGui.QPixmap(":/hp/images/black.png")
                pixmap = pixmap.scaled(self.__cell_list[cell_num].width(), self.__cell_list[cell_num].height())
                scene.addPixmap(pixmap)
            if board_data[cell_num] == 2:
                pixmap = QtGui.QPixmap(":/hp/images/white.png")
                pixmap = pixmap.scaled(self.__cell_list[cell_num].width(), self.__cell_list[cell_num].height())
                scene.addPixmap(pixmap)
            self.__cell_list[cell_num].setScene(scene)

    def on_timer(self):
        if not self.__game_finished:
            if self.__turn == 1:
                self.__controller.computer_step()
                self.paint_cells()
                self.check_result()
                self.change_side()

    def change_side(self):
        self.__turn += 1
        self.__turn = self.__turn % 2

    def check_result(self):
        result = self.__controller.check_result(self.__turn + 1)
        if result == 2:
            QMessageBox.information(self, None, "I Win!")
        if result == 1:
            QMessageBox.information(self, None, "You Win!")
        print()
        if result != 0:
            self.__game_finished = True
            self.__controller.update_ai()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QHpWidget()
    widget.show()
    sys.exit(app.exec())
