import enum


class Event(enum.Enum):
    TRUNSLUCENT = 0
    START_MENU_MODE = 1  # キャラウィンドウをダブルクリックしたときにメニューモードに切り替える
    SET_WINDOWPOS = 2  # ウィンドウの位置を調整する（ディスプレイ接続時に位置がずれるのを直す）
