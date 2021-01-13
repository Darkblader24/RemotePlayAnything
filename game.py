import ctypes
import os
import sys
import json
import ntpath
import pathlib
import traceback
from typing import Optional

import easygui
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox

from ui.main import Ui_MainWindow
from ui.details import Ui_Dialog

main_dir = pathlib.Path(os.path.dirname(__file__)).resolve()
resources_dir = os.path.join(str(main_dir), "resources")
open_file_icon = os.path.join(str(resources_dir), "open_file.png")

exe_dir = main_dir
if not sys.executable.endswith("python.exe"):
    exe_dir, _ = ntpath.split(sys.executable)
config_file = os.path.join(str(exe_dir), "config_rpa.json")


# Blizzard game launch parameters: https://steamcommunity.com/sharedfiles/filedetails/?id=1113049716


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


class GameList:
    def __init__(self, ui: Ui_MainWindow):
        self.ui: Ui_MainWindow = ui
        self.game_list: list[Game] = []

        # Clear games from list and then load in all saved games
        self.ui.gamesList.clear()
        self.load_games_from_config()

    def try_except(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args[:-1] if len(args) > 1 else args, **kwargs)
            except Exception as e:
                print(e)
                self: GameList = args[0]
                self.show_error(str(e), str(traceback.format_exc()))
        return wrapper

    @try_except
    def save_games_to_config(self):
        with open(config_file, 'w', encoding="utf8") as outfile:
            data = {
                "games": [game.serialize() for game in self.game_list]
            }
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    @try_except
    def load_games_from_config(self):
        if os.path.isfile(config_file):
            try:
                with open(config_file, encoding="utf8") as file:
                    data = json.load(file)
                    saved_games = data if type(data) is list else data.get("games")
                    if saved_games is None:
                        self.delete_config()

                    for game in saved_games:
                        self.add_game(name=game["name"], path=game["path"], parameters=game["parameters"], show_details=False)
            except json.decoder.JSONDecodeError:
                self.delete_config()

    @try_except
    def delete_config(self):
        if os.path.isfile(config_file):
            os.remove(config_file)
            print("Config file got reset.")

    @try_except
    def get_selected_row(self) -> Optional[int]:
        selected_rows = self.ui.gamesList.selectedIndexes()
        if not selected_rows:
            return None
        return selected_rows[0].row()

    @try_except
    def get_selected_game(self) -> Optional[Game]:
        row = self.get_selected_row()
        if row is None:
            return None
        return self.game_list[row]

    @try_except
    def start_game(self):
        game = self.get_selected_game()
        if not game:
            self.show_error("No game selected", "Please select a game from the list first!")
            return

        # Check if file exists:
        if not game.is_valid_path():
            self.show_error("Game not found", "The path to the game is invalid! Please check the path of the game.")
            return

        # Run the game with steam overlay enabled
        cmd = game.get_file()
        if game.parameters:
            cmd += " " + game.parameters

        try:
            os.chdir(game.get_dir())
            subprocess.Popen(cmd)
        except WindowsError as e:
            error = str(e)
            if " 740]" in error:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", game.path, game.parameters, None, 1)
            else:
                self.show_error(text=error.replace("%1", game.name))

    @try_except
    def add_game(self, name=None, path=None, parameters=None, show_details=True):
        if show_details:
            result, name, path, parameters = self.open_details_dialog()
            if not result or not path:
                return

        game = Game(name, path, parameters)
        self.game_list.append(game)

        item = QtWidgets.QListWidgetItem()
        item.setText(game.title())
        self.ui.gamesList.addItem(item)

        if show_details:
            item.setSelected(True)
            self.set_selected_game_label(game)
            self.save_games_to_config()

    @try_except
    def remove_game(self):
        selected_rows = self.ui.gamesList.selectedIndexes()
        if not selected_rows:
            return

        for selected_row in selected_rows:
            row = selected_row.row()
            self.ui.gamesList.takeItem(row)
            self.game_list.pop(row)

        self.save_games_to_config()

    @try_except
    def edit_game(self):
        game = self.get_selected_game()
        row = self.get_selected_row()
        if not game:
            return

        result, name, path, parameters = self.open_details_dialog(name=game.name, path=game.path, parameters=game.parameters)
        if not result:
            return

        # Update the game details
        game.name = name
        game.path = path
        game.parameters = parameters

        # Update the item in the list and the selected game
        self.ui.gamesList.item(row).setText(name if name else path)
        self.ui.selectedGameLabel.setText(name)

        # Update the config
        self.save_games_to_config()

    @try_except
    def select_game(self):
        game = self.get_selected_game()
        if not game:
            return

        self.set_selected_game_label(game)

    def set_selected_game_label(self, game):
        self.ui.selectedGameLabel.setText(game.name)

    def show_error(self, title="Error", text="An error has occurred!"):
        message_box = QMessageBox()
        message_box.critical(self.ui.centralwidget, title, text)
        message_box.setMinimumWidth(1000)

    @try_except
    def open_details_dialog(self, name=None, path=None, parameters=None):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_Dialog()
        dialog.ui.setupUi(dialog)

        # Set the button icon
        pixmap = QPixmap(open_file_icon)
        icon = QIcon(pixmap)
        dialog.ui.openPathButton.setIcon(icon)

        # Fill in the forms
        dialog.ui.nameTextEdit.setPlainText(name)
        dialog.ui.pathTextEdit.setPlainText(path)
        dialog.ui.parametersTextEdit.setPlainText(parameters)

        # Add path button functionality
        dialog.ui.openPathButton.clicked.connect(lambda state, ui=dialog.ui: self.open_file_browser(ui))

        return dialog.exec_(), dialog.ui.nameTextEdit.toPlainText(), dialog.ui.pathTextEdit.toPlainText(), dialog.ui.parametersTextEdit.toPlainText()

    # @try_except
    def open_file_browser(self, dialog_ui: Optional[Ui_Dialog] = None):
        try:
            if not dialog_ui:
                return

            # Get the starting path
            start_path = dialog_ui.pathTextEdit.toPlainText()
            if start_path:
                start_path, _ = ntpath.split(start_path)
                start_path += os.path.sep + "*"
            else:
                start_path = None

            # Open the file browser and add the selected path to the path text field
            path = easygui.fileopenbox(title="Remote Play Anything", msg="Choose the game executable", default=start_path, filetypes=["*.exe"])
            if not path:
                return

            # If no name is in the name field or the name field is unchanged, set it as the file name
            curr_name = dialog_ui.nameTextEdit.toPlainText()
            curr_path = dialog_ui.pathTextEdit.toPlainText()
            if not curr_name or ntpath.split(curr_path)[1] == curr_name:
                _, name = ntpath.split(path)
                dialog_ui.nameTextEdit.setPlainText(name)

            # Then set the path field
            dialog_ui.pathTextEdit.setPlainText(path)
        except Exception as e:
            print(e)
            self.show_error(str(e), str(traceback.format_exc()))
