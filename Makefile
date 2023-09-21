UI_FILE=game_ui.ui

make build_ui:
	pyuic6 $(UI_FILE) -o game_ui.py
