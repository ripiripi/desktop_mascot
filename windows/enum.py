import enum


class Event(enum.Enum):
    TRUNSLUCENT = 0
    START_MENU_MODE = 1  # キャラウィンドウをダブルクリックしたときにメニューモードに切り替える
    SETWINDOWORDER = 2  # ウィンドウの重なり順を設定する
