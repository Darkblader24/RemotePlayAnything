import os
import utils
import ntpath
import platform
import win32gui
import pywintypes

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWinExtras import QtWin


class Game:
    def __init__(self, name, path, parameters):
        if not name:
            _, name = ntpath.split(path)

        self.name = name
        self.path = path
        self.parameters = parameters

    def is_valid_path(self):
        return os.path.isfile(self.path)

    def title(self):
        return self.name if self.name else self.path

    def serialize(self):
        return self.__dict__

    def get_dir(self):
        return ntpath.split(self.path)[0]

    def get_file(self):
        return ntpath.split(self.path)[1]


class GameItemWidget(QtWidgets.QWidget):
    def __init__(self):
        super(GameItemWidget, self).__init__(None)

        # Set up labels
        self.nameLabel = QtWidgets.QLabel()
        self.iconLabel = QtWidgets.QLabel()

        # Set up layout
        self.boxLayout = QtWidgets.QHBoxLayout()
        self.boxLayout.addWidget(self.iconLabel)
        self.boxLayout.addWidget(self.nameLabel, 1)
        self.setLayout(self.boxLayout)

        # Set up design
        self.nameLabel.setStyleSheet("font: 15px;")


class GameListItem(QtWidgets.QListWidgetItem):
    def __init__(self, game_list, game: Game):
        super(GameListItem, self).__init__(game_list)
        self.game = game
        self.game_list: QtWidgets.QListWidget = game_list
        self.game_item_widget = GameItemWidget()

        # Set details
        self.update()

    def update(self):
        self.set_name(self.game.name if self.game.name else self.game.path)
        self.set_icon(self.game.path)
        self.setSizeHint(self.game_item_widget.sizeHint())

    def set_name(self, name):
        self.game_item_widget.nameLabel.setText(name)

    def set_icon(self, path):
        if platform.system() == "Windows":
            # Get the icons in different sizes from the binary
            try:
                large, small = win32gui.ExtractIconEx(path, 0, 10)
            except pywintypes.error:
                return

            # Convert it into a pixmap
            if large:
                pixmap: QPixmap = QtWin.fromHICON(large[0])
                self.game_item_widget.iconLabel.setPixmap(QPixmap.scaledToHeight(pixmap, 32))
            tuple(map(win32gui.DestroyIcon, small + large))

    def add_to_list(self):
        self.game_list.addItem(self)
        self.game_list.setItemWidget(self, self.game_item_widget)

    def move_up(self):
        try:
            current_row = self.game_list.currentRow()
            self.game_list.removeItemWidget(self)
            self.game_list.takeItem(current_row)

            self.setSizeHint(self.game_item_widget.sizeHint())
            self.game_list.insertItem(current_row - 1, self)
            # self.game_list.setItemWidget(self, self.game_item_widget)
        except Exception as e:
            utils.show_error(text=e)

    def move_down(self):
        try:
            current_row = self.game_list.currentRow()
            self.game_list.removeItemWidget(self)
            self.game_list.takeItem(current_row)

            self.setSizeHint(self.game_item_widget.sizeHint())
            self.game_list.insertItem(current_row + 1, self)
            # self.game_list.setItemWidget(self, self.game_item_widget)
        except Exception as e:
            utils.show_error(text=e)
