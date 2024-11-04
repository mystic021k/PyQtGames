# This Python file uses the following encoding: utf-8
import sys
import tttengine

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene, QMessageBox
from PyQt6 import QtGui, QtCore

from ui_form import Ui_QTttWidget
import rc_tttres

class QTttWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_QTttWidget()
        self.ui.setupUi(self)
        self.__cell_list = [self.ui.tttgv_0, self.ui.tttgv_1, self.ui.tttgv_2, self.ui.tttgv_3, self.ui.tttgv_4, self.ui.tttgv_5, self.ui.tttgv_6, self.ui.tttgv_7, self.ui.tttgv_8]
        for cell_num in range(len(self.__cell_list)):
            self.__cell_list[cell_num].set_cell_value(cell_num)
            self.__cell_list[cell_num].click_signal.connect(self.cell_click)
        self.__game_finished = False
        self.__turn = 0
        self.__controller = tttengine.TictactoeController()
        self.__timer = QtCore.QTimer(self)
        self.__timer.setInterval(1000)
        self.__timer.timeout.connect(self.on_timer)
        self.new_game()

    def cell_click(self, value):
        if not self.__game_finished:
            test = self.__controller.player_step(value + 1)
            if test == 0:
                self.paint_cells()
                self.check_result()
                self.change_side()
        else:
            self.new_game()

    def new_game(self):
        self.__game_finished = False
        self.__turn = 0
        self.__controller.init_board()
        self.__controller.init_ai()
        self.paint_cells()
        self.__timer.start()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.PenStyle.NoPen))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.darkGray))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()

    def paint_cells(self):
        board_data = self.__controller.board_data
        for cell_num in range(len(self.__cell_list)):
            scene = QGraphicsScene()
            if board_data[cell_num] == 0:
                pixmap = QtGui.QPixmap(":/ttt/images/blank.gif")
                pixmap = pixmap.scaled(self.__cell_list[cell_num].width(), self.__cell_list[cell_num].height())
                scene.addPixmap(pixmap)
            if board_data[cell_num] == 1:
                pixmap = QtGui.QPixmap(":/ttt/images/cross.gif")
                pixmap = pixmap.scaled(self.__cell_list[cell_num].width(), self.__cell_list[cell_num].height())
                scene.addPixmap(pixmap)
            if board_data[cell_num] == 2:
                pixmap = QtGui.QPixmap(":/ttt/images/not.gif")
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
        result = self.__controller.check_result()
        if result == 2:
            QMessageBox.information(self, None, "I Win!")
        if result == 1:
            QMessageBox.information(self, None, "You Win!")
        if result == -1:
            QMessageBox.information(self, None, "Draw")
        print()
        if result != 0:
            self.__game_finished = True
            self.__controller.update_ai()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QTttWidget()
    widget.show()
    sys.exit(app.exec())
