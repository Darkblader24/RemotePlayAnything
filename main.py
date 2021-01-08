import os
import sys
import pathlib

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.main import Ui_MainWindow
from game import GameList

main_dir = pathlib.Path(os.path.dirname(__file__)).resolve()
resources_dir = os.path.join(str(main_dir), "resources")
icon_file = os.path.join(str(resources_dir), "logo.ico")

version = (1, 0)


def main():
    # This is only used for Pycharm to close the application when you only want to build the dependencies
    if len(sys.argv) > 1 and sys.argv[1] == '--build-only':
        print("Build successful!")
        return

    # Create the application object
    app = QApplication(sys.argv)

    # Create the main window
    main_window = QMainWindow()

    # Set icon
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/Icons/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    main_window.setWindowIcon(icon)

    # Load the custom UI settings from QtDesigner into the main window
    ui = Ui_MainWindow()
    ui.setupUi(main_window)

    main_window.statusBar().hide()

    # Initialize the list of games
    game_list = GameList(ui)

    # Set the version number
    version_str = ".".join([str(x) for x in version])
    ui.versionLabel.setText(f"Remote Play Anything v{version_str}")

    # Add click events to all the buttons
    ui.startGameButton.clicked.connect(game_list.start_game)
    ui.addGameButton.clicked.connect(game_list.add_game)
    ui.editGameButton.clicked.connect(game_list.edit_game)
    ui.removeGameButton.clicked.connect(game_list.remove_game)
    ui.gamesList.clicked.connect(game_list.select_game)

    # Set the size of the window to fixed
    main_window.statusBar().setSizeGripEnabled(False)
    main_window.setFixedSize(main_window.size())

    # Finally show the window
    main_window.show()

    # Exit the app after closing the window
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
