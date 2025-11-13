from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Input
from textual.containers import Vertical
import requests
from common.account import Account

class ChatroomScreen(Screen):
    TITLE: str
    CCS_PATH = "css/chatroom.tcss"

    account: Account

    def __init__(self, account, other_user):
        super().__init__()
        self.account: Account = account

    def _on_mount(self) -> None:
        conversation = 